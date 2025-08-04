import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.types

def svg(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    filter_glob: str = "*.svg",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
) -> None:
    """Load a SVG file

    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: File Path, Filepath used for importing the file
    :type filepath: str
    :param filter_glob: filter_glob
    :type filter_glob: str
    :param files: File Path
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    """
