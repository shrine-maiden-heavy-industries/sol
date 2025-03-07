# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Import shortcuts for our most commonly used functionality. '''

# Create shorthands for the most common parts of the library's usb2 gateware.
from .gateware.usb.usb2.device                import USBDevice
from .gateware.usb.usb2.endpoint              import EndpointInterface
from .gateware.usb.usb2.endpoints.isochronous import USBIsochronousInEndpoint
from .gateware.usb.usb2.endpoints.status      import USBSignalInEndpoint
from .gateware.usb.usb2.endpoints.stream      import (
	USBMultibyteStreamInEndpoint, USBStreamInEndpoint, USBStreamOutEndpoint
)
from .gateware.usb.usb2.request               import RequestHandlerInterface

__all__ = (
	'USBDevice',
	'EndpointInterface',
	'USBIsochronousInEndpoint',
	'USBSignalInEndpoint',
	'USBMultibyteStreamInEndpoint',
	'USBStreamInEndpoint',
	'USBStreamOutEndpoint',
	'RequestHandlerInterface',
)
