@REM SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

@REM SPDX-License-Identifier: GPL-3.0-or-later

@echo off
setlocal

REM Save the original directory
set "ORIGINAL_DIR=%cd%"
set "WHEEL_DIR=%ORIGINAL_DIR%\src\multiple_camera_render\wheels"

REM Change directory to ../lib/
cd /d "%~dp0..\lib"

REM Build wheels for each local library without dependencies
for %%D in (lib_bhqui lib_bhqrprt lib_bhqmain) do (
    echo Building wheel for %%D...
    cd "%%D"
    py -m pip wheel . --no-deps --wheel-dir="%WHEEL_DIR%"
    cd ..
)

REM Return to the original directory
cd /d "%ORIGINAL_DIR%"

REM Build Blender extension from the original directory
blender --command extension build --source-dir ./src/multiple_camera_render/ --output-dir ./build