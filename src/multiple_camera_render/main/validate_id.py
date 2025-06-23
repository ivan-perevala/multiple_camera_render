# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import ID, Object


def validate_id(id: None | ID) -> bool:
    """Validate id data block is not None and not deleted.

    :param id: ID data block.
    :type id: None | ID
    :return: Valid state.
    :rtype: bool
    """

    if id is None:
        return False

    try:
        getattr(id, "name_full")
    except ReferenceError:
        return False
    else:
        return True


def validate_camera_object(ob: None | Object) -> bool:
    """Validate object is not None or deleted and is camera.

    :param ob: Object to check.
    :type ob: None | Object
    :return: Valid state.
    :rtype: bool
    """

    if validate_id(ob):
        return 'CAMERA' == ob.type
    return False
