from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
from gpu.types import GPUBatch, GPUVertBuf, GPUIndexBuf, GPUVertFormat

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
        pass

__all__ = ("BatchPreset",)


class BatchPreset:
    """
    Заздалегідь заготовлені групи вершин. Всі змінні класу можна використовувати лише для зчитування.
    """

    _unit_rectangle_tris_P_vbo: None | GPUVertBuf = None
    _unit_rectangle_tris_P_ibo: None | GPUIndexBuf = None

    _ndc_rectangle_tris_P_UV_vbo: None | GPUVertBuf = None
    _ndc_rectangle_tris_P_UV_ibo: None | GPUIndexBuf = None

    @classmethod
    def get_unit_rectangle_tris_P(cls) -> GPUBatch:
        """
        Квадрат типу 'TRIS' з центром на початку координат і стороною 1 одиницю виміру.
        """
        if not cls._unit_rectangle_tris_P_vbo or not cls._unit_rectangle_tris_P_ibo:
            cls._update_unit_rectangle_tris_P_buffer_objects()
        # Створюємо новий кожного разу, оскільки:
        # ERROR (gpu.debug):  : GL_INVALID_OPERATION error generated. VAO names must be generated with glGenVertexArrays
        # before they can be bound or used.
        return GPUBatch(type='TRIS', buf=cls._unit_rectangle_tris_P_vbo, elem=cls._unit_rectangle_tris_P_ibo)

    @classmethod
    def _update_unit_rectangle_tris_P_buffer_objects(cls):
        vert_fmt = GPUVertFormat()
        vert_fmt.attr_add(id="P", comp_type='F32', len=2, fetch_mode='FLOAT')

        vbo = GPUVertBuf(format=vert_fmt, len=4)
        vbo.attr_fill(id="P", data=((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)))

        ibo = GPUIndexBuf(type='TRIS', seq=((0, 1, 2), (0, 2, 3)))

        cls._unit_rectangle_tris_P_vbo = vbo
        cls._unit_rectangle_tris_P_ibo = ibo

    @classmethod
    def get_ndc_rectangle_tris_P_UV(cls) -> GPUBatch:
        """
        Квадрат типу 'TRIS' зі стороною 2 одиниці виміру для відображення в нормалізованих координатах.Містить
        атрибути "P" (-1.0 ... 1.0) і "UV" (0.0 ... 1.0).
        """
        if not cls._ndc_rectangle_tris_P_UV_vbo or not cls._ndc_rectangle_tris_P_UV_ibo:
            cls._update_ndc_rectangle_tris_P_UV_buffer_objects()
        # Створюємо новий кожного разу, оскільки:
        # ERROR (gpu.debug):  : GL_INVALID_OPERATION error generated. VAO names must be generated with glGenVertexArrays
        # before they can be bound or used.
        return GPUBatch(type='TRIS', buf=cls._ndc_rectangle_tris_P_UV_vbo, elem=cls._ndc_rectangle_tris_P_UV_ibo)

    @classmethod
    def _update_ndc_rectangle_tris_P_UV_buffer_objects(cls):
        vert_fmt = GPUVertFormat()
        vert_fmt.attr_add(id="P", comp_type='F32', len=2, fetch_mode='FLOAT')
        vert_fmt.attr_add(id="UV", comp_type='F32', len=2, fetch_mode='FLOAT')

        vbo = GPUVertBuf(format=vert_fmt, len=4)
        vbo.attr_fill(id="P", data=((-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (1.0, -1.0))),
        vbo.attr_fill(id="UV", data=((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))),

        ibo = GPUIndexBuf(type='TRIS', seq=((0, 1, 2), (0, 2, 3)))

        cls._ndc_rectangle_tris_P_UV_vbo = vbo
        cls._ndc_rectangle_tris_P_UV_ibo = ibo
