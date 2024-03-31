# Multiple Camera Render

- [Multiple Camera Render](#multiple-camera-render)
  - [About](#about)
  - [How To Use the Addon](#how-to-use-the-addon)
  - [Release Notes](#release-notes)
  - [License](#license)


## About

Addon for [Blender](https://www.blender.org/) for sequential rendering from multiple cameras.

The addon was created for prototyping photogrammetric, photometric or volumetric captures of multiple-camera rigs.

It enables quick simulation of not only the location of the cameras, but also the selection of the desired lens, reproduction of inaccuracies from the real world (lens distortion, depth of field, chromatic aberration, etc.). That is, you can set up a scene and create a synthetic dataset for testing in your photogrammetry software.

Obviously, the addon can be used not only for these purposes, but also with any scenes where you need to render from several different cameras - this is also a good use case for it. 

An example of use can be the creation of render proxy [impostors](https://docs.unrealengine.com/en-US/Engine/Content/Tools/RenderToTextureTools/3/index.html) for Unity or Unreal.

## How To Use the Addon

Download the latest addon version from the [releases page](https://github.com/BlenderHQ/multiple_camera_render/releases/latest) and install it according to the [Blender manual](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons).

---

This means that you have a multi-camera scene, for example imported from photogrammetry software or manually created. After installing the addon, new options will appear in the render menu:

![image](https://github.com/BlenderHQ/multiple_camera_render/assets/16822993/3e69e667-2822-426e-9fd5-73d18b607592)

* `Use Multiple Camera Render` - Whether to use render from multiple cameras. If the flag is not active, rendering will take place in the usual way.
* `Use in Viewport` - When changing the current frame, changes will be displayed in the viewport. This does not affect the render file path, it will only show the order in which the cameras will be changed during rendering.

![mcr](https://github.com/BlenderHQ/multiple_camera_render/assets/16822993/763126a7-2522-4b1f-ad69-de07454e3d7c)

## Release Notes

<details open><summary>
<b>Version 3.6.3</b>
</summary>

* **This release changes the way the addon works.**
* 

</details>


<details open><summary>
<b>Version 3.0.0</b>
</summary>

Refactor of older versions of the addon, updated according to BlenderHQ addon standards. This release can be considered initial. It can be used to work with older versions of Blender (`2.80`-`3.6.0`). In new releases, the principle of the addon has been changed.

<!-- 
Download, install, design your multi camera rig layout. Define saving path for images and used settings. Setup composing if needed.
In addon UI press what type of render you want: Render all cams or only selected and their order. -->


</details>

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue)](https://www.gnu.org/licenses/gpl-3.0)

Copyright © 2020 Vladlen Kuzmin (ssh4), Ivan Perevala (ivpe).

<details><summary>
GNU GPL v3 License.
</summary>

```
Multiple Camera Render addon.
Copyright (C) 2020 Vladlen Kuzmin (ssh4), Ivan Perevala (ivpe)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

</details>
