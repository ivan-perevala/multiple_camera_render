<!--
SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Building the documentation

Please, make sure you have [requirements.txt](../requirements.txt) installed to build this documentation.

Jump into docs directory like this:

```sh
cd docs
```

So the command to build:
```sh
sphinx-build -M html "." "_build"
```

To create `.pot` files for localization run:

```sh
sphinx-build -M gettext "" "_build"
```

To create localization `.po` files use the command (change `-l` argument as needed):

```sh
sphinx-intl update -p _build/gettext -l uk
```

# Notes about this documentation maintenance

Some of the files are reused between different projects, so they should be changed and maintained carefully:

* This file.
* [links.inc](links.inc) file contains links to current Blender Python API.
* [conf.py](conf.py) Sphinx configuration file which should be changed as little as possible. It was designed to reuse data from project's [pyproject.toml](../pyproject.toml) file, so change it only where is no other choice.
