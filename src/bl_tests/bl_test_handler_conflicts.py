# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later


def test_handler_conflicts(
    multiple_camera_render_module,
    test_handler_conflict_multilevel_module,
    test_handler_conflict_one_level_module,
    test_handlers_conflict_from_lib_module,
    handlers_conflict_module,
):
    # Check that all modules are loaded correctly. If any of these modules are not found, the test will fail.
    # Probably, test suite was not installed correctly.
    assert multiple_camera_render_module is not None
    assert test_handler_conflict_multilevel_module is not None
    assert test_handler_conflict_one_level_module is not None
    assert test_handlers_conflict_from_lib_module is not None
    assert handlers_conflict_module is not None

    conflicting_addons, conflicting_modules = multiple_camera_render_module.check_handlers_conflicts()

    # Than there is guaranteed that there is no duplicates.
    assert isinstance(conflicting_addons, set)
    assert isinstance(conflicting_modules, set)

    # Check that all test addons are in the conflicting addons.
    assert test_handler_conflict_multilevel_module in conflicting_addons
    assert test_handler_conflict_one_level_module in conflicting_addons
    assert test_handlers_conflict_from_lib_module not in conflicting_addons, "There is no way to test because it only loads handlers from the library"

    # Check module names in the conflicting modules.

    module_names = []
    for module in conflicting_modules:
        name_split = module.__name__.split(".")
        if name_split[0] == handlers_conflict_module.__name__:
            module_names.append(module.__name__)

    module_names.sort()

    expected_module_names = [
        'handlers_conflict.handlers.composite',
        'handlers_conflict.handlers.depsgraph.dg',
        'handlers_conflict.handlers.playback',
        'handlers_conflict.handlers.render',
        'handlers_conflict.handlers.scene_frame'
    ]

    assert module_names == expected_module_names
