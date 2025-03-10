# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Stream multiplexers/arbiters. '''

from warnings  import warn

__all__ = (
	'StreamArbiter',
)

def __dir__() -> list[str]:
	return list({*globals(), *__all__})

def __getattr__(name: str):
	if name in __all__:
		from torii.lib.stream.simple import StreamArbiter
		warn(
			'The sol StreamArbiter has been replaced with the Torii standard library one\n'
			'sol_usb.gateware.stream.arbiter.StreamArbiter -> torii.lib.stream.simple.StreamArbiter',
			DeprecationWarning,
			stacklevel = 2
		)
		return StreamArbiter
	if name not in __dir__():
		raise AttributeError(f'Module {__name__!r} has no attribute {name!r}')
