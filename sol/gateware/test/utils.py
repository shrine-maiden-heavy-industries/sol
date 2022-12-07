# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

""" Boilerplate for SOL unit tests. """

import math
import os
import unittest
from functools import wraps

from torii     import Signal
from torii.sim import Simulator


def sync_test_case(process_function, *, domain="sync"):
	""" Decorator that converts a function into a simple synchronous-process test case. """

	#
	# This function should automatically transform a given function into a pysim
	# synch process _without_ losing the function's binding on self. Accordingly,
	# we'll create a wrapper function that has self bound, and then a test case
	# that's closed over that wrapper function's context.
	#
	# This ensure that self is still accessible from the decorated function.
	#

	def run_test(self):
		@wraps(process_function)
		def test_case():
			yield from self.initialize_signals()
			yield from process_function(self)

		self.domain = domain
		self._ensure_clocks_present()
		self.sim.add_sync_process(test_case, domain=domain)
		self.simulate(vcd_suffix=process_function.__name__)

	return run_test


def usb_domain_test_case(process_function):
	"""
	Decorator that converts a function into a simple synchronous-process
	test case in the USB domain.
	"""
	return sync_test_case(process_function, domain='usb')


def fast_domain_test_case(process_function):
	"""
	Decorator that converts a function into a simple synchronous-process
	test case in the fast domain.
	"""
	return sync_test_case(process_function, domain='fast')


def ss_domain_test_case(process_function):
	"""
	Decorator that converts a function into a simple synchronous-process
	test case in the SuperSpeed domain.
	"""
	return sync_test_case(process_function, domain='ss')



class LunaGatewareTestCase(unittest.TestCase):

	domain = 'sync'

	# Convenience property: if set, instantiate_dut will automatically create
	# the relevant fragment with FRAGMENT_ARGUMENTS.
	FRAGMENT_UNDER_TEST = None
	FRAGMENT_ARGUMENTS = {}

	# Convenience properties: if not None, a clock with the relevant frequency
	# will automatically be added.
	FAST_CLOCK_FREQUENCY = None
	SYNC_CLOCK_FREQUENCY = 120e6
	USB_CLOCK_FREQUENCY  = None
	SS_CLOCK_FREQUENCY   = None


	def instantiate_dut(self):
		""" Basic-most function to instantiate a device-under-test.

		By default, instantiates FRAGMENT_UNDER_TEST.
		"""
		return self.FRAGMENT_UNDER_TEST(**self.FRAGMENT_ARGUMENTS)


	def get_vcd_name(self):
		""" Return the name to use for any VCDs generated by this class. """
		return "test_{}".format(self.__class__.__name__)


	def setUp(self):
		self.dut = self.instantiate_dut()
		self.sim = Simulator(self.dut)

		if self.USB_CLOCK_FREQUENCY:
			self.sim.add_clock(1 / self.USB_CLOCK_FREQUENCY, domain="usb")
		if self.SYNC_CLOCK_FREQUENCY:
			self.sim.add_clock(1 / self.SYNC_CLOCK_FREQUENCY, domain="sync")
		if self.FAST_CLOCK_FREQUENCY:
			self.sim.add_clock(1 / self.FAST_CLOCK_FREQUENCY, domain="fast")
		if self.SS_CLOCK_FREQUENCY:
			self.sim.add_clock(1 / self.SS_CLOCK_FREQUENCY, domain="ss")


	def initialize_signals(self):
		""" Provide an opportunity for the test apparatus to initialize siganls. """
		yield Signal()


	def traces_of_interest(self):
		""" Returns an interable of traces to include in any generated output. """
		return ()


	def simulate(self, *, vcd_suffix=None):
		""" Runs our core simulation. """

		# If we're generating VCDs, run the test under a VCD writer.
		if os.getenv('GENERATE_VCDS', default=False):

			# Figure out the name of our VCD files...
			vcd_name = self.get_vcd_name()
			if vcd_suffix:
				vcd_name = "{}_{}".format(vcd_name, vcd_suffix)

			# ... and run the simulation while writing them.
			traces = self.traces_of_interest()
			with self.sim.write_vcd(vcd_name + ".vcd", vcd_name + ".gtkw", traces=traces):
				self.sim.run()

		else:
			self.sim.run()


	@staticmethod
	def pulse(signal, *, step_after=True):
		""" Helper method that asserts a signal for a cycle. """
		yield signal.eq(1)
		yield
		yield signal.eq(0)

		if step_after:
			yield


	@staticmethod
	def advance_cycles(cycles):
		""" Helper methods that waits for a given number of cycles. """

		for _ in range(cycles):
			yield


	@staticmethod
	def wait_until(strobe, *, timeout=None):
		""" Helper method that advances time until a strobe signal becomes true. """

		cycles_passed = 0

		while not (yield strobe):
			yield

			cycles_passed += 1
			if timeout and cycles_passed > timeout:
				raise RuntimeError(f"Timeout waiting for '{strobe.name}' to go high!")


	def _ensure_clocks_present(self):
		""" Function that validates that a clock is present for our simulation domain. """
		frequencies = {
			'sync': self.SYNC_CLOCK_FREQUENCY,
			'usb':  self.USB_CLOCK_FREQUENCY,
			'fast': self.FAST_CLOCK_FREQUENCY,
			'ss': self.SS_CLOCK_FREQUENCY
		}
		self.assertIsNotNone(frequencies[self.domain], f"no frequency provied for `{self.domain}`-domain clock!")


	def wait(self, time):
		""" Helper method that waits for a given number of seconds in a *_test_case. """

		# Figure out the period of the clock we want to work with...
		if self.domain == 'sync':
			period = 1 / self.SYNC_CLOCK_FREQUENCY
		elif self.domain == 'usb':
			period = 1 / self.USB_CLOCK_FREQUENCY
		elif self.domain == 'fast':
			period = 1 / self.FAST_CLOCK_FREQUENCY

		# ... and, accordingly, how many cycles we want to delay.
		cycles = math.ceil(time / period)
		print(cycles)

		# Finally, wait that many cycles.
		yield from self.advance_cycles(cycles)


class LunaUSBGatewareTestCase(LunaGatewareTestCase):
	""" Specialized form of :class:``LunaGatewareTestCase`` that assumes a USB domain clock, but no others. """

	SYNC_CLOCK_FREQUENCY = None
	USB_CLOCK_FREQUENCY  = 60e6


class LunaSSGatewareTestCase(LunaGatewareTestCase):
	""" Specialized form of :class:``LunaGatewareTestCase`` that assumes a USB domain clock, but no others. """

	SYNC_CLOCK_FREQUENCY = None
	SS_CLOCK_FREQUENCY   = 125e6
