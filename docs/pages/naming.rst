..  SPDX-FileCopyrightText: 2024 Ivan Perevala <ivan95perevala@gmail.com>

..  SPDX-License-Identifier: GPL-3.0-or-later

Naming Conventions
==================

Here would be described how addon handles output file names.

.. seealso::

    The key here is ``Output > File Path`` option. The addon will use the same output behaviour as Blender does, but with slight modifications:
    `docs.blender.org/manual/en/latest/render/output/properties <https://docs.blender.org/manual/en/latest/render/output/properties/output.html#output>`_


Animation
---------

For rendering animations, it depends on the output file format. If output is video format (e.g. ``FFmpeg video``), the addon will use the same output file name as Blender does, but with the camera name appended to it. If the output is image format (e.g. ``PNG``), the addon will use pattern described below, for sequential rendering, but with the camera name appended to it.

Sequential Rendering
--------------------

In examples below, we would assume that we have a scene with a cameras named ``Camera`` and ``Camera.001``:

* If no output file name is specified (``//`` in this example), the addon will use the camera name as part of the output file name:
    - With ``Keep Frame Number`` option disabled:
        - ``Camera.png``
        - ``Camera.001.png``
        - ``<camera_name_full>.<ext>``

    - With ``Keep Frame Number`` option enabled:
        - ``Camera0001.png``
        - ``Camera.0010001.png``
        - ``<camera_name_full><frame_number>.<ext>``

* If the output file name is specified (``Prefix`` in this example), the addon will use it as is, but with the camera name appended to it:
    - With ``Keep Frame Number`` option disabled:
        - ``Prefix_Camera.png``
        - ``Prefix_Camera.001.png``
        - ``<prefix>_<camera_name_full>.<ext>``

    - With ``Keep Frame Number`` option enabled:
        - ``Prefix_Camera0001.png``
        - ``Prefix_Camera.0010001.png``
        - ``<prefix>_<camera_name_full><frame_number>.<ext>``

* If the output file name is specified with padding (``Prefix_##_Suffix`` in this example), frame number will be placed in the padding part:
    - With ``Keep Frame Number`` option disabled:
        - ``Prefix_##_Suffix_Camera.png``
        - ``Prefix_##_Suffix_Camera.001.png``
        - ``<filename>_<camera_name_full>.<ext>``

    - With ``Keep Frame Number`` option enabled:
        - ``Prefix_01_Suffix_Camera.png``
        - ``Prefix_01_Suffix_Camera.001.png``
        - ``<prefix><frame_number_padded><suffix>_<camera_name_full>.<ext>``

Frame Number
------------

For sequentional rendering of images, by default Blender will not write frame number even if the padding is specified. If this case you can enable ``Keep Frame Number`` option in the addon render settings. That does not apply to animation rendering, where frame number is always written.
