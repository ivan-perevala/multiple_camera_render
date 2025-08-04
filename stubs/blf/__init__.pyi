"""
This module provides access to Blender's text drawing functions.


--------------------

Example of using the blf module. For this module to work we
need to use the GPU module gpu as well.

```../examples/blf.py```


--------------------

Example showing how text can be draw into an image.
This can be done by binding an image buffer (imbuf) to the font's ID.

```../examples/blf.1.py```

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def aspect(fontid: int, aspect: float) -> None:
    """Set the aspect for drawing text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param aspect: The aspect ratio for text drawing to use.
    :type aspect: float
    """

def bind_imbuf(fontid: int, image, display_name: None | str | None = None) -> None:
    """Context manager to draw text into an image buffer instead of the GPU's context.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param display_name: The color management display name to use or None.
    :type display_name: None | str | None
    :return: The BLF ImBuf context manager.
    """

def clipping(fontid: int, xmin: float, ymin: float, xmax: float, ymax: float) -> None:
    """Set the clipping, enable/disable using CLIPPING.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param xmin: Clip the drawing area by these bounds.
    :type xmin: float
    :param ymin: Clip the drawing area by these bounds.
    :type ymin: float
    :param xmax: Clip the drawing area by these bounds.
    :type xmax: float
    :param ymax: Clip the drawing area by these bounds.
    :type ymax: float
    """

def color(fontid: int, r: float, g: float, b: float, a: float) -> None:
    """Set the color for drawing text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param r: red channel 0.0 - 1.0.
    :type r: float
    :param g: green channel 0.0 - 1.0.
    :type g: float
    :param b: blue channel 0.0 - 1.0.
    :type b: float
    :param a: alpha channel 0.0 - 1.0.
    :type a: float
    """

def dimensions(fontid: int, text: str) -> tuple[float, float]:
    """Return the width and height of the text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param text: the text to draw.
    :type text: str
    :return: the width and height of the text.
    :rtype: tuple[float, float]
    """

def disable(fontid: int, option: int) -> None:
    """Disable option.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param option: One of ROTATION, CLIPPING, SHADOW or KERNING_DEFAULT.
    :type option: int
    """

def draw(fontid: int, text: str) -> None:
    """Draw text in the current context.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param text: the text to draw.
    :type text: str
    """

def draw_buffer(fontid: int, text: str) -> None:
    """Draw text into the buffer bound to the fontid.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param text: the text to draw.
    :type text: str
    """

def enable(fontid: int, option: int) -> None:
    """Enable option.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param option: One of ROTATION, CLIPPING, SHADOW or KERNING_DEFAULT.
    :type option: int
    """

def load(filepath: bytes | str) -> int:
    """Load a new font.

    :param filepath: the filepath of the font.
    :type filepath: bytes | str
    :return: the new font's fontid or -1 if there was an error.
    :rtype: int
    """

def position(fontid: int, x: float, y: float, z: float) -> None:
    """Set the position for drawing text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param x: X axis position to draw the text.
    :type x: float
    :param y: Y axis position to draw the text.
    :type y: float
    :param z: Z axis position to draw the text.
    :type z: float
    """

def rotation(fontid: int, angle: float) -> None:
    """Set the text rotation angle, enable/disable using ROTATION.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param angle: The angle for text drawing to use.
    :type angle: float
    """

def shadow(fontid: int, level: int, r: float, g: float, b: float, a: float) -> None:
    """Shadow options, enable/disable using SHADOW .

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param level: The blur level (0, 3, 5) or outline (6).
    :type level: int
    :param r: Shadow color (red channel 0.0 - 1.0).
    :type r: float
    :param g: Shadow color (green channel 0.0 - 1.0).
    :type g: float
    :param b: Shadow color (blue channel 0.0 - 1.0).
    :type b: float
    :param a: Shadow color (alpha channel 0.0 - 1.0).
    :type a: float
    """

def shadow_offset(fontid: int, x: float, y: float) -> None:
    """Set the offset for shadow text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param x: Vertical shadow offset value in pixels.
    :type x: float
    :param y: Horizontal shadow offset value in pixels.
    :type y: float
    """

def size(fontid: int, size: float) -> None:
    """Set the size for drawing text.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param size: Point size of the font.
    :type size: float
    """

def unload(filepath: bytes | str) -> None:
    """Unload an existing font.

    :param filepath: the filepath of the font.
    :type filepath: bytes | str
    """

def word_wrap(fontid: int, wrap_width: int) -> None:
    """Set the wrap width, enable/disable using WORD_WRAP.

    :param fontid: The id of the typeface as returned by `blf.load`, for default font use 0.
    :type fontid: int
    :param wrap_width: The width (in pixels) to wrap words at.
    :type wrap_width: int
    """

CLIPPING: typing.Any
""" Constant value 2
"""

MONOCHROME: typing.Any
""" Constant value 128
"""

ROTATION: typing.Any
""" Constant value 1
"""

SHADOW: typing.Any
""" Constant value 4
"""

WORD_WRAP: typing.Any
""" Constant value 64
"""
