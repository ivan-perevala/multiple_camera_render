# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later


def register_handler(handlers: list, func, before=None) -> bool:
    if func not in handlers:
        if before is not None and before in handlers:
            index = handlers.index(before)
            handlers.insert(index, func)
        else:
            handlers.append(func)

        return True
    return False


def unregister_handler(handlers: list, func) -> bool:
    if func in handlers:
        handlers.remove(func)
        return True
    return False
