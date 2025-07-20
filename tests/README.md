<!-- SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

SPDX-License-Identifier: GPL-3.0-or-later -->

# Tests

Tests are long running because they involve actual rendering, so they are supposed to be run before release.

Examples of tests for different Blender versions on Windows:

```powershell
pytest --blender="C:/Program Files/Blender Foundation/Blender 4.2/blender.exe" --repo=user_default
pytest --blender="C:/Program Files/Blender Foundation/Blender 4.3/blender.exe" --repo=user_default
pytest --blender="C:/Program Files/Blender Foundation/Blender 4.4/blender.exe" --repo=user_default
pytest --blender="C:/Program Files/Blender Foundation/Blender 4.5/blender.exe" --repo=user_default
pytest --blender="C:/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe" --repo=user_default
```

* You would need pytest installed.
* Tested Blender version needs to have addon installed and enabled.
* Blender executable might be available on PATH, you don't need `--blender` argument in that case.
* For CI/CD platforms, added `--background-only` option. This would skip all tests which are not in background mode.

> [!NOTE]
> Avoid datasets with any other renderer than Cycles in CPU mode for test files. Workbench does not work with no display so it will not be compatible with GitHub Actions testing.
