# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Interfaces to SOL's PSRAM chips.'''


from torii         import Cat, Elaboratable, Module, Record, Signal
from torii.hdl.rec import DIR_FANIN, DIR_FANOUT

from ..utils.io    import delay


class HyperBus(Record):
	''' Record representing an HyperBus (DDR-ish connection for HyperRAM). '''

	def __init__(self):
		super().__init__([
			('clk', 1, DIR_FANOUT),
			('dq',
				('i', 8, DIR_FANIN),
				('o', 8, DIR_FANOUT),
				('e', 1, DIR_FANOUT),
			),
			('rwds',
				('i', 1, DIR_FANIN),
				('o', 1, DIR_FANOUT),
				('e', 1, DIR_FANOUT),
			),
			('cs',     1, DIR_FANOUT),
			('reset',  1, DIR_FANOUT)
		])



class HyperRAMInterface(Elaboratable):
	'''
	Gateware interface to HyperRAM series self-refreshing DRAM chips.

	I/O port:
		B: bus              -- The primary physical connection to the DRAM chip.
		I: reset            -- An active-high signal used to provide a prolonged reset upon configuration.

		I: address[32]      -- The address to be targeted by the given operation.
		I: register_space   -- When set to 1, read and write requests target registers instead of normal RAM.
		I: perform_write    -- When set to 1, a transfer request is viewed as a write, rather than a read.
		I: single_page      -- If set, data accesses will wrap around to the start of the current page when done.
		I: start_transfer   -- Strobe that goes high for 1-8 cycles to request a read operation.
							   [This added duration allows other clock domains to easily perform requests.]
		I: final_word       -- Flag that indicates the current word is the last word of the transaction.

		O: read_data[16]    -- word that holds the 16 bits most recently read from the PSRAM
		I: write_data[16]   -- word that accepts the data to output during this transaction

		O: idle             -- High whenever the transmitter is idle (and thus we can start a new piece of data.)
		O: new_data_ready   -- Strobe that indicates when new data is ready for reading

	''' # noqa: E101

	LOW_LATENCY_EDGES  = 6
	HIGH_LATENCY_EDGES = 14

	def __init__(self, *, bus, in_skew = None, out_skew = None, clock_skew = None):
		'''
		Parameters
		----------
		bus
			The RAM record that should be connected to this RAM chip.

		data_skews
			If provided, adds an input delay to each line of the data input.
			Can be provided as a single delay number, or an interable of eight
			delays to separately delay each of the input lines.

		'''

		self.in_skew    = in_skew
		self.out_skew   = out_skew
		self.clock_skew = clock_skew

		#
		# I/O port.
		#
		self.bus              = bus
		self.reset            = Signal()

		# Control signals.
		self.address          = Signal(32)
		self.register_space   = Signal()
		self.perform_write    = Signal()
		self.single_page      = Signal()
		self.start_transfer   = Signal()
		self.final_word       = Signal()

		# Status signals.
		self.idle             = Signal()
		self.new_data_ready   = Signal()

		# Data signals.
		self.read_data        = Signal(16)
		self.write_data       = Signal(16)


	def elaborate(self, platform):
		m = Module()

		#
		# Delayed input and output.
		#

		if self.in_skew is not None:
			data_in = delay(m, self.bus.dq.i, self.in_skew)
		else:
			data_in = self.bus.dq.i

		data_oe = self.bus.dq.oe
		if self.out_skew is not None:
			data_out = Signal.like(self.bus.dq.o)
			delay(m, data_out, self.out_skew, out = self.bus.dq.o)
		else:
			data_out = self.bus.dq.o


		#
		# Transaction clock generator.
		#
		advance_clock  = Signal()
		reset_clock    = Signal()

		if self.clock_skew is not None:
			out_clock = Signal()
			delay(m, out_clock, self.clock_skew, out = self.bus.clk)
		else:
			out_clock = self.bus.clk

		with m.If(reset_clock):
			m.d.sync += out_clock.eq(0)
		with m.Elif(advance_clock):
			m.d.sync += out_clock.eq(~out_clock)


		#
		# Latched control/addressing signals.
		#
		is_read         = Signal()
		is_register     = Signal()
		current_address = Signal(32)
		is_multipage    = Signal()

		#
		# FSM datapath signals.
		#

		# Tracks whether we need to add an extra latency period between our
		# command and the data body.
		extra_latency   = Signal()

		# Tracks how many cycles of latency we have remaining between a command
		# and the relevant data stages.
		latency_edges_remaining  = Signal(range(0, self.HIGH_LATENCY_EDGES + 1))

		# One cycle delayed version of RWDS.
		# This is used to detect edges in RWDS during reads, which semantically mean
		# we should accept new data.
		last_rwds = Signal.like(self.bus.rwds.i)
		m.d.sync += last_rwds.eq(self.bus.rwds.i)

		# Create a sync-domain version of our 'new data ready' signal.
		new_data_ready = self.new_data_ready

		#
		# Core operation FSM.
		#

		# Provide defaults for our control/status signals.
		m.d.sync += [
			advance_clock.eq(1),
			reset_clock.eq(0),
			new_data_ready.eq(0),

			self.bus.cs.eq(1),
			self.bus.rwds.oe.eq(0),
			self.bus.dq.oe.eq(0),
		]

		with m.FSM():

			# IDLE state: waits for a transaction request
			with m.State('IDLE'):
				m.d.sync += reset_clock.eq(1)
				m.d.comb += self.idle.eq(1)

				# Once we have a transaction request, latch in our control
				# signals, and assert our chip-select.
				with m.If(self.start_transfer):
					m.next = 'LATCH_RWDS'

					m.d.sync += [
						is_read.eq(~self.perform_write),
						is_register.eq(self.register_space),
						is_multipage.eq(~self.single_page),
						current_address.eq(self.address),
					]

				with m.Else():
					m.d.sync += self.bus.cs.eq(0)


			# LATCH_RWDS -- latch in the value of the RWDS signal, which determines
			# our read/write latency. Note that we advance the clock in this state,
			# as our out-of-phase clock signal will output the relevant data before
			# the next edge can occur.
			with m.State('LATCH_RWDS'):
				m.d.sync += extra_latency.eq(self.bus.rwds.i),
				m.next = 'SHIFT_COMMAND0'


			# Commands, in order of bytes sent:
			#   - WRBAAAAA
			#     W         => selects read or write; 1 = read, 0 = write
			#      R        => selects register or memory; 1 = register, 0 = memory
			#       B       => selects burst behavior; 0 = wrapped, 1 = linear
			#        AAAAA  => address bits [27:32]
			#
			#   - AAAAAAAA  => address bits [19:27]
			#   - AAAAAAAA  => address bits [11:19]
			#   - AAAAAAAA  => address bits [ 3:16]
			#   - 00000000  => [reserved]
			#   - 00000AAA  => address bits [ 0: 3]

			# SHIFT_COMMANDx -- shift each of our command bytes out
			with m.State('SHIFT_COMMAND0'):
				m.next = 'SHIFT_COMMAND1'

				# Build our composite command byte.
				command_byte = Cat(
					current_address[27:32],
					is_multipage,
					is_register,
					is_read
				)

				# Output our first byte of our command.
				m.d.sync += [
					data_out.eq(command_byte),
					data_oe.eq(1)
				]

			# Note: it's felt that this is more readable with each of these
			# states defined explicitly. If you strongly disagree, feel free
			# to PR a for-loop, here.~


			with m.State('SHIFT_COMMAND1'):
				m.d.sync += [
					data_out.eq(current_address[19:27]),
					data_oe.eq(1)
				]
				m.next = 'SHIFT_COMMAND2'

			with m.State('SHIFT_COMMAND2'):
				m.d.sync += [
					data_out.eq(current_address[11:19]),
					data_oe.eq(1)
				]
				m.next = 'SHIFT_COMMAND3'

			with m.State('SHIFT_COMMAND3'):
				m.d.sync += [
					data_out.eq(current_address[ 3:16]),
					data_oe.eq(1)
				]
				m.next = 'SHIFT_COMMAND4'

			with m.State('SHIFT_COMMAND4'):
				m.d.sync += [
					data_out.eq(0),
					data_oe.eq(1)
				]
				m.next = 'SHIFT_COMMAND5'

			with m.State('SHIFT_COMMAND5'):
				m.d.sync += [
					data_out.eq(current_address[0:3]),
					data_oe.eq(1)
				]

				# If we have a register write, we don't need to handle
				# any latency. Move directly to our SHIFT_DATA state.
				with m.If(is_register & ~is_read):
					m.next = 'WRITE_DATA_MSB'

				# Otherwise, react with either a short period of latency
				# or a longer one, depending on what the RAM requested via
				# RWDS.
				with m.Else():
					m.next = 'HANDLE_LATENCY'

					with m.If(extra_latency):
						m.d.sync += latency_edges_remaining.eq(self.HIGH_LATENCY_EDGES)
					with m.Else():
						m.d.sync += latency_edges_remaining.eq(self.LOW_LATENCY_EDGES)


			# HANDLE_LATENCY -- applies clock edges until our latency period is over.
			with m.State('HANDLE_LATENCY'):
				m.d.sync += latency_edges_remaining.eq(latency_edges_remaining - 1)

				with m.If(latency_edges_remaining == 0):
					with m.If(is_read):
						m.next = 'READ_DATA_MSB'
					with m.Else():
						m.next = 'WRITE_DATA_MSB'


			# STREAM_DATA_MSB -- scans in or out the first byte of data
			with m.State('READ_DATA_MSB'):

				# If RWDS has changed, the host has just sent us new data.
				with m.If(self.bus.rwds.i != last_rwds):
					m.d.sync += self.read_data[8:16].eq(data_in)
					m.next = 'READ_DATA_LSB'


			# STREAM_DATA_LSB -- scans in or out the second byte of data
			with m.State('READ_DATA_LSB'):

				# If RWDS has changed, the host has just sent us new data.
				# Sample it, and indicate that we now have a valid piece of new data.
				with m.If(self.bus.rwds.i != last_rwds):
					m.d.sync += [
						self.read_data[0:8].eq(data_in),
						new_data_ready.eq(1)
					]

					# If our controller is done with the transcation, end it.
					with m.If(self.final_word):
						m.next = 'RECOVERY'
						m.d.sync += advance_clock.eq(0)

					with m.Else():
						# m.next = 'READ_DATA_MSB'
						m.next = 'RECOVERY'


			# WRITE_DATA_MSB -- write the first of our two bytes of data to the to the PSRAM
			with m.State('WRITE_DATA_MSB'):
				m.d.sync += [
					data_out.eq(self.write_data[8:16]),
					data_oe.eq(1),
				]
				m.next = 'WRITE_DATA_LSB'


			# WRITE_DATA_LSB -- write the first of our two bytes of data to the to the PSRAM
			with m.State('WRITE_DATA_LSB'):
				m.d.sync += [
					data_out.eq(self.write_data[0:8]),
					data_oe.eq(1),
				]
				m.next = 'WRITE_DATA_LSB'

				# If we just finished a register write, we're done -- there's no need for recovery.
				with m.If(is_register):
					m.next = 'IDLE'
					m.d.sync += advance_clock.eq(0)

				with m.Elif(self.final_word):
					m.next = 'RECOVERY'
					m.d.sync += advance_clock.eq(0)

				with m.Else():
					# m.next = 'READ_DATA_MSB'
					m.next = 'RECOVERY'


			# RECOVERY state: wait for the required period of time before a new transaction
			with m.State('RECOVERY'):
				m.d.sync += [
					self.bus.cs.eq(0),
					advance_clock.eq(0)
				]

				# TODO: implement recovery
				m.next = 'IDLE'



		return m
