#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

from torii.hdl                 import Cat, Elaboratable, Module, Signal

from sol_usb.cli               import cli
from sol_usb.gateware.platform import NullPin

class Blinky(Elaboratable):
	''' Hardware module that validates basic SOL functionality. '''

	def elaborate(self, platform):
		''' Generate the Blinky tester. '''

		m = Module()

		# Grab our I/O connectors.
		leds    = [platform.request_optional('led', i, default = NullPin()).o for i in range(0, 8)]
		user_io = [platform.request_optional('user_io', i, default = NullPin()).o for i in range(0, 8)]

		# Clock divider / counter.
		counter = Signal(28)
		m.d.sync += counter.eq(counter + 1)

		# Attach the LEDs and User I/O to the MSBs of our counter.
		m.d.comb += Cat(leds).eq(counter[-7:-1])
		m.d.comb += Cat(user_io).eq(counter[7:21])

		# Return our elaborated module.
		return m

if __name__ == '__main__':
	cli(Blinky)
