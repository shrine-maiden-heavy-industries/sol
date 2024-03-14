# SPDX-License-Identifier: BSD-3-Clause

from unittest      import TestCase

from torii         import Module, Record, Signal
from torii.hdl.rec import DIR_FANIN, DIR_FANOUT

from sol_usb.gateware.test      import SolGatewareTestCase, sync_test_case
from sol_usb.gateware.utils.cdc import stretch_strobe_signal, synchronize

class StrobeStretcherTest(SolGatewareTestCase):
	''' Test case for our strobe stretcher function. '''


	def instantiate_dut(self):
		m = Module()

		# Create a module that only has our stretched strobe signal.
		m.strobe_in = Signal()
		m.stretched_strobe = stretch_strobe_signal(m, m.strobe_in, to_cycles = 2)

		return m


	def initialize_signals(self):
		yield self.dut.strobe_in.eq(0)


	@sync_test_case
	def test_stretch(self):

		# Ensure our stretched strobe stays 0 until it sees an input.
		yield
		self.assertEqual((yield self.dut.stretched_strobe), 0)
		yield
		self.assertEqual((yield self.dut.stretched_strobe), 0)

		# Apply our strobe, and validate that we immediately see a '1'...
		yield self.dut.strobe_in.eq(1)
		yield
		self.assertEqual((yield self.dut.stretched_strobe), 1)

		# ... ensure that 1 lasts for a second cycle ...
		yield self.dut.strobe_in.eq(0)
		yield
		self.assertEqual((yield self.dut.stretched_strobe), 1)

		# ... and then returns to 0.
		yield
		self.assertEqual((yield self.dut.stretched_strobe), 0)

		yield
		self.assertEqual((yield self.dut.stretched_strobe), 0)



class SynchronizedTest(TestCase):

	def test_signal(self):
		m = Module()
		m._MustUse__silence = True
		synchronize(m, Signal())

	def test_directional_record(self):
		m = Module()
		m._MustUse__silence = True

		record = Record([
			('sig_in',  1, DIR_FANIN),
			('sig_out', 1, DIR_FANOUT)
		])
		synchronize(m, record)

	def test_nested_record(self):
		m = Module()
		m._MustUse__silence = True

		record = Record([
			('sig_in',  1, DIR_FANIN),
			('sig_out', 1, DIR_FANOUT),
			('nested', [
				('subsig_in',  1, DIR_FANIN),
				('subsig_out', 1, DIR_FANOUT),
			])
		])
		synchronize(m, record)
