#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause
from sol_usb.gateware.applets.analyzer import (
	USBAnalyzerConnection, USB_SPEED_LOW, USB_SPEED_FULL, USB_SPEED_HIGH
)
from argparse import ArgumentParser
from pathlib import Path
from construct import (
	this,
	Struct, Switch, Computed, If, RepeatUntil, Rebuild,
	BitStruct, BitsInteger,
	Hex, Enum, Int8ul, Int16ul, Int32ul, Int64ul, Int64sl, Bytes,
	CString, PaddedString, HexDump, Check, Default, GreedyRange,
	Const, Aligned, Pass, len_, Probe
)
from arrow import Arrow
from datetime import datetime
from construct_typed import Context
from typing import BinaryIO
from usb.core import USBError

SPEEDS = {
	'high': USB_SPEED_HIGH,
	'full': USB_SPEED_FULL,
	'low':  USB_SPEED_LOW
}

blockType = 'Block Type' / Enum(Int32ul,
	sectionHeader = 0x0A0D0D0A,
	interface = 0x00000001,
	interfaceStats = 0x00000005,
	enhancedPacket = 0x00000006,
)

optionType = 'Option Type' / Enum(Int16ul,
	end = 0x0000,
	comment = 0x0001,
)

linkType = 'Link Type' / Enum(Int16ul,
	usbFreeBSD = 186,
	usbLinux = 189,
	usbLinuxMemMapped = 220,
	usbPcap = 249,
	usbDarwin = 266,
	openVizsla = 278,
	usb2_0 = 288,
)

epoch = Arrow(1970, 1, 1)

def timestampFromRaw(this: Context):
	value = (this.Raw.High << 32) + this.Raw.Low
	return epoch.shift(seconds = value * 1e-6)

def timestampToRaw(this: Context):
	from datetime import timedelta
	timestamp = this.Value
	# For now assume that if the object is not an Arrow datetime, it's standard library one
	if not isinstance(timestamp, Arrow):
		timestamp = Arrow.fromdatetime(timestamp)
	value: timedelta = timestamp - epoch
	value = int(value.total_seconds() * 1e6)
	return {'Low': value & 0xffffffff, 'High': value >> 32}

timestamp = 'Timestamp' / Struct(
	'Raw' / Rebuild(Struct(
		'High' / Hex(Int32ul),
		'Low' / Hex(Int32ul),
	), timestampToRaw),
	'Value' / Computed(timestampFromRaw),
)

optionValue = Aligned(4, Switch(
	this.Code,
	{
		optionType.end: Pass,
		optionType.comment: PaddedString(this.Length, 'utf8'),

		0x0002: Switch(this._.Type,
			{
				blockType.sectionHeader: PaddedString(this.Length, 'utf8'), # shb_hardware
				blockType.interface: PaddedString(this.Length, 'utf8'), # if_name
				blockType.enhancedPacket: BitStruct( # epb_flags
					'direction' / BitsInteger(2),
					'recept_type' / BitsInteger(3),
					'fcs_len' / BitsInteger(4),
					'reserved' / BitsInteger(7),
					'll_errors' / BitsInteger(16),
				),
				blockType.interfaceStats: timestamp, # isb_starttime
			},
			HexDump(Bytes(this.Length))
		),
		0x0003: Switch(this._.Type,
			{
				blockType.sectionHeader: PaddedString(this.Length, 'utf8'), # shb_os
				blockType.interface: PaddedString(this.Length, 'utf8'), # if_description
				blockType.enhancedPacket: Bytes(this.Length), # epb_hash
				blockType.interfaceStats: timestamp, # isb_endtime
			},
			HexDump(Bytes(this.Length))
		),
		0x0004: Switch(this._.Type,
			{
				blockType.sectionHeader: PaddedString(this.Length, 'utf8'), # shb_userappl
				blockType.interface: Struct( # if_IPv4addr
					'address' / Hex(Bytes(4)),
					'mask' / Hex(Bytes(4)),
				),
				blockType.enhancedPacket: Int64ul, # epb_dropcount
				blockType.interfaceStats: Hex(Int64ul), # isb_ifrecvoptionValue
			},
			HexDump(Bytes(this.Length))
		),
		0x0009: Switch(this._.Type,
			{
				blockType.interface: Int8ul, # if_tsresol
			},
			HexDump(Bytes(this.Length))
		),
		0x000c: Switch(this._.Type,
			{
				blockType.interface: PaddedString(this.Length, 'utf8'), # if_os
			},
			HexDump(Bytes(this.Length))
		),
	},
	HexDump(Bytes(this.Length)),
))

def optionLen(this: Context) -> int:
	if isinstance(this.Value, str):
		value = CString('utf8').build(this.Value, **this)[:-1]
	else:
		value = optionValue.build(this.Value, **this)
	return len(value)

option = 'Option' / Struct(
	'Code' / Hex(optionType),
	'Length' / Rebuild(Int16ul, optionLen),
	'Value' / If(this.Length > 0, optionValue)
)

sectionHeaderBlock = 'Section Header' / Struct(
	'BOM' / Hex(Const(0x1A2B3C4D, Int32ul)),
	'Version' / Struct(
		'Major' / Const(1, Int16ul),
		'Minor' / Const(0, Int16ul),
	),
	'Section Len' / Default(Int64sl, -1),
)

interfaceBlock = 'Interface Header' / Struct(
	'LinkType' / Hex(linkType),
	'Reserved' / Hex(Const(0, Int16ul)),
	'SnapLen' / Int32ul,
)

