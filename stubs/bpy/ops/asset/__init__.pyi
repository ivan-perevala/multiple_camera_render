import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def assign_action(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Set this pose Action as active Action on the active Object

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def bundle_install(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    asset_library_reference: str | None = "",
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
) -> None:
    """Copy the current .blend file into an Asset Library. Only works on standalone .blend files (i.e. when no other files are referenced)

        :type execution_context: int | str | None
        :type undo: bool | None
        :param asset_library_reference: asset_library_reference
        :type asset_library_reference: str | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter Python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
    """

def catalog_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    catalog_id: str = "",
) -> None:
    """Remove an asset catalog from the asset library (contained assets will not be affected and show up as unassigned)

    :type execution_context: int | str | None
    :type undo: bool | None
    :param catalog_id: Catalog ID, ID of the catalog to delete
    :type catalog_id: str
    """

def catalog_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    parent_path: str = "",
) -> None:
    """Create a new catalog to put assets in

    :type execution_context: int | str | None
    :type undo: bool | None
    :param parent_path: Parent Path, Optional path defining the location to put the new catalog under
    :type parent_path: str
    """

def catalog_redo(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Redo the last undone edit to the asset catalogs

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def catalog_undo(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Undo the last edit to the asset catalogs

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def catalog_undo_push(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Store the current state of the asset catalogs in the undo buffer

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def catalogs_save(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Make any edits to any catalogs permanent by writing the current set up to the asset library

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    set_fake_user: bool | None = False,
) -> None:
    """Delete all asset metadata and turn the selected asset data-blocks back into normal data-blocks

    :type execution_context: int | str | None
    :type undo: bool | None
    :param set_fake_user: Set Fake User, Ensure the data-block is saved, even when it is no longer marked as asset
    :type set_fake_user: bool | None
    """

def clear_single(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    set_fake_user: bool | None = False,
) -> None:
    """Delete all asset metadata and turn the asset data-block back into a normal data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    :param set_fake_user: Set Fake User, Ensure the data-block is saved, even when it is no longer marked as asset
    :type set_fake_user: bool | None
    """

def library_refresh(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Reread assets and asset catalogs from the asset library on disk

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def mark(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Enable easier reuse of selected data-blocks through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def mark_single(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Enable easier reuse of a data-block through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def open_containing_blend_file(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Open the blend file that contains the active asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def screenshot_preview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    p1: collections.abc.Iterable[int] | None = (0, 0),
    p2: collections.abc.Iterable[int] | None = (0, 0),
    force_square: bool | None = True,
) -> None:
    """Capture a screenshot to use as a preview for the selected asset

    :type execution_context: int | str | None
    :type undo: bool | None
    :param p1: Point 1, First point of the screenshot in screenspace
    :type p1: collections.abc.Iterable[int] | None
    :param p2: Point 2, Second point of the screenshot in screenspace
    :type p2: collections.abc.Iterable[int] | None
    :param force_square: Force Square, If enabled, the screenshot will have the same height as width
    :type force_square: bool | None
    """

def tag_add(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Add a new keyword tag to the active asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def tag_remove(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Remove an existing keyword tag from the active asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """
