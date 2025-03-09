# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2020 whitequark@whitequark.org
#
# The ECP5's DCU parameters/signals/instance have been partially documented by whitequark
# as part of the Yumewatari project: https://github.com/whitequark/Yumewatari.
#
# Code based in part on ``litex`` and ``liteiclink``.

''' Soft PIPE backend for the Lattice ECP5 SerDes. '''

from warnings  import warn
from importlib import import_module

__all__ = (
	'ECP5SerDesPLLConfiguration',
	'ECP5SerDesConfigInterface',
	'ECP5SerDesRegisterTranslator',
	'ECP5SerDesEqualizerInterface',
	'ECP5SerDesEqualizer',
	'ECP5SerDesResetSequencer',
	'ECP5SerDes',
	'ECP5SerDesPIPE',
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
