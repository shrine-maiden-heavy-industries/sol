#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>


from apollo_fpga            import create_ila_frontend

from torii                  import *

from sol_usb.cli                import cli
from sol_usb.gateware.debug.ila import SyncSerialILA
from sol_usb.gateware.platform  import NullPin
from sol_usb.gateware.utils.cdc import synchronize


class ILAExample(Elaboratable):
	''' Gateware module that demonstrates use of the internal ILA. '''

	def __init__(self):
		self.counter = Signal(28)
		self.ila  = SyncSerialILA(signals = [self.counter], sample_depth = 32)

	def emit_analysis_vcd(self, filename = '-'):
		frontend = create_ila_frontend(self.ila)
		frontend.emit_vcd(filename)


	def elaborate(self, platform):
		m = Module()
		m.submodules += self.ila

		# Clock divider / counter.
		m.d.sync += self.counter.eq(self.counter + 1)

		# Set our ILA to trigger each time the counter is at a random value.
		# This shows off our example a bit better than counting at zero.
		m.d.comb += self.ila.trigger.eq(self.counter == 7)

		# Grab our I/O connectors.
		leds    = [platform.request_optional('led', i, default = NullPin(), dir = 'o') for i in range(0, 6)]
		spi_bus = synchronize(m, platform.request('debug_spi'))

		# Attach the LEDs and User I/O to the MSBs of our counter.
		m.d.comb += Cat(leds).eq(self.counter[-7:-1])

		# Connect our ILA up to our board's aux SPI.
		m.d.comb += self.ila.spi.connect(spi_bus)

		# Return our elaborated module.
		return m


if __name__ == '__main__':
	example = cli(ILAExample)
	example.emit_analysis_vcd()
