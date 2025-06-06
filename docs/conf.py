# SPDX-License-Identifier: BSD-2-Clause

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))

from sol_usb import __version__ as sol_version

ROOT_DIR = (Path(__file__).parent).parent

project   = 'SOL'
version   = sol_version
release   = version.split('+')[0]
copyright = '2020 Great Scott Gadgets'
author    = 'Katherine J. Temkin'
language  = 'en'

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
	'sphinx.ext.extlinks',
	'sphinx.ext.githubpages',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'sphinx_inline_tabs',
	'myst_parser',
	'sphinx_copybutton',
]

source_suffix = {
	'.rst': 'restructuredtext',
	'.md': 'markdown',
}

extlinks = {
	'issue': ('https://github.com/shrine-maiden-heavy-industries/sol/issues/%s', 'sol/%s'),
	'pypi':  ('https://pypi.org/project/%s/', '%s'),
}

pygments_style         = 'default'
pygments_dark_style    = 'monokai'
autodoc_member_order   = 'bysource'
todo_include_todos     = True

intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'torii': ('https://torii.shmdn.link/', None),
	'torii_usb': ('https://torii-usb.shmdn.link/', None),
	'usb_construct': ('https://usb-construct.shmdn.link/', None)
}

napoleon_google_docstring              = False
napoleon_numpy_docstring               = True
napoleon_use_ivar                      = True
napoleon_use_admonition_for_notes      = True
napoleon_use_admonition_for_examples   = True
napoleon_use_admonition_for_references = True
napoleon_custom_sections  = [
	('Attributes', 'params_style'),
]

myst_heading_anchors = 3

templates_path = [
	'_templates',
]

html_baseurl     = 'https://sol.shmdn.link/'
html_theme       = 'furo'
html_copy_source = False

html_theme_options = {

}

html_static_path = [
	'_static'
]

html_css_files = [
	'css/styles.css'
]

linkcheck_retries = 2
linkcheck_workers = 1 # At the cost of speed try to prevent rate-limiting
linkcheck_ignore  = []
