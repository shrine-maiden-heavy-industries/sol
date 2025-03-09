# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
#
# Code adapted from ``usb3_pipe``.

'''
Code for handling SKP ordered sets on the transmit and receive path.

SKP ordered sets are provided in order to give some "padding data" that can be removed
in order to handle differences in transmitter/receiver clock rates -- a process called
"clock tolerance compensation" (CTC). The actual insertion and removal of SKP ordered sets
for CTC is handled by the PHY -- but it only adds and removes sets where it needs to to
compensate for clock differences.

It's up to us to insert and remove additional ordered sets.
'''

from warnings  import warn
from importlib import import_module

__all__ = (
	'CTCSkipRemover',
	'CTCSkipInserter',
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
