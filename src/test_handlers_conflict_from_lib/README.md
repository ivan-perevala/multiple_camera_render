<!--
SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Test Handler Conflict From Library

This is more complicated test case. Some of handlers are possibly registered in libraries, so this also need to be covered.

Directory ```wheels/src/lib_handlers_conflict``` contains source files of tested library, which need to be build.

It can be done from project root directory like that:

```powershell
py -m pip wheel "src\test_handlers_conflict_from_lib\wheels\lib_handlers_conflict" --wheel-dir "src\test_handlers_conflict_from_lib\wheels"
```
