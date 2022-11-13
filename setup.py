# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, find_packages

def vcs_ver():
	def scheme(version):
		if version.tag and not version.distance:
			return version.format_with("")
		else:
			return version.format_choice("+{node}", "+{node}.dirty")
	return {
		"relative_to": __file__,
		"version_scheme": "guess-next-dev",
		"local_scheme": scheme
	}

setup(
	name            = 'sol',
	use_scm_version = vcs_ver(),
	author          = 'Katherine Temkin',
	author_email    = 'k@ktemkin.com',
	maintainer      = [
		'Aki Van Ness',
		'Rachel Mant',
	],
	maintainer_email= [
		'aki@lethalbit.net',
		'git@dragonmux.network',
	],
	license         = 'BSD-3-Clause',
	description     = 'Amaranth HDL framework for FPGA-based USB solutions',
	python_requires = '~=3.9',
	packages        = find_packages(),
	setup_requires  = [
		'wheel',
		'setuptools',
		'setuptools_scm',
	],

	install_requires = [
		'pyserial~=3.5',
		'pyvcd>=0.2.2,<0.4',

		'usb-construct @ git+https://github.com/shrine-maiden-heavy-industries/usb-construct@main',
		'amaranth @ git+https://github.com/amaranth-lang/amaranth.git@main',
		'amaranth-boards @ git+https://github.com/amaranth-lang/amaranth-boards.git@main',
		'amaranth-soc @ git+https://github.com/amaranth-lang/amaranth-soc.git@main',
		'amaranth-stdio @ git+https://github.com/amaranth-lang/amaranth-stdio.git@main',
	],

	extras_require = {
		'dev': [
			'tox~=3.22.0',
		],
		'soc': [
			'lambdasoc @ git+https://github.com/shrine-maiden-heavy-industries/lambdasoc.git@main',
			'minerva @ git+https://github.com/lambdaconcept/minerva.git',
		],
		'platform': [
			'pyusb~=1.2.0',
			'libusb1~=1.9.2',
			'apollo-fpga @ git+https://github.com/shrine-maiden-heavy-industries/apollo@main',
			'prompt-toolkit~=3.0.16',
			'ziglang~=0.8.0',
		]
	}
)
