from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
import os
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
import bpy
import bpy.utils.previews

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        from typing import Iterable
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        from bpy.types import ImagePreview

__all__ = ("IconsCache",)


class IconsCache:
    _directory: str = ""
    "Директорія для якої було згенеровано кеш значків"
    _cache: dict[str, int] = dict()
    "Кеш значків у форматі `identifier: icon_value`"
    _pcoll_cache: None | bpy.utils.previews.ImagePreviewCollection = None
    "Кеш значків згенерованих джерелом яких є зображення"

    @classmethod
    def _intern_initialize_from_data_files(cls, *, directory: str, ids: Iterable[str]):
        for identifier in ids:
            try:
                icon_value = bpy.app.icons.new_triangles_from_file(os.path.join(directory, f"{identifier}.dat"))
            except ValueError:
                # log.warning(f"Unable to load icon \"{identifier}\"")
                icon_value = 0

            cls._cache[identifier] = icon_value

    @classmethod
    def _intern_initialize_from_image_files(cls, *, directory: str, ids: Iterable[str]):
        pcoll = bpy.utils.previews.new()
        for identifier in ids:
            prv: ImagePreview = pcoll.load(identifier, os.path.join(directory, f"{identifier}.png"), 'IMAGE')
            cls._cache[identifier] = prv.icon_id
        cls._pcoll_cache = pcoll

    @classmethod
    def initialize(cls, *, directory: str, data_identifiers: Iterable[str], image_identifiers: Iterable[str]):
        """
        Метод для ініціалізації кешу значків.

        :param directory: Директорія що містить дані значків. Це можуть бути зображення а також згенеровані дата-файли.
        :type directory: str
        :param data_identifiers: Ідентифікатори значків джерелом яких є дата-файли.
        :type data_identifiers: Iterable[str]
        :param image_identifiers: Ідентифікатори значків джерелом яких є зображення.
        :type image_identifiers: Iterable[str]
        """
        if cls._cache and cls._directory == directory:
            return

        cls.release()

        if directory:
            cls._intern_initialize_from_data_files(directory=directory, ids=data_identifiers)
            cls._intern_initialize_from_image_files(directory=directory, ids=image_identifiers)

        cls._directory = directory

    @classmethod
    def release(cls):
        """
        Метод для очищення кешу значків. Його необхідно викликати коли видаляється реєстрація доповнення.
        """
        if cls._pcoll_cache is not None:
            bpy.utils.previews.remove(cls._pcoll_cache)
            cls._pcoll_cache = None

        cls._cache.clear()

    @classmethod
    def get_id(cls, identifier: str) -> int:
        """
        Метод для отримання `icon_value` для заданого ідентифікатора.

        :param identifier: Назва значка, одна з тих які було вказано під час ініціалізації кешу.
        :type identifier: str
        :return: Число яке можна використовувати як параметр в користувацькому інтерфейсі.
        :rtype: int
        """
        return cls._cache.get(identifier, 0)
