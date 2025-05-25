<!-- SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

SPDX-License-Identifier: GPL-3.0-or-later -->

# Icons

You would need ``blender_icons_geom.py`` from [Official Blender Repository](https://projects.blender.org/blender/blender/src/branch/main/release/datafiles/blender_icons_geom.py), see SPDX license specifier of it (its Apache-2.0, compatible with current GPLv3 project)

* ``default.blend`` contains icon source objects, should be updated according to [Blender ToolBar Icons](https://projects.blender.org/blender/blender-assets/src/branch/main/icons/toolbar.blend) file.
* ``generate.py`` - simplifies icon generation process. This script calls Blender (must be available in system's PATH) with call of  ``blender_icons_geom.py`` script with output to extension's directory.


It can be executed on Windows:

```powershell
py generate.py
```

other platforms have different python command line argument (eg. ```python3``` on Linux, etc.)
