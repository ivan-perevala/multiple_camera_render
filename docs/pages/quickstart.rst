Quick Start
===========

This would be a quick user guide to get started with the addon.

For example, you have a scene with multiple cameras and you want to render all of them. In this example, we will use
a photogrammetry scene captured in Warszaw, Poland. It has 62 cameras and I want to render all of them from the same
angle they was captured in real world, but with different lighting.

.. image::
    https://raw.githubusercontent.com/ivan-perevala/multiple_camera_render/main/.github/images/general.png
    :alt: Example scene
    :width: 100%

Rendering all cameras would be time consuming, so first I would like to preview how it would look like. To do that, I
will use the addon preview feature. I will open ``Render`` menu and press ``Preview`` button.

.. image::
    https://raw.githubusercontent.com/ivan-perevala/multiple_camera_render/main/.github/images/camera_order.gif
    :alt: Preview
    :width: 100%

As far as I am satisfied with the preview, I can start rendering. I will open ``Render`` menu and press
``Multiple Camera Render`` button.

After that, actual rendering will start. The addon will render all cameras one by one, and once the rendering is finished,
the rendered images will be saved to the output directory.

.. image::
    https://raw.githubusercontent.com/ivan-perevala/multiple_camera_render/main/.github/images/output-files.png
    :alt: Rendering
    :width: 100%

As you can see, names of the rendered images are based on the camera names, so you can easily identify which image
belongs to which camera.

If you want to render animations, you can do that as well. Just select the cameras you want to render and press
``Multiple Camera Render`` button. The addon will render all cameras one by one, and once the rendering is finished,
the rendered animations will be saved to the output directory.
