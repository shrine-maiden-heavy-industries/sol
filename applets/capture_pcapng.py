#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause

from argparse                          import ArgumentParser
from pathlib                           import Path
from platform                          import uname

from usb.core                          import USBError

from sol_usb._pcapng                   import LinkType, PcapngStream, OptionType
from sol_usb.gateware.applets.analyzer import USB_SPEED_FULL, USB_SPEED_HIGH, USB_SPEED_LOW, USBAnalyzerConnection

SPEEDS = {
	'high': USB_SPEED_HIGH,
	'full': USB_SPEED_FULL,
	'low':  USB_SPEED_LOW
}

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

	hostSystem = uname()

	analyzer = USBAnalyzerConnection()
	analyzer.build_and_configure(SPEEDS.get(args.capture_speed, USB_SPEED_HIGH))

	with PcapngStream(fileName) as stream:
		stream.emit_header(
			hardware = '', writer = 'sol_usb USB Analyzer applet', os = f'{hostSystem.system} {hostSystem.release}'
		)
		interface = stream.emit_interface(
			LinkType.USB2_0, name = 'LUNA', snap_len = 8195, options = [
				{ 'type': OptionType.IF_TSRESOL, 'value': 6 }
			]
		)

		analyzer.start_capture()

		try:
			while True:
				packet, timestamp, _ = analyzer.read_raw_packet()
				interface.emit_packet(packet, timestamp)
		except USBError:
			pass

	print('Capture complete')

if __name__ == '__main__':
	main()
