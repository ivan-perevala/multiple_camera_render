..  SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

..  SPDX-License-Identifier: GPL-3.0-or-later

Conflicts
=========

Extension can conflict with other extensions. The reason for this is lays in how Blender API was designed: different extensions can register its functionality to the same Blender handlers. This situation is hard to predict, as far as there is a wide variety of extensions available.

How is it handled?
------------------

* User would be notified about conflicts in user interface:
