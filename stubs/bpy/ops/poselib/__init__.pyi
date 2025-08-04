import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def apply_pose_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    blend_factor: float | None = 1.0,
    flipped: bool | None = False,
) -> None:
    """Apply the given Pose Action to the rig

    :type execution_context: int | str | None
    :type undo: bool | None
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: float | None
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool | None
    """

def asset_delete(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Delete the selected Pose Asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def asset_modify(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["ADJUST", "REPLACE", "ADD", "REMOVE"] | None = "ADJUST",
) -> None:
    """Update the selected pose asset in the asset library from the currently selected bones. The mode defines how the asset is updated

        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Overwrite Mode, Specify which parts of the pose asset are overwritten

    ADJUST
    Adjust -- Update existing channels in the pose asset but don't remove or add any channels.

    REPLACE
    Replace with Selection -- Completely replace all channels in the pose asset with the current selection.

    ADD
    Add Selected Bones -- Add channels of the selection to the pose asset. Existing channels will be updated.

    REMOVE
    Remove Selected Bones -- Remove channels of the selection from the pose asset.
        :type mode: typing.Literal['ADJUST','REPLACE','ADD','REMOVE'] | None
    """

def blend_pose_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    blend_factor: float | None = 0.0,
    flipped: bool | None = False,
    release_confirm: bool | None = False,
) -> None:
    """Blend the given Pose Action to the rig

    :type execution_context: int | str | None
    :type undo: bool | None
    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: float | None
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool | None
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button
    :type release_confirm: bool | None
    """

def convert_old_object_poselib(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Create a pose asset for each pose marker in this legacy pose library data-block

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def convert_old_poselib(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Create a pose asset for each pose marker in the current action

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def copy_as_asset(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Create a new pose asset on the clipboard, to be pasted into an Asset Browser

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def create_pose_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pose_name: str = "",
    asset_library_reference: str | None = "",
    catalog_path: str = "",
    activate_new_action: bool | None = False,
) -> None:
    """Create a new asset from the selected bones in the scene

    :type execution_context: int | str | None
    :type undo: bool | None
    :param pose_name: Pose Name, Name for the new pose asset
    :type pose_name: str
    :param asset_library_reference: Library, Asset library used to store the new pose
    :type asset_library_reference: str | None
    :param catalog_path: Catalog, Catalog to use for the new asset
    :type catalog_path: str
    :param activate_new_action: Activate New Action, This property is deprecated and will be removed in the future
    :type activate_new_action: bool | None
    """

def paste_asset(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Paste the Asset that was previously copied using Copy As Asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def pose_asset_select_bones(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
    flipped: bool | None = False,
) -> None:
    """Select those bones that are used in this pose

    :type execution_context: int | str | None
    :type undo: bool | None
    :param select: Select
    :type select: bool | None
    :param flipped: Flipped
    :type flipped: bool | None
    """

def restore_previous_action(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Switch back to the previous Action, after creating a pose asset

    :type execution_context: int | str | None
    :type undo: bool | None
    """
