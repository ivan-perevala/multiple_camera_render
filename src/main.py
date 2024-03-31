from __future__ import annotations

import os

from bpy.app.handlers import persistent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bpy.types import (
        Object,
    )
    from . props import Scene
    from . props.scene import SceneProps


class Main:
    do: bool = False
    frame_camera_queue: list[Object] = list()
    frame_current: None | int = None
    render_directory: str = ""

    initial_render_filepath: str = ""
    initial_use_lock_interface: bool = False

    @staticmethod
    def _validate_camera(camera: None | Object) -> bool:
        if camera:
            try:
                getattr(camera, "name_full")
            except RuntimeError:
                return False
            else:
                return True
        return False

    @classmethod
    def _restore(cls, scene: Scene):
        if cls.do:
            scene.render.filepath = cls.initial_render_filepath
            scene.render.use_lock_interface = cls.initial_use_lock_interface
            cls.do = False

    @classmethod
    @persistent
    def handler_render_init(cls, scene: Scene, _):
        scene_props: SceneProps = scene.mcr

        if scene_props.use_multiple_camera_render:
            # Під час зміни кадру у вікні перегляду черга камер може бути заповненою на момент початку рендеру.
            cls.frame_camera_queue.clear()
            # Ініціалізуємо значення за замовчуванням для поточного кадру.
            cls.frame_current = scene.frame_current
            # Занотовуємо поточний шлях рендеру, його повинно бути відновлено наприкінці або у випадку скасування.
            cls.initial_render_filepath = scene.render.filepath

            # Занотовуємо прапор блокування інтерфейсу і блокуємо. Його повинно бути відновлено наприкінці або у випадку
            # скасування
            cls.initial_use_lock_interface = scene.render.use_lock_interface
            if not scene.render.use_lock_interface:
                scene.render.use_lock_interface = True

            # Визначаємо директорію до якої буде збережено зображення.
            abs_fp = scene.render.frame_path(frame=0)
            root, ext = os.path.splitext(abs_fp)
            cls.render_directory = os.path.dirname(root)

            cls.do = True
        else:
            cls.do = False

    @classmethod
    @persistent
    def handler_render_complete(cls, scene: Scene, _):
        cls._restore(scene)

    @classmethod
    @persistent
    def handler_render_cancel(cls, scene: Scene, _):
        cls._restore(scene)

    @classmethod
    @persistent
    def handler_render_write(cls, scene: Scene, _):
        pass  # scene.render.filepath = cls.initial_render_filepath

    @classmethod
    @persistent
    def handler_frame_change_pre(cls, scene: Scene, _):
        scene_props: SceneProps = scene.mcr

        do_camera, do_filepath = False, False

        if cls.do:
            do_camera = True
            do_filepath = True
        elif scene_props.use_multiple_camera_render and scene_props.use_viewport:
            do_camera = True
            do_filepath = False

        if do_camera or do_filepath:
            if not cls.frame_camera_queue:
                cls.frame_camera_queue = [_ for _ in scene.objects if _.type == 'CAMERA' and (not _.hide_render)]
                cls.frame_current = scene.frame_current

            scene.frame_current = cls.frame_current

            camera: None | Object = None
            while camera is None:
                camera = cls.frame_camera_queue.pop(0)
                if not cls._validate_camera(camera=camera):
                    camera = None

            if camera:
                if do_camera:
                    scene.camera = camera

                if do_filepath:
                    scene.render.filepath = os.path.join(cls.render_directory, f"{camera.name}_####")
