import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def autocomplete(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Show a list of used text in the open document

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def comment_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["TOGGLE", "COMMENT", "UNCOMMENT"] | None = "TOGGLE",
) -> None:
    """Undocumented, consider contributing.

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Add or remove comments
    :type type: typing.Literal['TOGGLE','COMMENT','UNCOMMENT'] | None
    """

def convert_whitespace(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["SPACES", "TABS"] | None = "SPACES",
) -> None:
    """Convert whitespaces by type

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Type of whitespace to convert to
    :type type: typing.Literal['SPACES','TABS'] | None
    """

def copy(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Copy selected text to clipboard

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def cursor_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    x: int | None = 0,
    y: int | None = 0,
) -> None:
    """Set cursor position

    :type execution_context: int | str | None
    :type undo: bool | None
    :param x: X
    :type x: int | None
    :param y: Y
    :type y: int | None
    """

def cut(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Cut selected text to clipboard

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "NEXT_CHARACTER", "PREVIOUS_CHARACTER", "NEXT_WORD", "PREVIOUS_WORD"
    ]
    | None = "NEXT_CHARACTER",
) -> None:
    """Delete text by cursor position

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Which part of the text to delete
    :type type: typing.Literal['NEXT_CHARACTER','PREVIOUS_CHARACTER','NEXT_WORD','PREVIOUS_WORD'] | None
    """

def duplicate_line(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Duplicate the current line

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def find(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Find specified text

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def find_set_selected(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Find specified text and set as selected

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def indent(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Indent selected text

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def indent_or_autocomplete(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Indent selected text or autocomplete

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    text: str = "",
) -> None:
    """Insert text at cursor position

    :type execution_context: int | str | None
    :type undo: bool | None
    :param text: Text, Text to insert at the cursor position
    :type text: str
    """

def jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    line: int | None = 1,
) -> None:
    """Jump cursor to line

    :type execution_context: int | str | None
    :type undo: bool | None
    :param line: Line, Line number to jump to
    :type line: int | None
    """

def jump_to_file_at_point(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    line: int | None = 0,
    column: int | None = 0,
) -> None:
    """Jump to a file for the text editor

    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: Filepath
    :type filepath: str
    :param line: Line, Line to jump to
    :type line: int | None
    :param column: Column, Column to jump to
    :type column: int | None
    """

def line_break(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Insert line break at cursor position

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def line_number(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """The current line number

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def make_internal(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Make active text file internal

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "LINE_BEGIN",
        "LINE_END",
        "FILE_TOP",
        "FILE_BOTTOM",
        "PREVIOUS_CHARACTER",
        "NEXT_CHARACTER",
        "PREVIOUS_WORD",
        "NEXT_WORD",
        "PREVIOUS_LINE",
        "NEXT_LINE",
        "PREVIOUS_PAGE",
        "NEXT_PAGE",
    ]
    | None = "LINE_BEGIN",
) -> None:
    """Move cursor to position type

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Where to move cursor to
    :type type: typing.Literal['LINE_BEGIN','LINE_END','FILE_TOP','FILE_BOTTOM','PREVIOUS_CHARACTER','NEXT_CHARACTER','PREVIOUS_WORD','NEXT_WORD','PREVIOUS_LINE','NEXT_LINE','PREVIOUS_PAGE','NEXT_PAGE'] | None
    """

def move_lines(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "DOWN",
) -> None:
    """Move the currently selected line(s) up/down

    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def move_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "LINE_BEGIN",
        "LINE_END",
        "FILE_TOP",
        "FILE_BOTTOM",
        "PREVIOUS_CHARACTER",
        "NEXT_CHARACTER",
        "PREVIOUS_WORD",
        "NEXT_WORD",
        "PREVIOUS_LINE",
        "NEXT_LINE",
        "PREVIOUS_PAGE",
        "NEXT_PAGE",
    ]
    | None = "LINE_BEGIN",
) -> None:
    """Move the cursor while selecting

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Where to move cursor to, to make a selection
    :type type: typing.Literal['LINE_BEGIN','LINE_END','FILE_TOP','FILE_BOTTOM','PREVIOUS_CHARACTER','NEXT_CHARACTER','PREVIOUS_WORD','NEXT_WORD','PREVIOUS_LINE','NEXT_LINE','PREVIOUS_PAGE','NEXT_PAGE'] | None
    """

def new(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Create a new text data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def open(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = True,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = True,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "DEFAULT",
        "FILE_SORT_ALPHA",
        "FILE_SORT_EXTENSION",
        "FILE_SORT_TIME",
        "FILE_SORT_SIZE",
        "ASSET_CATALOG",
    ]
    | None = "",
    internal: bool | None = False,
) -> None:
    """Open a new text data-block

        :type execution_context: int | str | None
        :type undo: bool | None
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

    DEFAULT
    Default -- Automatically determine sort method for files.

    FILE_SORT_ALPHA
    Name -- Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension -- Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date -- Sort files by modification time.

    FILE_SORT_SIZE
    Size -- Sort files by size.

    ASSET_CATALOG
    Asset Catalog -- Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..
        :type sort_method: typing.Literal['DEFAULT','FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE','ASSET_CATALOG'] | None
        :param internal: Make Internal, Make text file internal after loading
        :type internal: bool | None
    """

def overwrite_toggle(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Toggle overwrite while typing

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    selection: bool | None = False,
) -> None:
    """Paste text from clipboard

    :type execution_context: int | str | None
    :type undo: bool | None
    :param selection: Selection, Paste text selected elsewhere rather than copied (X11/Wayland only)
    :type selection: bool | None
    """

def reload(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Reload active text data-block from its file

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def replace(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> None:
    """Replace text with the specified text

    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: Replace All, Replace all occurrences
    :type all: bool | None
    """

def replace_set_selected(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Replace text with specified text and set as selected

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def resolve_conflict(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    resolution: typing.Literal["IGNORE", "RELOAD", "SAVE", "MAKE_INTERNAL"]
    | None = "IGNORE",
) -> None:
    """When external text is out of sync, resolve the conflict

    :type execution_context: int | str | None
    :type undo: bool | None
    :param resolution: Resolution, How to solve conflict due to differences in internal and external text
    :type resolution: typing.Literal['IGNORE','RELOAD','SAVE','MAKE_INTERNAL'] | None
    """

def run_script(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Run active script

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def save(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Save active text data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def save_as(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = True,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = True,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
) -> None:
    """Save active text file with options

        :type execution_context: int | str | None
        :type undo: bool | None
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

def scroll(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    lines: int | None = 1,
) -> None:
    """Undocumented, consider contributing.

    :type execution_context: int | str | None
    :type undo: bool | None
    :param lines: Lines, Number of lines to scroll
    :type lines: int | None
    """

def scroll_bar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    lines: int | None = 1,
) -> None:
    """Undocumented, consider contributing.

    :type execution_context: int | str | None
    :type undo: bool | None
    :param lines: Lines, Number of lines to scroll
    :type lines: int | None
    """

def select_all(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select all text

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_line(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select text by line

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_word(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select word under cursor

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def selection_set(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Set text selection

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def start_find(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Start searching text

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def to_3d_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    split_lines: bool | None = False,
) -> None:
    """Create 3D text object from active text data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    :param split_lines: Split Lines, Create one object per line in the text
    :type split_lines: bool | None
    """

def unindent(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Unindent selected text

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def unlink(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Unlink active text data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def update_shader(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Update users of this shader, such as custom cameras and script nodes, with its new sockets and options

    :type execution_context: int | str | None
    :type undo: bool | None
    """
