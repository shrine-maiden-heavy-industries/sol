# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
#
# Code adapted from ``litex`` and ``usb3_pipe``.

''' SerDes-based USB3 PIPE PHY. '''


from .ecp5    import ECP5SerDesPIPE
from .xc7_gtp import XC7GTPSerDesPIPE
from .xc7_gtx import XC7GTXSerDesPIPE

__all__ = (
	'ECP5SerDesPIPE',
	'XC7GTPSerDesPIPE',
	'XC7GTXSerDesPIPE',
)
