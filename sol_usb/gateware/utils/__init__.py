# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#

''' Simple utility constructs for SOL. '''

from warnings  import warn
from importlib import import_module

__all__ = (
	'synchronize',
	'past_value_of',
	'rising_edge_detected',
	'falling_edge_detected',
	'any_edge_detected',
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
