<!-- SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

SPDX-License-Identifier: GPL-3.0-or-later -->

# Icons

* ``default.blend`` contains icon source objects. 
* ``blender_icons_geom.py`` is from [Official Blender Repository](https://projects.blender.org/blender/blender/src/branch/main/release/datafiles), see SPDX license specifier of it (its Apache-2.0, compatible with current GPLv3 project)
* ``generate.py`` - simplifies icon generation process. This script calls Blender (must be available in system's PATH) with call of  ``blender_icons_geom.py`` script with output to extension's directory.


It can be executed on Windows:

```powershell
py generate.py
```

other platforms have different python command line argument (eg. ```python3``` on Linux, ect.)
