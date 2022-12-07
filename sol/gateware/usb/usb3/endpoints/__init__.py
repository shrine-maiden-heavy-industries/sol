# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' USB3 endpoint-type implementations. '''


from .control import USB3ControlEndpoint

__all__ = (
	'USB3ControlEndpoint',
)
