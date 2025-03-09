# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

'''
Contains the organizing hardware used to add USB Device functionality
to your own designs; including the core :class:`USBDevice` class.
'''

from torii.hdl import Elaboratable, Module, Signal

from warnings  import warn
from importlib import import_module

__all__ = (
	'USBDevice',
)

def __dir__() -> list[str]:
	return list({*globals(), *__all__})

def __getattr__(name: str):
	if name in __all__:
		torii_usb_mod = __name__.replace('sol_usb', 'torii_usb').replace('.gateware', '')
		warn(
			'Core USB functionality has been migrated to torii_usb, see the migration guide: '
			'https://torii-usb.shmdn.link/migrating.html \n'
			f'(hint: replace \'{__name__}.{name}\' with \'{torii_usb_mod}.{name}\')',
			DeprecationWarning,
			stacklevel = 2
		)
		return import_module(torii_usb_mod).__dict__[name]
	if name not in __dir__():
		raise AttributeError(f'Module {__name__!r} has no attribute {name!r}')


# TODO(aki): Figure out what the hecc to do with this
#
# Section that requires our CPU framework.
# We'll very deliberately section that off, so it
#
try:

	from ...soc.peripheral import Peripheral

	class USBDeviceController(Peripheral, Elaboratable):
		''' SoC controller for a USBDevice.

		Breaks our USBDevice control and status signals out into registers so a CPU / Wishbone master
		can control our USB device.

		The attributes below are intended to connect to a USBDevice. Typically, they'd be created by
		using the .controller() method on a USBDevice object, which will automatically connect all
		relevant signals.

		Attributes
		----------

		connect: Signal(), output
			High when the USBDevice should be allowed to connect to a host.

		'''

		def __init__(self):
			super().__init__()

			#
			# I/O port
			#
			self.connect   = Signal(reset = 1)
			self.bus_reset = Signal()

			#
			# Registers.
			#

			regs = self.csr_bank()
			self._connect = regs.csr(1, 'rw', desc = '''
				Set this bit to '1' to allow the associated USB device to connect to a host.
			''')

			self._speed = regs.csr(2, 'r', desc = '''
				Indicates the current speed of the USB device. 0 indicates High; 1 => Full,
				2 => Low, and 3 => SuperSpeed (incl SuperSpeed+).
			''')

			self._reset_irq = self.event(mode = 'rise', name = 'reset', desc = '''
				Interrupt that occurs when a USB bus reset is received.
			''')

			# Wishbone connection.
			self._bridge    = self.bridge(data_width = 32, granularity = 8, alignment = 2)
			self.bus        = self._bridge.bus
			self.irq        = self._bridge.irq

		def attach(self, device: USBDevice):
			''' Returns a list of statements necessary to connect this to a USB controller.

			The returned values makes all of the connections necessary to provide control and fetch status
			from the relevant USB device. These can be made in either the combinatorial or synchronous domains,
			but combinatorial is recommended; as these signals are typically fed from a register anyway.

			Parameters
			----------
			device: USBDevice
				The :class:`USBDevice` object to be controlled.
			'''
			return [
				device.connect.eq(self.connect),
				self.bus_reset.eq(device.reset_detected),
				self._speed.r_data.eq(device.speed)
			]

		def elaborate(self, platform):
			m = Module()
			m.submodules.bridge = self._bridge

			# Core connection register.
			m.d.comb += self.connect.eq(self._connect.r_data)
			with m.If(self._connect.w_stb):
				m.d.usb += self._connect.r_data.eq(self._connect.w_data)

			# Reset-detection event.
			m.d.comb += self._reset_irq.stb.eq(self.bus_reset)

			return m

except ImportError:
	pass
