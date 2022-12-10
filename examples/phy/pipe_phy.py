#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Incomplete example for working with a hardware PIPE PHY.'''

from torii   import *

from sol_usb.cli import cli

class PIPEPhyExample(Elaboratable):
	''' Hardware module that demonstrates grabbing a PHY resource with gearing. '''

	def elaborate(self, platform):
		m = Module()

		# Generate our domain clocks/resets.
		m.submodules.car = platform.clock_domain_generator()

		# Create our core PIPE PHY. Since PHY configuration is per-board, we'll just ask
		# our platform for a pre-configured USB3 PHY.
		m.submodules.phy = platform.create_usb3_phy()

		# Return our elaborated module.
		return m


if __name__ == '__main__':
	cli(PIPEPhyExample)
