..  SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>

..  SPDX-License-Identifier: GPL-3.0-or-later

Conflicts
=========

Extension can conflict with other extensions. The reason for this is lays in how Blender API was designed: different extensions can register its functionality to the same Blender handlers. This situation is hard to predict, as far as there is a wide variety of extensions available.

Known issues:
*************

* **Individual Camera Properties** - functionality is untested addons can't work in pair.
* **Auto Active Camera Switcher** - blocks camera from switching which leads to rendering same camera over and over again.

Why is it not handled?
**********************

Multiple Camera Render version 4.3.0 was the only version which was able to handle those situations and guaranteed that the addon would work as expected. Unfortunately, this version got an anonymous report on Blender Extensions platform, so in order to make Multiple Camera Render available again it was mandatory to remove this functionality in its entirety. 

What does it mean for me?
*************************

That means that you can use Multiple Camera Render with other extensions, but you should be aware of the fact that some functionality may not work as expected. If you encounter any issues, please report them to the addon developer so they can be addressed in future updates.
If you are a developer of an extension and you want to make sure that your extension works with Multiple Camera Render, please test it with the latest version of the addon and report any issues you encounter.
