#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

from torii.hdl                        import Array, Elaboratable, Module, Signal

from sol_usb.cli                      import cli
from sol_usb.gateware.usb.devices.ila import USBIntegratedLogicAnalyzer, USBIntegratedLogicAnalyzerFrontend

class ILAExample(Elaboratable):
	''' Gateware module that demonstrates use of the internal ILA. '''

	def __init__(self):
		self.counter = Signal(16)
		self.hello   = Signal(8)

		self.ila = USBIntegratedLogicAnalyzer(
			domain = 'usb',  # Sample from the USB domain.
			signals = [
				self.counter,
				self.hello
			],
			sample_depth = 32
		)

	def interactive_display(self):
		frontend = USBIntegratedLogicAnalyzerFrontend(ila = self.ila)
		frontend.interactive_display()

	def elaborate(self, platform):
		m = Module()
		m.submodules += self.ila

		# Generate our domain clocks/resets.
		m.submodules.car = platform.clock_domain_generator()

		# Clock divider / counter.
		m.d.usb += self.counter.eq(self.counter + 1)

		# Say 'hello world' constantly over our ILA...
		letters = Array(ord(i) for i in 'Hello, world! \r\n')

		current_letter = Signal(range(0, len(letters)))

		m.d.usb += current_letter.eq(current_letter + 1)
		m.d.comb += self.hello.eq(letters[current_letter])

		# Set our ILA to trigger each time the counter is at a random value.
		# This shows off our example a bit better than counting at zero.
		m.d.comb += self.ila.trigger.eq(self.counter == 227)

		# Return our elaborated module.
		return m

if __name__ == '__main__':
	example = cli(ILAExample)
	example.interactive_display()
