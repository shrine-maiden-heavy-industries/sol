#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>


from torii                  import *

from usb_construct.emitters import SuperSpeedDeviceDescriptorCollection

from sol_usb.cli                import cli
from sol_usb.usb3               import USBSuperSpeedDevice


class USBSuperSpeedExample(Elaboratable):
	''' Simple example of a USB SuperSpeed device using the SOL framework. '''


	def create_descriptors(self):
		''' Create the descriptors we want to use for our device. '''

		descriptors = SuperSpeedDeviceDescriptorCollection()

		#
		# We'll add the major components of the descriptors we we want.
		# The collection we build here will be necessary to create a standard endpoint.
		#

		# We'll need a device descriptor...
		with descriptors.DeviceDescriptor() as d:
			d.idVendor           = 0x16d0
			d.idProduct          = 0xf3b

			# We're complying with the USB 3.2 standard.
			d.bcdUSB             = 3.2

			# USB3 requires this to be '9', to indicate 2 ** 9, or 512B.
			d.bMaxPacketSize0    = 9

			d.iManufacturer      = 'SOL'
			d.iProduct           = 'SuperSpeed Test Device'
			d.iSerialNumber      = '1234'

			d.bNumConfigurations = 1


		# ... and a description of the USB configuration we'll provide.
		with descriptors.ConfigurationDescriptor() as c:
			c.bMaxPower        = 50

			with c.InterfaceDescriptor() as i:
				i.bInterfaceNumber = 0

				with i.EndpointDescriptor(add_default_superspeed = True) as e:
					e.bEndpointAddress = 0x01
					e.wMaxPacketSize   = 512

				with i.EndpointDescriptor(add_default_superspeed = True) as e:
					e.bEndpointAddress = 0x81
					e.wMaxPacketSize   = 512

		return descriptors


	def elaborate(self, platform):
		m = Module()

		# Generate our domain clocks/resets.
		m.submodules.car = platform.clock_domain_generator()

		# Create our core PIPE PHY. Since PHY configuration is per-board, we'll just ask
		# our platform for a pre-configured USB3 PHY.
		m.submodules.phy = phy = platform.create_usb3_phy()

		# Create our core SuperSpeed device.
		m.submodules.usb = usb = USBSuperSpeedDevice(phy = phy)

		# Add our standard control endpoint to the device.
		descriptors = self.create_descriptors()
		usb.add_standard_control_endpoint(descriptors)


		# Return our elaborated module.
		return m


if __name__ == '__main__':
	cli(USBSuperSpeedExample)
