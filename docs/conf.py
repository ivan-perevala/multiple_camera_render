# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import sys
from pathlib import Path
import tomllib

CURRENT_DIR = Path(os.path.dirname(__file__))

# Make module available in path
sys.path.append(str((CURRENT_DIR / "../src/").resolve()))

# Reuse data from "../pyproject.toml" file instead of writing it directly
with open((CURRENT_DIR / "../pyproject.toml").resolve(), 'rb') as pyproject_file:
    pyproject = tomllib.load(pyproject_file)

project = pyproject["project"]["name"]
copyright = ','.join(
    f"{author_info['name']} ({author_info['email']})"
    for author_info
    in pyproject["project"]["authors"]
)
version = pyproject["project"]["version"]

extensions = [
    "sphinx.ext.coverage",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    '.md': 'markdown',
}
master_doc = 'index'

exclude_patterns = [
    "*.md",
]

autodoc_member_order = "bysource"
autodoc_mock_imports = []

autodoc_typehints_format = 'short'
autodoc_typehints = 'none'

language = "en"
locale_dirs = ['locale/']
gettext_compact = True
gettext_location = False

napoleon_google_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True

html_theme = "furo"
html_static_path = ["_static"]
html_templates_path = ["_templates"]
html_favicon = "_static/favicon.ico"
html_title = pyproject['project']['description']
html_logo = "_static/mcr-logo.webp"

html_css_files = [
    'mcr.css',
]

# https://pradyunsg.me/furo/customisation/
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "black",
    },

    "dark_css_variables": {
        "color-brand-primary": "white",
    },
}
