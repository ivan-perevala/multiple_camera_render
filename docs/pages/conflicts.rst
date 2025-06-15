..  SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

..  SPDX-License-Identifier: GPL-3.0-or-later

Conflicts
=========

Extension can conflict with other extensions. The reason for this is lays in how Blender API was designed: different extensions can register its functionality to the same Blender handlers. This situation is hard to predict, as far as there is a wide variety of extensions available.

How is it handled?
------------------

User would be notified about conflicts in user interface. If conflict is detected, a new button will appear in top of Multiple Camera Render section of Render Menu:

.. image:: https://raw.githubusercontent.com/ivan-perevala/multiple_camera_render/main/.github/images/conflict_warn_v422.webp
    :alt: Conflict Warning
    :align: center


This button will open extensions preferences, where you can see information about conflicting addons:


.. image:: https://raw.githubusercontent.com/ivan-perevala/multiple_camera_render/main/.github/images/conflicting_addons_v422.webp
    :alt: Conflicting Addons
    :align: center

At this point you can disable conflicting addons, or just ignore the warning.

.. note::
    It is recommended to disable conflicting addons.

What would happen if you ignore the warning?
--------------------------------------------

If you ignore the warning, Multiple Camera Render will still work, but there is not guarantee that other addons will function correctly. The idea is that when you would start any of Multiple Camera Render operators it would temporarily remove conflicting functions from Blender handlers, so Multiple Camera Render can work correctly. But this may lead to unexpected behavior of other addons, as they would not be able to use their functionality while Multiple Camera Render is running.

