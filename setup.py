#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-2-Clause

from setuptools import setup, find_packages
from pathlib    import Path

REPO_ROOT   = Path(__file__).parent
README_FILE = (REPO_ROOT / 'README.md')

def scm_version():
	def local_scheme(version):
		if version.tag and not version.distance:
			return version.format_with('')
		else:
			return version.format_choice('+{node}', '+{node}.dirty')
	return {
		'relative_to'   : __file__,
		'version_scheme': 'guess-next-dev',
		'local_scheme'  : local_scheme
	}

def doc_version():
	try:
		from setuptools_scm.git import parse as parse_git
	except ImportError:
		return ''

	git = parse_git('.')
	if not git:
		return ''
	elif git.exact:
		return git.format_with('v{tag}')
	else:
		return 'latest'

setup(
	name             = 'sol-usb',
	use_scm_version  = scm_version(),
	author           = 'Katherine Temkin',
	author_email     = 'k@ktemkin.com',
	maintainer       = ', '.join([
		'Aki Van Ness',
		'Rachel Mant',
	]),
	maintainer_email = ', '.join([
		'aki@lethalbit.net',
		'git@dragonmux.network',
	]),
	license          = 'BSD-3-Clause',
	description      = 'Torii HDL framework for FPGA-based USB solutions',
	python_requires  = '~=3.9',
	zip_safe         = True,
	url              = 'https://sol.shmdn.link/',

	long_description = README_FILE.read_text(),
	long_description_content_type = 'text/markdown',

	setup_requires   = [
		'wheel',
		'setuptools',
		'setuptools_scm',
	],

	install_requires = [
		'pyserial~=3.5',
		'pyvcd>=0.2.2,<0.4',
		'rich~=12.6.0',

		'usb-construct<1.0',
		'torii<1.0',
	],

	extras_require = {
		'dev': [
			'nox',
		],
		'platform': [
			'pyusb~=1.2.0',
			'libusb1~=1.9.2',
			'prompt-toolkit~=3.0.16',
			'ziglang~=0.8.0',
		]
	},

	packages         = find_packages(
		where   = '.',
		exclude = (
			'tests',
			'tests.*',
			'hardware',
			'examples',
			'examples.*',
			'applets',
			'applets.*',
		)
	),
	package_data      = {
		'sol_usb': [
			'py.typed'
		],
	},
	classifiers       = [
		'Development Status :: 4 - Beta',

		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Science/Research',

		'License :: OSI Approved :: BSD License',

		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',

		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',

		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
		'Topic :: Software Development',
		'Topic :: Software Development :: Embedded Systems',
		'Topic :: Software Development :: Libraries',
		'Topic :: System :: Hardware :: Universal Serial Bus (USB)',

		'Typing :: Typed',
	],

	project_urls     = {
		'Documentation': 'https://sol.shmdn.link/',
		'Source Code'  : 'https://github.com/shrine-maiden-heavy-industries/sol',
		'Bug Tracker'  : 'https://github.com/shrine-maiden-heavy-industries/sol/issues',
	},
)
