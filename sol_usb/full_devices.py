# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Import shortcuts for our ready-to-use devices. '''

# Create shorthands for the most common parts of the library's usb2 gateware.
from .gateware.usb.devices.acm import USBSerialDevice

__all__ = (
	'USBSerialDevice',
)
