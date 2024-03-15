# SPDX-License-Identifier: BSD-3-Clause

from torii                           import Module
from torii.sim                       import Settle, Tick
from typing                          import Union, Iterable, TypedDict
from concurrent.futures              import Future

from sol_usb.gateware.usb.analyzer   import USBAnalyzer
from sol_usb.gateware.interface.utmi import UTMIInterface
from sol_usb.gateware.test           import SolGatewareTestCase, usb_domain_test_case

class WaitDict(TypedDict):
	wait: float

class USBAnalyzerTest(SolGatewareTestCase):
	USB_CLOCK_FREQUENCY = 60e6
	SYNC_CLOCK_FREQUENCY = None

	dut: USBAnalyzer

	fast_traffic: tuple[Union[tuple[int, ...], WaitDict], ...] = (
		# SOF 1321
		(0xa5, 0x29, 0x9d),

		{'wait': 586e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 00 03 00 00 FF 00 ]
		(0xc3, 0x80, 0x06, 0x00, 0x03, 0x00, 0x00, 0xff, 0x00, 0xd4, 0x64),
		# ACK
		(0xd2,),

		{'wait': 7e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 04 03 04 09 ]
		(0x4b, 0x04, 0x03, 0x04, 0x09, 0xcc, 0x2d),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 343.75e-6},
		# SOF 1322
		(0xa5, 0x2a, 0xbb),

		{'wait': 997.5e-6},
		# SOF 1323
		(0xa5, 0x2b, 0x25),

		{'wait': 22.5e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 03 03 04 09 FF 00 ]
		(0xc3, 0x80, 0x06, 0x03, 0x03, 0x04, 0x09, 0xff, 0x00, 0x05, 0x65),
		# ACK
		(0xd2,),

		{'wait': 7.5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 12 03 42 00 46 00 43 00 35 00 39 00 30 00 46 00 35 00 ]
		(0x4b, 0x12, 0x03, 0x42, 0x00, 0x45, 0x00, 0x35, 0x00, 0x39, 0x00, 0x30, 0x00, 0x46, 0x00, 0x35,
		0x00, 0xfd, 0xc3),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 888e-6},
		# SOF 1324
		(0xa5, 0x2c, 0x5b),

		{'wait': 997.5e-6},
		# SOF 1340
		(0xa5, 0x3c, 0xbd),

		{'wait': 248.25e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 00 03 00 00 FF 00 ]
		(0xc3, 0x80, 0x06, 0x00, 0x03, 0x00, 0x00, 0xff, 0x00, 0xd4, 0x64),
		# ACK
		(0xd2,),

		{'wait': 7.5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 04 03 04 09 ]
		(0x4b, 0x04, 0x03, 0x04, 0x09, 0xcc, 0x2d),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 681.6e-6},
		# SOF 1341
		(0xa5, 0x3b, 0x45),

		{'wait': 997.5e-6},
		# SOF 1342
		(0xa5, 0x3e, 0x05),

		{'wait': 23e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 02 03 04 09 FF 00 ]
		(0xc3, 0x80, 0x06, 0x02, 0x03, 0x04, 0x09, 0xff, 0x00, 0x04, 0xb4),
		# ACK
		(0xd2,),

		{'wait': 7.5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 34 03 64 00 72 00 61 00 67 00 6f 00 6e 00 42 00 6f 00 6f 00 74 00 20 00 44 00 46 00 2a 00 10 00 31 00 37 00 37 00 3a 00 36 00 37 00 30 00 32 00 32 00 39 00 ]
		(0x4b, 0x34, 0x03, 0x64, 0x00, 0x72, 0x00, 0x61, 0x00, 0x67, 0x00, 0x6f, 0x00, 0x6e, 0x00, 0x42,
		0x00, 0x6f, 0x00, 0x6f, 0x00, 0x74, 0x00, 0x20, 0x00, 0x44, 0x00, 0x46, 0x00, 0x2a, 0x00, 0x10,
		0x00, 0x31, 0x00, 0x37, 0x00, 0x37, 0x00, 0x3a, 0x00, 0x36, 0x00, 0x37, 0x00, 0x30, 0x00, 0x32,
		0x00, 0x32, 0x00, 0x39, 0x00, 0xc7, 0x8a),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 835e-6},
		# SOF 1343
		(0xa5, 0x3f, 0xfd),

		{'wait': 997.5e-6},
		# SOF 1344
		(0xa5, 0x40, 0xc5),

		{'wait': 22.5e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 00 03 00 00 FF 00 ]
		(0xc3, 0x80, 0x06, 0x00, 0x03, 0x00, 0x00, 0xff, 0x00, 0xd4, 0x64),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 04 03 04 09 ]
		(0x4b, 0x04, 0x03, 0x04, 0x09, 0xcc, 0x2d),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 903e-6},
		# SOF 1345
		(0xa5, 0x41, 0x3d),

		{'wait': 997.5e-6},
		# SOF 1346
		(0xa5, 0x42, 0x7d),

		{'wait': 89e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 03 03 04 09 FF 00 ]
		(0xc3, 0x80, 0x06, 0x03, 0x03, 0x04, 0x09, 0xff, 0x00, 0x05, 0x65),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 12 03 42 00 46 00 43 00 35 00 39 00 30 00 46 00 35 00 ]
		(0x4b, 0x12, 0x03, 0x42, 0x00, 0x46, 0x00, 0x43, 0x00, 0x35, 0x00, 0x39, 0x00, 0x30, 0x00, 0x46,
		0x00, 0x35, 0x00, 0xcc, 0x2d),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 821.5e-6},
		# SOF 1347
		(0xa5, 0x43, 0x85),

		{'wait': 997.5e-6},
		# SOF 1348
		(0xa5, 0x44, 0xfd),

		{'wait': 89e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 01 0b 00 00 00 00 00 00 ]
		(0xc3, 0x01, 0x0b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc4, 0xf8),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 859e-6},
		# SOF 1349
		(0xa5, 0x45, 0x05),

		{'wait': 997.5e-6},
		# SOF 1350
		(0xa5, 0x46, 0x45),

		{'wait': 88e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 00 03 00 00 FF 00 ]
		(0xc3, 0x80, 0x06, 0x00, 0x03, 0x00, 0x00, 0xff, 0x00, 0xd4, 0x64),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 04 03 04 09 ]
		(0x4b, 0x04, 0x03, 0x04, 0x09, 0xcc, 0x2d),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 841.5e-6},
		# SOF 1351
		(0xa5, 0x47, 0xbd),

		{'wait': 997.5e-6},
		# SOF 1352
		(0xa5, 0x48, 0xb5),

		{'wait': 88.5e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 80 06 05 03 04 09 FF 00 ]
		(0xc3, 0x80, 0x06, 0x05, 0x03, 0x04, 0x09, 0xff, 0x00, 0x05, 0x03),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 44 03 44 00 65 00 76 00 69 00 63 00 65 00 20 00 46 00 69 00 72 00 6d 00 77 00 61 00 72 00 65 00 20 00 55 00 70 00 67 00 72 00 30 00 32 00 32 00 10 00 34 00 37 00 3a 00 32 00 39 00 33 00 30 00 ]
		(0x4b, 0x44, 0x03, 0x44, 0x00, 0x65, 0x00, 0x76, 0x00, 0x69, 0x00, 0x63, 0x00, 0x65, 0x00, 0x20,
		0x00, 0x46, 0x00, 0x69, 0x00, 0x72, 0x00, 0x6d, 0x00, 0x77, 0x00, 0x61, 0x00, 0x72, 0x00, 0x65,
		0x00, 0x20, 0x00, 0x55, 0x00, 0x70, 0x00, 0x67, 0x00, 0x72, 0x00, 0x30, 0x00, 0x32, 0x00, 0x32,
		0x00, 0x10, 0x00, 0x34, 0x00, 0x37, 0x00, 0x3a, 0x00, 0x32, 0x00, 0x39, 0x00, 0x33, 0x00, 0x30,
		0x00, 0x7e, 0xf1),
		# ACK
		(0xd2,),

		{'wait': 6e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA0 [ 63 00 65 00 ]
		(0xc3, 0x63, 0x00, 0x65, 0x00, 0xca, 0xcf),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 725e-6},
		# SOF 1353
		(0xa5, 0x49, 0x4d),

		{'wait': 997.5e-6},
		# SOF 1354
		(0xa5, 0x4a, 0x0d),

		{'wait': 44e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ a1 03 00 00 00 00 00 10 ]
		(0xc3, 0xa1, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x46, 0x8c),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 00 00 00 02 00 ]
		(0x4b, 0x00, 0x00, 0x00, 0x02, 0x00, 0xfe, 0x84),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 883.5e-6},
		# SOF 1355
		(0xa5, 0x4b, 0xf5),

		{'wait': 997.5e-6},
		# SOF 1356
		(0xa5, 0x4c, 0x8d),

		{'wait': 24e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ a1 03 00 00 00 00 00 10 ]
		(0xc3, 0xa1, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x46, 0x8c),
		# ACK
		(0xd2,),

		{'wait': 8e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# NAK
		(0x5a,),

		{'wait': 5e-6},
		# IN ADDR 74 EP 0
		(0x69, 0x4a, 0x80),
		# DATA1 [ 00 00 00 02 00 ]
		(0x4b, 0x00, 0x00, 0x00, 0x02, 0x00, 0xfe, 0x84),
		# ACK
		(0xd2,),

		{'wait': 8.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ ]
		(0x4b, 0x00, 0x00),
		# ACK
		(0xd2,),

		{'wait': 903.75e-6},
		# SOF 1357
		(0xa5, 0x4d, 0x75),

		{'wait': 997.5e-6},
		# SOF 1358
		(0xa5, 0x4e, 0x35),

		{'wait': 96.5e-6},
		# SETUP ADDR 74 EP 0
		(0x2d, 0x4a, 0x80),
		# DATA0 [ 21 01 00 00 00 00 00 10 ]
		(0xc3, 0xa1, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x46, 0x8c),
		# ACK
		(0xd2,),

		{'wait': 16.5e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ 00 50 00 20 11 06 01 08 0f 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 01 08 00 00 00 00 00
		#         00 00 00 00 00 00 00 00 00 00 00 0f 06 01 08 5d f4 00 08 00 00 00 00 0f 06 01 08 2b f6 00 08 ]
		(0x4b, 0x00, 0x50, 0x00, 0x20, 0x11, 0x06, 0x01, 0x08, 0x0f, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x01, 0x08, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x06, 0x01, 0x08,
		0x5d, 0xf4, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x06, 0x01, 0x08, 0x2b, 0xf6, 0x00, 0x08,
		0x14, 0xbf),
		# ACK
		(0xd2,),

		{'wait': 15e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08
		#         0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 a9 e6 00 08 b1 e6 00 08 ]
		(0x4b, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0xa9, 0xe6, 0x00, 0x08, 0xb1, 0xe6, 0x00,
		0x08, 0x65, 0xa9),
		# NAK
		(0x5a,),

		{'wait': 15e-6},
		# OUT ADDR 74 EP 0
		(0xe1, 0x4a, 0x80),
		# DATA1 [ 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08
		#         0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 0d 06 01 08 a9 e6 00 08 b1 e6 00 08 ]
		(0x4b, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01,
		0x08, 0x0d, 0x06, 0x01, 0x08, 0x0d, 0x06, 0x01, 0x08, 0xa9, 0xe6, 0x00, 0x08, 0xb1, 0xe6, 0x00,
		0x08, 0x65, 0xa9),
		# ACK
		(0xd2,),
	)

	def instantiate_dut(self):
		self.utmi = UTMIInterface()
		self.analyzer = USBAnalyzer(utmi_interface = self.utmi, mem_depth = 128)
		return self.analyzer

	def advance_stream(self, value):
		yield self.utmi.rx_data.eq(value)
		yield

	@usb_domain_test_case
	def test_single_packet(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Ensure we're not capturing until a transaction starts.
		self.assertEqual((yield self.dut.capturing), 0)

		# Apply our first input, and validate that we start capturing.
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield self.utmi.rx_data.eq(0)
		yield
		yield

		# Provide some data.
		for i in range(1, 10):
			yield from self.advance_stream(i)
			self.assertEqual((yield self.dut.capturing), 1)

		# Ensure we're still capturing, _and_ that we have
		# data available.
		self.assertEqual((yield self.dut.capturing), 1)

		# End our packet.
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_stream(10)

		# Idle for several cycles.
		yield from self.advance_cycles(5)
		self.assertEqual((yield self.dut.capturing), 0)
		yield from self.advance_cycles(5)

		# Try to read back the capture data, byte by byte.
		self.assertEqual((yield self.dut.stream.valid), 1)

		# First, we should get a header with the total data length.
		# This should be 0x00, 0x0B; as we captured 11 bytes.
		self.assertEqual((yield self.dut.stream.payload), 0)
		yield self.dut.stream.ready.eq(1)
		yield

		# Validate that we get all of the bytes of the packet we expected.
		expected_data = [0x00, 0x0a] + list(range(0, 10))
		for datum in expected_data:
			self.assertEqual((yield self.dut.stream.payload), datum)
			yield

		# We should now be out of data -- verify that there's no longer data available.
		self.assertEqual((yield self.dut.stream.valid), 0)

	@usb_domain_test_case
	def test_short_packet(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Apply our first input, and validate that we start capturing.
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield self.utmi.rx_data.eq(0)
		yield

		# Provide some data.
		yield from self.advance_stream(0xAB)

		# End our packet.
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_stream(10)

		# Idle for several cycles.
		yield from self.advance_cycles(5)
		self.assertEqual((yield self.dut.capturing), 0)
		yield from self.advance_cycles(5)

		# Try to read back the capture data, byte by byte.
		self.assertEqual((yield self.dut.stream.valid), 1)

		# First, we should get a header with the total data length.
		# This should be 0x00, 0x01; as we captured 1 byte.
		self.assertEqual((yield self.dut.stream.payload), 0)
		yield self.dut.stream.ready.eq(1)
		yield

		# Validate that we get all of the bytes of the packet we expected.
		expected_data = [0x00, 0x01, 0xab]
		for datum in expected_data:
			self.assertEqual((yield self.dut.stream.payload), datum)
			yield

		# We should now be out of data -- verify that there's no longer data available.
		self.assertEqual((yield self.dut.stream.valid), 0)

	def queue_packet(self, packet: Iterable[int]):
		yield self.utmi.rx_active.eq(1)
		yield self.utmi.rx_valid.eq(1)
		yield
		for byte in packet:
			yield self.utmi.rx_data.eq(byte)
			yield
		yield self.utmi.rx_active.eq(0)
		yield from self.advance_cycles(4)

	def read_length(self, expected_length: int):
		self.assertEqual((yield self.dut.stream.valid), 1)
		yield self.dut.stream.ready.eq(1)
		# Read the high byte
		actual_length = yield self.dut.stream.payload
		yield
		yield Settle()
		actual_length <<= 8
		# Then the low
		actual_length |= yield self.dut.stream.payload
		yield
		yield Settle()
		# And check that the reconstructed value matches expectations.
		self.assertEqual(actual_length, expected_length)

	def read_packet(self, expected_length: int):
		# Validate the length bytes
		yield from self.read_length(expected_length)
		# Pop the bytes out from the FIFO, we don't actually care what their values are here.
		for _ in range(expected_length):
			yield
		yield self.dut.stream.ready.eq(0)
		yield from self.advance_cycles(4)

	def read_overrun_marker(self):
		yield from self.read_length(0xffff)
		yield self.dut.stream.ready.eq(0)
		yield from self.advance_cycles(4)

	@usb_domain_test_case
	def test_overrun(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield

		# Queue the the packets in, triggering overrun with the final one
		yield from self.queue_packet((0x2d, 0x32, 0xc0))
		yield from self.queue_packet((0xc3, 0x80, 0x06, 0x02, 0x03, 0x09, 0x04, 0xff, 0x00, 0x97, 0xdb))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0x4b, 0x62, 0x03, 0x42, 0x00, 0x6c, 0x00, 0x61,
			0x00, 0x63, 0x00, 0x6b, 0x00, 0x20, 0x00, 0x4d,
			0x00, 0x61, 0x00, 0x67, 0x00, 0x69, 0x00, 0x63,
			0x00, 0x20, 0x00, 0x50, 0x00, 0x72, 0x00, 0x6f,
			0x00, 0x7a, 0x9c
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0xc3, 0x62, 0x00, 0x65, 0x00, 0x20, 0x00, 0x76,
			0x00, 0x31, 0x00, 0x2e, 0x00, 0x39, 0x00, 0x2e,
			0x00, 0x30, 0x00, 0x2d, 0x00, 0x72, 0x00, 0x63,
			0x00, 0x30, 0x00, 0x2d, 0x00, 0x39, 0x00, 0x34,
			0x00, 0xfd, 0x28
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))
		yield from self.queue_packet((
			0x4b, 0x2d, 0x00, 0x67, 0x00, 0x64, 0x00, 0x39,
			0x00, 0x37, 0x00, 0x65, 0x00, 0x63, 0x00, 0x38,
			0x00, 0x30, 0x00, 0x34, 0x00, 0x32, 0x00, 0x2d,
			0x00, 0x64, 0x00, 0x69, 0x00, 0x72, 0x00, 0x74,
			0x00, 0x8b, 0x79
		))
		yield from self.queue_packet((0xd2, ))
		yield from self.queue_packet((0x69, 0x32, 0xc0))

		# We have now tried to enqueue 160 bytes to the second-stage FIFO, overrunning it by 25 bytes.
		# Spin a few cycles to let the FIFOs all catch up
		yield from self.advance_cycles(50)

		# Now we can pop the packets and check that after 10 we get an overrun
		# marker and then a normal and happy packet
		yield from self.read_packet(3)
		yield from self.read_packet(11)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		yield from self.read_packet(35)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		yield from self.read_packet(35)
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		# Now we expect the overrun marker, which is a length of 65535 (invalid in normal USB traffic)
		yield from self.read_overrun_marker()
		# And finally we expect a good ACK packet following.
		yield from self.read_packet(1)
		yield from self.read_packet(3)
		self.assertEqual((yield self.dut.stream.valid), 0)

		# Having tested the second-stage FIFO, now lets overrun the first stage with a 1536 byte packet
		# (the first-stage FIFO can only handle 1027 bytes)
		yield from self.queue_packet(0xa5 for _ in range(1536))
		# Spin untill the FIFOs all catch up
		while (yield self.dut.stream.valid) == 0:
			yield
		yield from self.read_overrun_marker()
		# And finally let the second-stage FIFO state machine finish up
		yield from self.advance_cycles(1024)
		yield Settle()

	@usb_domain_test_case
	def test_fast_traffic(self):
		class PacketType:
			def __init__(self):
				self.reset()

			def reset(self):
				self.future = Future()
		packet_type = PacketType()

		def queue_packets():
			# Enable capture
			yield self.analyzer.capture_enable.eq(1)
			yield
			# Chew through the fast traffic entries
			for entry in self.fast_traffic:
				# Check if this is a wait point
				if isinstance(entry, dict):
					# Wait the indicated amount of time
					yield from self.wait(entry['wait'])
				else:
					# We now have a packet of data to queue
					yield from self.queue_packet(entry)
					packet_type.future.set_result(entry[0])
			packet_type.future.cancel()
			yield Settle()
			yield

		def process_packets():
			# While we should be chewing on packets
			while not packet_type.future.cancelled():
				# Look for a SOF packet
				while not packet_type.future.done():
					yield
				result = packet_type.future.result()
				packet_type.reset()
				if result != 0xa5:
					continue
				# Now we found a SOF, chew through any data in the packet buffer
				while (yield self.dut.stream.valid) == 1:
					yield self.dut.stream.ready.eq(1)
					yield
				yield self.dut.stream.ready.eq(0)
				yield

		generators = (queue_packets(), process_packets())
		try:
			while True:
				# Loop through the generators running each to its next clocking point
				for generator in generators:
					command = None
					# Run the generator to the next `yield` statement it contains
					while not isinstance(command, Tick):
						try:
							if command is not None:
								response = yield command
							else:
								response = None
						except Exception as error:
							generator.throw(error)
						else:
							command = generator.send(response)
							if command is None:
								command = Tick()
				# Clock the system
				yield
		except StopIteration:
			pass

class USBAnalyzerStackTest(SolGatewareTestCase):
	''' Test that evaluates a full-stack USB analyzer setup. '''

	SYNC_CLOCK_FREQUENCY = None
	USB_CLOCK_FREQUENCY = 60e6

	def instantiate_dut(self):
		from sol_usb.gateware.interface.ulpi import ULPIInterface, UTMITranslator

		self.ulpi = ULPIInterface()

		# Create a stack of our UTMITranslator and our USBAnalyzer.
		# We'll wrap the both in a module to establish a synthetic hierarchy.
		m = Module()
		m.submodules.translator = self.translator = UTMITranslator(ulpi = self.ulpi, handle_clocking = False)
		m.submodules.analyzer   = self.analyzer   = USBAnalyzer(utmi_interface = self.translator, mem_depth = 128)
		return m

	def initialize_signals(self):

		# Ensure the translator doesn't need to perform any register reads/writes
		# by default, so we can focus on packet Rx.
		yield self.translator.xcvr_select.eq(1)
		yield self.translator.dm_pulldown.eq(1)
		yield self.translator.dp_pulldown.eq(1)
		yield self.translator.use_external_vbus_indicator.eq(0)

	@usb_domain_test_case
	def test_simple_analysis(self):
		# Enable capture
		yield self.analyzer.capture_enable.eq(1)
		yield from self.advance_cycles(10)

		# Start a new packet.
		yield self.ulpi.dir.i.eq(1)
		yield self.ulpi.nxt.eq(1)

		# Bus turnaround packet.
		yield self.ulpi.data.i.eq(0x80)
		yield

		# Provide some data to be captured.
		for i in [0x2d, 0x00, 0x10]:
			yield self.ulpi.data.i.eq(i)
			yield

		# Mark our packet as complete.
		yield self.ulpi.dir.i.eq(0)
		yield self.ulpi.nxt.eq(0)
		yield

		# Wait for a few cycles, for realism.
		yield from self.advance_cycles(10)

		# Read our data out of the PHY.
		yield self.analyzer.stream.ready.eq(1)
		yield

		# Validate that we got the correct packet out; plus headers.
		for i in [0x00, 0x03, 0x2d, 0x00, 0x10]:
			self.assertEqual((yield self.analyzer.stream.payload), i)
			yield
