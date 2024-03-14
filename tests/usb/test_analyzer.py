# SPDX-License-Identifier: BSD-3-Clause

from torii                           import Record, Module
from torii.sim                       import Settle
from typing                          import Iterable

from sol_usb.gateware.usb.analyzer   import USBAnalyzer
from sol_usb.gateware.interface.utmi import UTMIInterface
from sol_usb.gateware.test           import SolGatewareTestCase, usb_domain_test_case

class USBAnalyzerTest(SolGatewareTestCase):
	SYNC_CLOCK_FREQUENCY = None
	USB_CLOCK_FREQUENCY = 60e6

	dut: USBAnalyzer

	def instantiate_dut(self):
		self.utmi = UTMIInterface()
		self.analyzer = USBAnalyzer(utmi_interface = self.utmi, mem_depth = 128)
		return self.analyzer

	def advance_stream(self, value):
		yield self.utmi.rx_data.eq(value)
		yield

	@usb_domain_test_case
	def test_single_packet(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Ensure we're not capturing until a transaction starts.
		self.assertEqual((yield self.dut.capturing), 0)

		# Apply our first input, and validate that we start capturing.
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield self.utmi.rx_data.eq(0)
		yield
		yield

		# Provide some data.
		for i in range(1, 10):
			yield from self.advance_stream(i)
			self.assertEqual((yield self.dut.capturing), 1)

		# Ensure we're still capturing, _and_ that we have
		# data available.
		self.assertEqual((yield self.dut.capturing), 1)

		# End our packet.
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_stream(10)

		# Idle for several cycles.
		yield from self.advance_cycles(5)
		self.assertEqual((yield self.dut.capturing), 0)
		yield from self.advance_cycles(5)

		# Try to read back the capture data, byte by byte.
		self.assertEqual((yield self.dut.stream.valid), 1)

		# First, we should get a header with the total data length.
		# This should be 0x00, 0x0B; as we captured 11 bytes.
		self.assertEqual((yield self.dut.stream.payload), 0)
		yield self.dut.stream.ready.eq(1)
		yield

		# Validate that we get all of the bytes of the packet we expected.
		expected_data = [0x00, 0x0a] + list(range(0, 10))
		for datum in expected_data:
			self.assertEqual((yield self.dut.stream.payload), datum)
			yield

		# We should now be out of data -- verify that there's no longer data available.
		self.assertEqual((yield self.dut.stream.valid), 0)

	@usb_domain_test_case
	def test_short_packet(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Apply our first input, and validate that we start capturing.
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield self.utmi.rx_data.eq(0)
		yield

		# Provide some data.
		yield from self.advance_stream(0xAB)

		# End our packet.
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_stream(10)

		# Idle for several cycles.
		yield from self.advance_cycles(5)
		self.assertEqual((yield self.dut.capturing), 0)
		yield from self.advance_cycles(5)

		# Try to read back the capture data, byte by byte.
		self.assertEqual((yield self.dut.stream.valid), 1)

		# First, we should get a header with the total data length.
		# This should be 0x00, 0x01; as we captured 1 byte.
		self.assertEqual((yield self.dut.stream.payload), 0)
		yield self.dut.stream.ready.eq(1)
		yield

		# Validate that we get all of the bytes of the packet we expected.
		expected_data = [0x00, 0x01, 0xab]
		for datum in expected_data:
			self.assertEqual((yield self.dut.stream.payload), datum)
			yield

		# We should now be out of data -- verify that there's no longer data available.
		self.assertEqual((yield self.dut.stream.valid), 0)

	def queue_packet(self, packet: Iterable[int]):
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield
		for byte in packet:
			yield self.utmi.rx_data.eq(byte)
			yield
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_cycles(4)

	def read_length(self, expected_length: int):
		self.assertEqual((yield self.dut.stream.valid), 1)
		yield self.dut.stream.ready.eq(1)
		# Read the high byte
		actual_length = yield self.dut.stream.payload
		yield
		yield Settle()
		actual_length <<= 8
		# Then the low
		actual_length |= yield self.dut.stream.payload
		yield
		yield Settle()
		# And check that the reconstructed value matches expectations.
		self.assertEqual(actual_length, expected_length)

	def read_packet(self, expected_length: int):
		# Validate the length bytes
		yield from self.read_length(expected_length)
		# Pop the bytes out from the FIFO, we don't actually care what their values are here.
		for _ in range(expected_length):
			yield
		yield self.dut.stream.ready.eq(0)
		yield from self.advance_cycles(4)

	def read_overrun_marker(self):
		yield from self.read_length(0xffff)
		yield self.dut.stream.ready.eq(0)
		yield from self.advance_cycles(4)

	@usb_domain_test_case
	def test_overrun(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Queue the the packets in, triggering overrun with the final one
		yield from self.queue_packet((0x2d, 0x32, 0xc0))
		yield from self.queue_packet((0xc3, 0x80, 0x06, 0x02, 0x03, 0x09, 0x04, 0xff, 0x00, 0x97, 0xdb))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0x4b, 0x62, 0x03, 0x42, 0x00, 0x6c, 0x00, 0x61,
			0x00, 0x63, 0x00, 0x6b, 0x00, 0x20, 0x00, 0x4d,
			0x00, 0x61, 0x00, 0x67, 0x00, 0x69, 0x00, 0x63,
			0x00, 0x20, 0x00, 0x50, 0x00, 0x72, 0x00, 0x6f,
			0x00, 0x7a, 0x9c
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0xc3, 0x62, 0x00, 0x65, 0x00, 0x20, 0x00, 0x76,
			0x00, 0x31, 0x00, 0x2e, 0x00, 0x39, 0x00, 0x2e,
			0x00, 0x30, 0x00, 0x2d, 0x00, 0x72, 0x00, 0x63,
			0x00, 0x30, 0x00, 0x2d, 0x00, 0x39, 0x00, 0x34,
			0x00, 0xfd, 0x28
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0x4b, 0x2d, 0x00, 0x67, 0x00, 0x64, 0x00, 0x39,
			0x00, 0x37, 0x00, 0x65, 0x00, 0x63, 0x00, 0x38,
			0x00, 0x30, 0x00, 0x34, 0x00, 0x32, 0x00, 0x2d,
			0x00, 0x64, 0x00, 0x69, 0x00, 0x72, 0x00, 0x74,
			0x00, 0x8b, 0x79
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))

		# We have now tried to enqueue 160 bytes to the second-stage FIFO, overrunning it by 25 bytes.
		# Spin a few cycles to let the FIFOs all catch up
		yield from self.advance_cycles(50)

		# Now we can pop the packets and check that after 10 we get an overrun
		# marker and then a normal and happy packet
		yield from self.read_packet(3)
		yield from self.read_packet(11)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		yield from self.read_packet(35)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		yield from self.read_packet(35)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		# Now we expect the overrun marker, which is a length of 65535 (invalid in normal USB traffic)
		yield from self.read_overrun_marker()
		# And finally we expect a good ACK packet following.
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		self.assertEqual((yield self.dut.stream.valid), 0)

		# Having tested the second-stage FIFO, now lets overrun the first stage with a 1536 byte packet
		# (the first-stage FIFO can only handle 1027 bytes)
		yield from self.queue_packet(0xa5 for _ in range(1536))
		# Spin untill the FIFOs all catch up
		while (yield self.dut.stream.valid) == 0:
			yield
		yield from self.read_overrun_marker()
		# And finally let the second-stage FIFO state machine finish up
		yield from self.advance_cycles(1024)
		yield Settle()

class USBAnalyzerStackTest(SolGatewareTestCase):
	''' Test that evaluates a full-stack USB analyzer setup. '''

	SYNC_CLOCK_FREQUENCY = None
	USB_CLOCK_FREQUENCY = 60e6

	def instantiate_dut(self):

		from sol_usb.gateware.interface.ulpi import UTMITranslator

		self.ulpi = Record([
			('data', [
				('i',  8),
				('o',  8),
				('oe', 8),
			]),
			('nxt', 1),
			('stp', 1),
			('dir', [('i', 1)]),
			('clk', 1),
			('rst', 1)
		])

		# Create a stack of our UTMITranslator and our USBAnalyzer.
		# We'll wrap the both in a module to establish a synthetic hierarchy.
		m = Module()
		m.submodules.translator = self.translator = UTMITranslator(ulpi = self.ulpi, handle_clocking = False)
		m.submodules.analyzer   = self.analyzer   = USBAnalyzer(utmi_interface = self.translator, mem_depth = 128)
		return m

	def initialize_signals(self):

		# Ensure the translator doesn't need to perform any register reads/writes
		# by default, so we can focus on packet Rx.
		yield self.translator.xcvr_select.eq(1)
		yield self.translator.dm_pulldown.eq(1)
		yield self.translator.dp_pulldown.eq(1)
		yield self.translator.use_external_vbus_indicator.eq(0)

	@usb_domain_test_case
	def test_simple_analysis(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield from self.advance_cycles(10)

		# Start a new packet.
		yield self.ulpi.dir.eq(1)
		yield self.ulpi.nxt.eq(1)

		# Bus turnaround packet.
		yield self.ulpi.data.i.eq(0x80)
		yield

		# Provide some data to be captured.
		for i in [0x2d, 0x00, 0x10]:
			yield self.ulpi.data.i.eq(i)
			yield

		# Mark our packet as complete.
		yield self.ulpi.dir.eq(0)
		yield self.ulpi.nxt.eq(0)
		yield

		# Wait for a few cycles, for realism.
		yield from self.advance_cycles(10)

		# Read our data out of the PHY.
		yield self.analyzer.stream.ready.eq(1)
		yield

		# Validate that we got the correct packet out; plus headers.
		for i in [0x00, 0x03, 0x2d, 0x00, 0x10]:
			self.assertEqual((yield self.analyzer.stream.payload), i)
			yield
