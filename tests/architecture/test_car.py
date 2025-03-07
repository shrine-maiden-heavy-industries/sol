# SPDX-License-Identifier: BSD-3-Clause

from sol_usb.gateware.architecture.car import PHYResetController
from sol_usb.gateware.test             import SolGatewareTestCase, sync_test_case

class PHYResetControllerTest(SolGatewareTestCase):
	FRAGMENT_UNDER_TEST = PHYResetController

	def initialize_signals(self):
		yield self.dut.trigger.eq(0)

	@sync_test_case
	def test_power_on_reset(self):

		#
		# After power-on, the PHY should remain in reset for a while.
		#
		yield
		self.assertEqual((yield self.dut.phy_reset), 1)

		yield from self.advance_cycles(30)
		self.assertEqual((yield self.dut.phy_reset), 1)

		yield from self.advance_cycles(60)
		self.assertEqual((yield self.dut.phy_reset), 1)

		#
		# Then, after the relevant reset time, it should resume being unasserted.
		#
		yield from self.advance_cycles(31)
		self.assertEqual((yield self.dut.phy_reset), 0)
		self.assertEqual((yield self.dut.phy_stop),  1)

		yield from self.advance_cycles(120)
		self.assertEqual((yield self.dut.phy_stop),  0)
