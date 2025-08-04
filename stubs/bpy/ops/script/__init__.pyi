import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def execute_preset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    menu_idname: str = "",
) -> None:
    """Load a preset

    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    :param menu_idname: Menu ID Name, ID name of the menu this was called from
    :type menu_idname: str
    """

def python_file_run(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
) -> None:
    """Run Python file

    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: Path
    :type filepath: str
    """

def reload(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Reload scripts

    :type execution_context: int | str | None
    :type undo: bool | None
    """
