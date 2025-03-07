# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of SOL.
#
# Copyright (c) 2020 Great Scott Gadgets <info@greatscottgadgets.com>

''' Request components shared between USB2 and USB3. '''

from torii.hdl     import Record, Signal
from torii.hdl.rec import Direction

class SetupPacket(Record):
	''' Record capturing the content of a setup packet.

	Components (O = output from setup parser; read-only input to others):
		O: received      -- Strobe; indicates that a new setup packet has been received,
							and thus this data has been updated.

		O: is_in_request -- High if the current request is an 'in' request.
		O: type[2]       -- Request type for the current request.
		O: recipient[5]  -- Recipient of the relevant request.

		O: request[8]    -- Request number.
		O: value[16]     -- Value argument for the setup request.
		O: index[16]     -- Index argument for the setup request.
		O: length[16]    -- Length of the relevant setup request.
	'''

	# Byte 1
	recipient: Signal[5, Direction.FANOUT]
	type: Signal[2, Direction.FANOUT]
	is_in_request: Signal[1, Direction.FANOUT]

	# Byte 2
	request: Signal[8, Direction.FANOUT]

	# Byte 3/4
	value: Signal[16, Direction.FANOUT]

	# Byte 5/6
	index: Signal[16, Direction.FANOUT]

	# Byte 7/8
	length: Signal[16, Direction.FANOUT]

	# Control signaling.
	received: Signal[1, Direction.FANOUT]