def packetDataLen(this: Context):
	# Handle initial parse phase
	if hasattr(this, 'CapturedLen'):
		return this.CapturedLen
	# Handle sizeof() calculation phase
	elif hasattr(this._.Data, 'CapturedLen'):
		return this._.Data.CapturedLen
	# Handle build phase
	return len(this._.Data['PacketData'])

enhancedPacketBlock = 'Enhanced Packet' / Aligned(4, Struct(
	'InterfaceID' / Hex(Int32ul),
	'Timestamp' / timestamp,
	'CapturedLen' / Rebuild(Int32ul, len_(this.PacketData)),
	'ActualLen' / Int32ul,
	'PacketData' / HexDump(Bytes(lambda this: packetDataLen(this))),
))

interfaceStatisticsBlock = 'Interface Statistics' / Struct(
	'InterfaceID' / Hex(Int32ul),
	'TimestampRaw' / Struct(
		'High' / Hex(Int32ul),
		'Low' / Hex(Int32ul)
	),
)

optionsBlock = RepeatUntil(
	lambda obj, _, __: obj['Code'] == optionType.end,
	option
)

def blockLen(this: Context) -> int:
	if not this._building:
		optionsLen = len(optionsBlock.build(this.Options, **this))
	else:
		# Special case to handle the building phase *grumbles*
		if this.Options is None:
			optionsLen = 0
		else:
			optionsLen = len(optionsBlock.build(this.Options, **this))

	return (
		this._subcons.Type.sizeof(**this) +
		this._subcons.Data.sizeof(**this) +
		optionsLen +
		Int32ul.sizeof() * 2
	)

def optionsLen(this: Context) -> int:
	return this.Length1 - (
		this._subcons.Type.sizeof(**this) +
		this._subcons.Data.sizeof(**this) +
		Int32ul.sizeof() * 2
	)

pcapngBlock = 'Block' / Struct(
	'Type' / Hex(blockType),
	'Length1' / Rebuild(Int32ul, blockLen),
	'Data' / Switch(
		this.Type, {
			blockType.sectionHeader: sectionHeaderBlock,
			blockType.interface: interfaceBlock,
			blockType.enhancedPacket: enhancedPacketBlock,
			# blockType.interfaceStats: interfaceStatisticsBlock,
		},
	),
	'Size' / Computed(lambda this: this._subcons.Data.sizeof(**this)),
	'Options' / If(lambda this: optionsLen(this) > 0, optionsBlock),
	'Length2' / Rebuild(Int32ul, this.Length1),
	Check(this.Length1 == this.Length2),
)

pcapng = 'pcapng' / GreedyRange(pcapngBlock)

def writePcapngHeaders(file: BinaryIO):
	from platform import uname
	hostSystem = uname()

	# Build the section header that defines the start of the pcapng file
	file.write(
		pcapngBlock.build(
		{
			'Type': blockType.sectionHeader,
			'Data': {},
			'Options':
			[
				# Should try and build shb_hardware (0x0002), but this is very difficult in Python.
				{
					# shb_os
					'Code': 0x0003,
					'Value': f'{hostSystem.system} {hostSystem.release}'
				},
				{
					# shb_userappl
					'Code': 0x0004,
					'Value': 'sol_usb USB Analyzer applet'
				},
				{
					'Code': optionType.end,
					'Value': None
				}
			]
		})
	)

	# Now build the interface header
	file.write(
		pcapngBlock.build(
		{
			'Type': blockType.interface,
			'Data':
			{
				'LinkType': linkType.usb2_0,
				# This defines the maximum size of any packet in the capture.
				# For USB 2.0, this gives a size of 8192 bytes in a data frame + 3 bytes for the PID and CRC16
				'SnapLen': 8195
			},
			'Options':
			[
				{
					# if_name
					'Code': 0x0002,
					'Value': 'LUNA'
				},
				{
					# if_tsresol
					'Code': 0x0009,
					'Value': 6
				},
				{
					# if_os
					'Code': 0x000c,
					'Value': f'{hostSystem.system} {hostSystem.release}'
				},
				{
					'Code': optionType.end,
					'Value': None
				}
			]
		})
	)

def writePcapngPacket(file: BinaryIO, packet: bytearray, timestamp: datetime):
	file.write(
		pcapngBlock.build(
		{
			'Type': blockType.enhancedPacket,
			'Data':
			{
				'InterfaceID': 0,
				'Timestamp': {'Value': timestamp},
				'ActualLen': len(packet),
				'PacketData': packet
			},
			'Options': None
		})
	)

def main():
	parser = ArgumentParser(description = 'Simple USB traffic capture engine')
	parser.add_argument(
		'--speed', dest = 'capture_speed', default = 'high', choices = SPEEDS.keys(),
		help = 'The speed of the USB data to capture.'
	)
	parser.add_argument(
		'--filename', dest = 'filename', default = Path('capture.pcapng'), type = Path,
		help = 'The pcapng file to write the captured data to (defaults to capture.pcapng)'
	)
	args = parser.parse_args()

	fileName = Path(args.filename)
	with fileName.open('wb') as file:
		writePcapngHeaders(file)

		analyzer = USBAnalyzerConnection()
		analyzer.build_and_configure(SPEEDS.get(args.capture_speed, USB_SPEED_HIGH))
		analyzer.start_capture()

		try:
			while True:
				packet, timestamp, _ = analyzer.read_raw_packet()
				writePcapngPacket(file, packet, timestamp)
		except USBError:
			pass

	print('Capture complete')

if __name__ == '__main__':
	main()
