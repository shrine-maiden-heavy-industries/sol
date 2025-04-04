#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

from torii.hdl                      import Elaboratable, Module

from torii_usb.utils.cdc            import synchronize

from sol_usb.cli                    import cli
from sol_usb.gateware.interface.spi import SPIDeviceInterface

class DebugSPIExample(Elaboratable):
	''' Hardware meant to demonstrate use of the Debug Controller's SPI interface. '''

	def __init__(self):

		# Base ourselves around an SPI command interface.
		self.interface = SPIDeviceInterface(clock_phase = 1)

	def elaborate(self, platform):
		m = Module()
		board_spi = platform.request('debug_spi')

		# Use our command interface.
		m.submodules.interface = self.interface

		#
		# Synchronize and connect our SPI.
		#
		spi = synchronize(m, board_spi)
		m.d.comb  += self.interface.spi.connect(spi)

		# Turn on a single LED, just to show something's running.
		led = platform.request('led', 0).o
		m.d.comb += led.eq(1)

		# Echo back the last received data.
		m.d.comb += self.interface.word_out.eq(self.interface.word_in)

		return m

if __name__ == '__main__':
	cli(DebugSPIExample)
