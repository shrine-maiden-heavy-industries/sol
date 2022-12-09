# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

# Try to import the SoC modules, will fail if lambdasoc is not installed
try:

	from .simplesoc import SimpleSoC		# noqa: F401
	from .uart      import UARTPeripheral	# noqa: F401

	__all__ = (
		'SimpleSoC',
		'UARTPeripheral',
	)
except ImportError:
	__all__ = ()
