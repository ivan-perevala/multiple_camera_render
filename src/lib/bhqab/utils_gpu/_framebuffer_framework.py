from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
from enum import Enum, auto
# Зовнішній пакунок
from .. utils_wm import iter_regions
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
from gpu.types import GPUFrameBuffer, GPUTexture, GPUOffScreen
import bpy

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        from bpy.types import Region, Context

__all__ = (
    "Mode",
    "FrameBufferFramework",
)


class Mode(Enum):
    """
    Режим роботи фреймворку.
    """

    REGION = auto()
    "Робота з усіма регіонами переглядачів."
    TEXTURE = auto()
    "Робота з текстурою."


class FrameBufferFramework:
    """
    Фреймворк для роботи з буферами кадру.

    :param mode: Режим роботи, за замовчуванням :attr:`Mode.REGION`
    :type mode: :class:`Mode`, опційно
    :param area_type: Тип ділянки інтерфейсу, за замовчуванням 'VIEW_3D'
    :type area_type: str, опційно
    :param region_type: Тип регіону інтерфейсу, за замовчуванням 'WINDOW'
    :type region_type: str, опційно

    """
    __slots__ = (
        "_mode",
        "_region_framebuffer",
        "_area_type",
        "_region_type",
        "_texture_offscreen_data",
    )

    _mode: Mode

    # Mode.REGION
    _region_framebuffer: dict[Region, tuple[GPUFrameBuffer, None | GPUTexture, None | GPUTexture]]
    _area_type: str
    _region_type: str

    # Mode.TEXTURE
    _texture_offscreen_data: None | GPUOffScreen

    def __init__(self, *, mode=Mode.REGION, area_type='VIEW_3D', region_type='WINDOW'):
        self._mode = mode

        match self._mode:
            case Mode.REGION:
                self._region_framebuffer = dict()
                self._area_type = area_type
                self._region_type = region_type

            case Mode.TEXTURE:
                self._texture_offscreen_data = None

    def modal_eval(
            self,
            context: Context,
            *,
            texture_width: int = 0,
            texture_height: int = 0,
            color_format: str = "",
            depth_format: str = "",
            percentage: int = 100
    ):
        """
        Оновлює буфер кадру відповідно до розміру переглядачів і їх наявності. Повинен бути викликаний в модальній
        частині оператора.

        :param context: Поточний контекст.
        :type context: `Context`_
        :param texture_width: Ширина текстури (якщо створено з :attr:`Mode.TEXTURE`), за замовчуванням 0
        :type texture_width: int, опційно
        :param texture_height: Висота текстури (якщо створено з :attr:`Mode.TEXTURE`), за замовчуванням 0
        :type texture_height: int, опційно
        :param color_format: Формат текстури кольору або пустий рядок, якщо вона не потрібна, за замовчуванням ''.
        :type color_format: str, див. наявні опції `GPUTexture`_, опційно.
        :param depth_format: Формат текстури глибини або пустий рядок, якщо вона не потрібна, за замовчуванням ''.
        :type depth_format: str, див. наявні опції `GPUTexture`_, опційно.
        :param percentage: Відсоток від розміру переглядача або текстури, за замовчуванням 100.
        :type percentage: int, опційно
        """
        scale = max(10, min(400, percentage)) / 100

        match self._mode:
            case Mode.REGION:
                existing_regions = set(
                    region for region
                    in iter_regions(context, area_type=self._area_type, region_type=self._region_type)
                )

                invalid_regions = set(self._region_framebuffer.keys())
                invalid_regions.difference_update(existing_regions)
                for region in invalid_regions:
                    del self._region_framebuffer[region]

                for region in existing_regions:
                    do_update = True
                    do_update_depth_texture = True

                    width = int(region.width * scale)
                    height = int(region.height * scale)

                    if region in self._region_framebuffer:
                        framebuffer, texture, depth_texture = self._region_framebuffer[region]

                        do_update = not (
                            (
                                color_format and texture and (
                                    texture.width == width
                                    and texture.height == height
                                    and texture.format == color_format
                                )
                            )
                        )

                        do_update_depth_texture = not (
                            (
                                depth_format and depth_texture and (
                                    depth_texture.width == width
                                    and depth_texture.height == height
                                    and depth_texture.format == depth_format
                                )
                            )
                        )

                    if do_update or do_update_depth_texture:
                        if do_update:
                            if color_format:
                                texture = GPUTexture(size=(width, height), format=color_format)
                            else:
                                texture = None

                        if do_update_depth_texture:
                            if depth_format:
                                depth_texture = GPUTexture(size=(width, height), format=depth_format)
                            else:
                                depth_texture = None

                        framebuffer = GPUFrameBuffer(color_slots=texture, depth_slot=depth_texture)
                        self._region_framebuffer[region] = (framebuffer, texture, depth_texture)

            case Mode.TEXTURE:
                assert (color_format)

                offscreen = self._texture_offscreen_data

                do_update = True

                required_width = int(texture_width * scale)
                required_height = int(texture_height * scale)

                if offscreen:
                    width = int(offscreen.width * scale)
                    height = int(offscreen.height * scale)

                    do_update = not (
                        width == required_width
                        and height == required_height
                        and offscreen.format == color_format
                    )

                if do_update:
                    self._texture_offscreen_data = GPUOffScreen(
                        width=required_width,
                        height=required_height,
                        format=color_format
                    )

    def get(
        self,
        *,
        region: None | Region = None
    ) -> None | GPUFrameBuffer | GPUOffScreen:
        """
        Отримання даних буфера залежно від контексту створення екземпляру.

        :param region: Поточний регіон перегляду, потрібно вказати для режиму :attr:`Mode.REGION`, за замовчуванням None
        :type region: None | `Region`_, опційно
        :return: Буфер кадру або закадровий буфер.
        :rtype: None | tuple[`GPUFrameBuffer`_, None | `GPUTexture`_, None | `GPUTexture`_] | `GPUOffScreen`_
        """
        match self._mode:
            case Mode.REGION:
                if not region:
                    region = bpy.context.region
                if region in self._region_framebuffer:
                    return self._region_framebuffer[region][0]
                return None
            case Mode.TEXTURE:
                return self._texture_offscreen_data

    def get_color_texture(self, *, region: None | Region = None) -> None | GPUTexture:
        """
        Метод отримання текстури кольору.

        :param region: Поточний регіон перегляду, потрібно вказати для режиму :attr:`Mode.REGION`, за замовчуванням None
        :type region: None | Region, опційно
        :return: Наявна текстура кольору або нічого якщо вона відсутня.
        :rtype: None | `GPUTexture`_
        """
        match self._mode:
            case Mode.REGION:
                if not region:
                    region = bpy.context.region
                if region in self._region_framebuffer:
                    return self._region_framebuffer[region][1]
                return None
            case Mode.TEXTURE:
                return self._texture_offscreen_data.texture_color

    def get_depth_texture(self, *, region: None | Region = None) -> None | GPUTexture:
        """
        Метод отримання текстури глибини.

        :param region: Поточний регіон перегляду, потрібно вказати для режиму :attr:`Mode.REGION`, за замовчуванням None
        :type region: None | Region, опційно
        :return: Наявна текстура глибини або нічого якщо вона відсутня (або створено в режимі :attr:`Mode.TEXTURE`).
        :rtype: None | `GPUTexture`_
        """
        match self._mode:
            case Mode.REGION:
                if not region:
                    region = bpy.context.region
                if region in self._region_framebuffer:
                    return self._region_framebuffer[region][2]
                return None
            case Mode.TEXTURE:
                return None
