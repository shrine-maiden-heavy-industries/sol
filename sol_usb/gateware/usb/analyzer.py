# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Low-level USB analyzer gateware. '''



from torii    import Elaboratable, Memory, Module, Signal

from ..stream import StreamInterface


class USBAnalyzer(Elaboratable):
	'''
	Core USB analyzer; backed by a small ringbuffer in FPGA block RAM.

	If you're looking to instantiate a full analyzer, you'll probably want to grab
	one of the DRAM-based ringbuffer variants (which are currently forthcoming).

	If you're looking to use this with a ULPI PHY, rather than the FPGA-convenient UTMI interface,
	grab the UTMITranslator from `sol.gateware.interface.ulpi`.

	Attributes
	----------
	stream: StreamInterface(), output stream
		Stream that carries USB analyzer data.

	idle: Signal(), output
		Asserted iff the analyzer is not currently receiving data.
	overrun: Signal(), output
		Asserted iff the analyzer has received more data than it can store in its internal buffer.
		Occurs if :attr:``stream`` is not being read quickly enough.
	capturing: Signal(), output
		Asserted iff the analyzer is currently capturing a packet.


	Parameters
	----------
	utmi_interface: UTMIInterface()
		The UTMI interface that carries the data to be analyzed.
	mem_depth: int, default = 8192
		The depth of the analyzer's local ringbuffer, in bytes.
		Must be a power of 2.
	'''

	# Current, we'll provide a packet header of 16 bits.
	HEADER_SIZE_BITS = 16
	HEADER_SIZE_BYTES = HEADER_SIZE_BITS // 8

	# Support a maximum payload size of 1024B, plus a 1-byte PID and a 2-byte CRC16.
	MAX_PACKET_SIZE_BYTES = 1024 + 1 + 2

	def __init__(self, *, utmi_interface, mem_depth = 65536):
		'''
		Parameters
		----------
		utmi_interface
			A record or elaboratable that presents a UTMI interface.

		'''

		self.utmi = utmi_interface

		if (mem_depth % 2) != 0:
			raise ValueError('mem_depth must be a power of 2')

		# Internal storage memory.
		self.mem = Memory(width = 8, depth = mem_depth, name = 'analysis_ringbuffer')
		self.mem_size = mem_depth

		#
		# I/O port
		#
		self.stream         = StreamInterface()

		self.capture_enable = Signal()
		self.idle           = Signal()
		self.overrun        = Signal()
		self.capturing      = Signal()

		# Diagnostic I/O.
		self.sampling       = Signal()


	def elaborate(self, platform):
		m = Module()

		# Memory read and write ports.
		m.submodules.read  = mem_read_port  = self.mem.read_port(domain = 'usb')
		m.submodules.write = mem_write_port = self.mem.write_port(domain = 'usb')

		# Store the memory address of our active packet header, which will store
		# packet metadata like the packet size.
		header_location = Signal.like(mem_write_port.addr)
		write_location  = Signal.like(mem_write_port.addr)

		# Read FIFO status.
		read_location   = Signal.like(mem_read_port.addr)
		fifo_count      = Signal.like(mem_read_port.addr, reset = 0)
		fifo_new_data   = Signal()

		# Current receive status.
		packet_size     = Signal(16)

		#
		# Read FIFO logic.
		#
		m.d.comb += [

			# We have data ready whenever there's data in the FIFO.
			self.stream.valid.eq((fifo_count != 0) & (self.idle | self.overrun)),

			# Our data_out is always the output of our read port...
			self.stream.payload.eq(mem_read_port.data),


			self.sampling.eq(mem_write_port.en)
		]

		# Once our consumer has accepted our current data, move to the next address.
		with m.If(self.stream.ready & self.stream.valid):
			m.d.usb += read_location.eq(read_location + 1)
			m.d.comb += mem_read_port.addr.eq(read_location + 1)

		with m.Else():
			m.d.comb += mem_read_port.addr.eq(read_location),



		#
		# FIFO count handling.
		#
		fifo_full = (fifo_count == self.mem_size)

		data_pop   = Signal()
		data_push  = Signal()
		m.d.comb += [
			data_pop.eq(self.stream.ready & self.stream.valid),
			data_push.eq(fifo_new_data & ~fifo_full)
		]

		# If we have both a read and a write, don't update the count,
		# as we've both added one and subtracted one.
		with m.If(data_push & data_pop):
			pass

		# Otherwise, add when data's added, and subtract when data's removed.
		with m.Elif(data_push):
			m.d.usb += fifo_count.eq(fifo_count + 1)
		with m.Elif(data_pop):
			m.d.usb += fifo_count.eq(fifo_count - 1)


		#
		# Core analysis FSM.
		#
		with m.FSM(domain = 'usb') as f:
			m.d.comb += [
				self.idle.eq(f.ongoing('START') | f.ongoing('IDLE')),
				self.overrun.eq(f.ongoing('OVERRUN')),
				self.capturing.eq(f.ongoing('CAPTURE')),
			]

			# START: wait for capture to be enabled, but don't start mid-packet.
			with m.State('START'):
				with m.If(self.capture_enable & ~self.utmi.rx_active):
					m.next = 'IDLE'


			# IDLE: capture is enabled, wait for a packet to start.
			with m.State('IDLE'):
				with m.If(~self.capture_enable):
					m.next = 'START'
				with m.Elif(self.utmi.rx_active):
					m.next = 'CAPTURE'
					m.d.usb += [
						header_location.eq(write_location),
						write_location.eq(write_location + self.HEADER_SIZE_BYTES),
						packet_size.eq(0),
					]


			# Capture data until the packet is complete.
			with m.State('CAPTURE'):

				byte_received = self.utmi.rx_valid & self.utmi.rx_active

				# Capture data whenever RxValid is asserted.
				m.d.comb += [
					mem_write_port.addr.eq(write_location),
					mem_write_port.data.eq(self.utmi.rx_data),
					mem_write_port.en.eq(byte_received),
					fifo_new_data.eq(byte_received),
				]

				# Advance the write pointer each time we receive a bit.
				with m.If(byte_received):
					m.d.usb += [
						write_location.eq(write_location + 1),
						packet_size.eq(packet_size + 1)
					]

					# If this would be filling up our data memory,
					# move to the OVERRUN state.
					with m.If(fifo_count == self.mem_size - 1 - self.HEADER_SIZE_BYTES):
						m.next = 'OVERRUN'

				# If we've stopped receiving, move to the 'finalize' state.
				with m.If(~self.utmi.rx_active):
					m.next = 'EOP_1'

					# Optimization: if we didn't receive any data, there's no need
					# to create a packet. Clear our header from the FIFO and disarm.
					with m.If(packet_size == 0):
						m.next = 'START'
						m.d.usb += [
							write_location.eq(header_location)
						]
					with m.Else():
						m.next = 'EOP_1'

			# EOP: handle the end of the relevant packet.
			with m.State('EOP_1'):

				# Now that we're done, add the header to the start of our packet.
				# This will take two cycles, currently, as we're using a 2-byte header,
				# but we only have an 8-bit write port.
				m.d.comb += [
					mem_write_port.addr.eq(header_location),
					mem_write_port.data.eq(packet_size[8:16]),
					mem_write_port.en.eq(1),
					fifo_new_data.eq(1)
				]
				m.next = 'EOP_2'


			with m.State('EOP_2'):

				# Add the second byte of our header.
				# Note that, if this is an adjacent read, we should have
				# just captured our packet header _during_ the stop turnaround.
				m.d.comb += [
					mem_write_port.addr.eq(header_location + 1),
					mem_write_port.data.eq(packet_size[0:8]),
					mem_write_port.en.eq(1),
					fifo_new_data.eq(1)
				]
				m.next = 'START'


			# BABBLE -- handles the case in which we've received a packet beyond
			# the allowable size in the USB spec
			with m.State('BABBLE'):

				# Trap here, for now.
				pass


			with m.State('OVERRUN'):
				# TODO: we should probably set an overrun flag and then emit an EOP, here?

				# If capture is stopped by the host, reset back to the ready state.
				with m.If(~self.capture_enable):
					m.next = 'START'


		return m
