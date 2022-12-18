# SPDX-License-Identifier: BSD-3-Clause

import logging         as log
from argparse          import ArgumentParser, Namespace
from os                import getenv
from pathlib           import Path
from shutil            import rmtree
from sys               import argv, exit
from tempfile          import mkdtemp
from typing            import Any, Optional, Callable, Union

from rich              import traceback
from rich.logging      import RichHandler

from torii.hdl._unused import MustUse
from torii.hdl.ir      import Fragment

__all__ = (
	'cli',
	'setup_logger',
)

def setup_logger(args: Optional[Namespace] = None) -> None:
	level = log.INFO
	if args is not None and args.verbose:
		level = log.DEBUG

	traceback.install()
	log.basicConfig(
		force    = True,
		format   = '%(message)s',
		datefmt  = '[%X]',
		level    = level,
		handlers = [
			RichHandler(rich_tracebacks = True, show_path = True)
		]
	)

def cli(
	fragment: Union[Fragment, Callable[..., Fragment]], *pos_args,
	cli_soc: Optional[Any] = None,
	**kwargs
) -> Optional[Fragment]:
	'''
	Runs a default CLI that assists in building and running gateware.

		If the user's options resulted in the board being programmed, this returns the fragment
		that was programmed onto the board. Otherwise, it returns None.

	Parameters
	----------
	fragment : Union[torii.hdl.ir.Fragment, Callable[..., torii.hdl.ir.Fragment]]
		The fragment instance to be built; or a callable that returns a fragment,
		such as a Elaborable type. If the latter is provided, any keyword or positional
		arguments not specified here will be passed to this callable.

	pos_args :
		Arguments to pass to ``fragment`` if it is a Callable[..., torii.hdl.ir.Fragment].

	cli_soc
		Optional. If a SoC design provides a SimpleSoc, options will be provided for generating
		build artifacts, such as header or linker files; instead of elaborating a design.
	'''

	from .gateware.platform import get_appropriate_platform

	name = fragment.__name__ if callable(fragment) else fragment.__class__.__name__

	parser = ArgumentParser(
		description = f'Gateware generation/upload script for \'{name}\' gateware.'

	)

	parser.add_argument(
		'--output', '-o',
		metavar = 'filename',
		type    = Path,
		help    = 'Build and output a bitstream to the given file.'
	)
	parser.add_argument(
		'--erase', '-E',
		action  = 'store_true',
		default = False,
		help    = 'Clears the relevant FPGA\'s flash before performing other options.'
	)
	parser.add_argument(
		'--upload', '-U',
		action  = 'store_true',
		default = False,
		help    = 'Uploads the relevant design to the target hardware. Default if no options are provided.'
	)
	parser.add_argument(
		'--flash', '-F',
		action  = 'store_true',
		default = False,
		help    = 'Flashes the relevant design to the target hardware\'s configuration flash.'
	)
	parser.add_argument(
		'--dry-run', '-D',
		action  = 'store_true',
		default = False,
		help    = 'When provided as the only option; builds the relevant bitstream without uploading or flashing it.'
	)
	parser.add_argument(
		'--keep-files',
		action  = 'store_true',
		default = False,
		help    = 'Keeps the local files in the default `build` folder.'
	)
	parser.add_argument(
		'--fpga',
		metavar = 'part_number',
		type    = str,
		help    = 'Overrides build configuration to build for a given FPGA. Useful if no FPGA is connected during build.'
	)
	parser.add_argument(
		'--console',
		metavar = 'port',
		type    = Path,
		help    = 'Attempts to open a convenience 115200 8N1 UART console on the specified port immediately after uploading.'
	)

	# If we have SoC options, print them to the command line.
	if cli_soc:
		parser.add_argument(
			'--generate-c-header',
			action  = 'store_true',
			default = False,
			help    = 'Print the C header file for this design\'s SoC will to stdout then exit.'
		)
		parser.add_argument(
			'--generate-ld-script',
			action  = 'store_true',
			default = False,
			help    = 'Print the linker script for design\'s SoC memory regions to stdout then exit.'
		)
		parser.add_argument(
			'--get-fw-address',
			action  = 'store_true',
			default = False,
			help    = 'Print the address firmware should be loaded at to stdout then exit.'
		)


	# Disable UnusedElaboarable warnings until we decide to build things.
	# This is sort of cursed, but it keeps us categorically from getting UnusedElaborable warnings
	# if we're not actually buliding.
	MustUse._MustUse__silence = True

	args = parser.parse_args()

	setup_logger(args)

	# If this isn't a fragment directly, interpret it as an object that will build one.
	if callable(fragment):
		fragment = fragment(*pos_args, **kwargs)

	# If we have no other options set, build and upload the relevant file.
	if (args.output is None and not all((args.flash, args.erase, args.dry_run))):
		args.upload = True

	# Once the device is flashed, it will self-reconfigure, so we
	# don't need an explicitly upload step; and it implicitly erases
	# the flash, so we don't need an erase step.
	if args.flash:
		args.erase = False
		args.upload = False


	# If we've been asked to generate a C header, generate -only- that.
	if cli_soc and args.generate_c_header:
		cli_soc.generate_c_header(platform_name = get_appropriate_platform().name)
		exit(0)

	# If we've been asked to generate linker region info, generate -only- that.
	if cli_soc and args.generate_ld_script:
		cli_soc.generate_ld_script()
		exit(0)

	if cli_soc and args.get_fw_address:
		print(f'0x{cli_soc.main_ram_address():08x}')
		exit(0)

	# Build the relevant gateware, uploading if requested.
	build_dir = 'build' if args.keep_files else mkdtemp()

	# Build the relevant files.
	try:
		platform = get_appropriate_platform()

		# If we have a toolchain override, apply it to our platform.
		toolchain = getenv('SOL_TOOLCHAIN')
		if toolchain:
			platform.toolchain = toolchain

		if args.fpga:
			platform.device = args.fpga

		if args.erase:
			log.info('Erasing flash...')
			platform.toolchain_erase()
			log.info('Erase complete.')

		join_text = 'and uploading gateware to attached' if args.upload else 'for'
		log.info(f'Building {join_text} {platform.name}...')

		# If we have an SoC, allow it to perform any pre-elaboration steps it wants.
		# This allows it to e.g. build a BIOS or equivalent firmware.
		if cli_soc and hasattr(cli_soc, 'build'):
			cli_soc.build(build_dir = build_dir)


		# Now that we're actually building, re-enable Unused warnings.
		MustUse._MustUse__silence = False
		products = platform.build(fragment, do_program = args.upload, build_dir = build_dir)

		log.info(f'{"Upload" if args.upload else "Build"} complete.')

		# If we're flashing the FPGA's flash, do so.
		if args.flash:
			log.info('Programming flash...')
			platform.toolchain_flash(products)
			log.info('Programming complete.')

		# If we're outputting a file, write it.
		if args.output:
			bitstream = products.get('top.bit')
			with args.output.open('wb') as f:
				f.write(bitstream)

		# If we're expecting a console, open one.
		if args.console:
			import serial.tools.miniterm

			# Clear our arguments, so they're not parsed by miniterm.
			del argv[1:]

			# Run miniterm with our default port and baudrate.
			serial.tools.miniterm.main(default_port = args.console, default_baudrate = 115200)

		# Return the fragment we're working with, for convenience.
		if args.upload or args.flash:
			return fragment

	# Clean up any directories we've created.
	finally:
		if not args.keep_files:
			rmtree(build_dir)
