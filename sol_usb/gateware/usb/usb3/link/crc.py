# SPDX-License-Identifier: BSD-3-Clause
# The line below is a hack to disable flake8 from yelling about the massive polynomial tables
# Eventually it'll be cleaned up, but as it's the only flake8 issue in this file left, it'll wait
# flake8: noqa
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' CRC computation gateware for USB3. '''

from warnings  import warn
from importlib import import_module

__all__ = (
	'compute_usb_crc5',
	'HeaderPacketCRC',
	'DataPacketPayloadCRC',
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
