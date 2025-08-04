import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def create(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "Collection",
) -> None:
    """Create an object collection from selected objects

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the new collection
    :type name: str
    """

def export_all(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Invoke all configured exporters on this collection

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def exporter_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
) -> None:
    """Add Exporter

    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, FileHandler idname
    :type name: str
    """

def exporter_export(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> None:
    """Invoke the export operation

    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Exporter index
    :type index: int | None
    """

def exporter_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> None:
    """Remove Exporter

    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Exporter index
    :type index: int | None
    """

def objects_add_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> None:
    """Add selected objects to one of the collections the active-object is part of. Optionally add to "All Collections" to ensure selected objects are included in the same collections as the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to add other selected objects to
    :type collection: str | None
    """

def objects_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> None:
    """Remove selected objects from a collection

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove this object from
    :type collection: str | None
    """

def objects_remove_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> None:
    """Remove the object from an object collection that contains the active object

    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, The collection to remove other selected objects from
    :type collection: str | None
    """

def objects_remove_all(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Remove selected objects from all collections

    :type execution_context: int | str | None
    :type undo: bool | None
    """
