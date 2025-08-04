import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops.transform
import bpy.stub_internal.rna_enums
import bpy.types
import mathutils

def add_bezier(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> None:
    """Add new bezier curve

        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

def add_circle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> None:
    """Add new circle curve

        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Sequence[float] | mathutils.Vector | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Sequence[float] | mathutils.Euler | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Sequence[float] | mathutils.Vector | None
    """

def attribute_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value_float: float | None = 0.0,
    value_float_vector_2d: collections.abc.Iterable[float] | None = (0.0, 0.0),
    value_float_vector_3d: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    value_int: int | None = 0,
    value_int_vector_2d: collections.abc.Iterable[int] | None = (0, 0),
    value_color: collections.abc.Iterable[float] | None = (1.0, 1.0, 1.0, 1.0),
    value_bool: bool | None = False,
) -> None:
    """Set values of the active attribute for selected elements

    :type execution_context: int | str | None
    :type undo: bool | None
    :param value_float: Value
    :type value_float: float | None
    :param value_float_vector_2d: Value
    :type value_float_vector_2d: collections.abc.Iterable[float] | None
    :param value_float_vector_3d: Value
    :type value_float_vector_3d: collections.abc.Iterable[float] | None
    :param value_int: Value
    :type value_int: int | None
    :param value_int_vector_2d: Value
    :type value_int_vector_2d: collections.abc.Iterable[int] | None
    :param value_color: Value
    :type value_color: collections.abc.Iterable[float] | None
    :param value_bool: Value
    :type value_bool: bool | None
    """

def convert_from_particle_system(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Add a new curves object based on the current state of the particle system

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def convert_to_particle_system(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Add a new or update an existing hair particle system on the surface object

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def curve_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: bpy.stub_internal.rna_enums.CurvesTypeItems | None = "POLY",
    use_handles: bool | None = False,
) -> None:
    """Set type of selected curves

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Curve type
    :type type: bpy.stub_internal.rna_enums.CurvesTypeItems | None
    :param use_handles: Handles, Take handle information into account in the conversion
    :type use_handles: bool | None
    """

def cyclic_toggle(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Make active curve closed/opened loop

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def delete(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Remove selected control points or curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def draw(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    error_threshold: float | None = 0.0,
    fit_method: bpy.stub_internal.rna_enums.CurveFitMethodItems | None = "REFIT",
    corner_angle: float | None = 1.22173,
    use_cyclic: bool | None = True,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    wait_for_input: bool | None = True,
    is_curve_2d: bool | None = False,
    bezier_as_nurbs: bool | None = False,
) -> None:
    """Draw a freehand curve

    :type execution_context: int | str | None
    :type undo: bool | None
    :param error_threshold: Error, Error distance threshold (in object units)
    :type error_threshold: float | None
    :param fit_method: Fit Method
    :type fit_method: bpy.stub_internal.rna_enums.CurveFitMethodItems | None
    :param corner_angle: Corner Angle
    :type corner_angle: float | None
    :param use_cyclic: Cyclic
    :type use_cyclic: bool | None
    :param stroke: Stroke
    :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
    :param wait_for_input: Wait for Input
    :type wait_for_input: bool | None
    :param is_curve_2d: Curve 2D
    :type is_curve_2d: bool | None
    :param bezier_as_nurbs: As NURBS
    :type bezier_as_nurbs: bool | None
    """

def duplicate(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Copy selected points or curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVES_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
) -> None:
    """Make copies of selected elements and move them

    :type execution_context: int | str | None
    :type undo: bool | None
    :param CURVES_OT_duplicate: Duplicate, Copy selected points or curves
    :type CURVES_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def extrude(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Extrude selected control point(s)

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def extrude_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVES_OT_extrude: extrude | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
) -> None:
    """Extrude curve and move result

    :type execution_context: int | str | None
    :type undo: bool | None
    :param CURVES_OT_extrude: Extrude, Extrude selected control point(s)
    :type CURVES_OT_extrude: extrude | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def handle_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: bpy.stub_internal.rna_enums.CurvesHandleTypeItems | None = "AUTO",
) -> None:
    """Set the handle type for bezier curves

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: bpy.stub_internal.rna_enums.CurvesHandleTypeItems | None
    """

def sculptmode_toggle(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Enter/Exit sculpt mode for curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> None:
    """(De)select all control points

        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Literal['TOGGLE','SELECT','DESELECT','INVERT'] | None
    """

def select_ends(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    amount_start: int | None = 0,
    amount_end: int | None = 1,
) -> None:
    """Select end points of curves

    :type execution_context: int | str | None
    :type undo: bool | None
    :param amount_start: Amount Front, Number of points to select from the front
    :type amount_start: int | None
    :param amount_end: Amount Back, Number of points to select from the back
    :type amount_end: int | None
    """

def select_less(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Shrink the selection by one point

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select all points in curves with any point selection

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
) -> None:
    """Select all points in the curve under the cursor

    :type execution_context: int | str | None
    :type undo: bool | None
    :param deselect: Deselect, Deselect linked control points rather than selecting them
    :type deselect: bool | None
    """

def select_more(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Grow the selection by one point

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    seed: int | None = 0,
    probability: float | None = 0.5,
) -> None:
    """Randomizes existing selection or create new random selection

    :type execution_context: int | str | None
    :type undo: bool | None
    :param seed: Seed, Source of randomness
    :type seed: int | None
    :param probability: Probability, Chance of every point or curve being included in the selection
    :type probability: float | None
    """

def separate(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Separate selected geometry into a new object

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_selection_domain(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    domain: bpy.stub_internal.rna_enums.AttributeCurvesDomainItems | None = "POINT",
) -> None:
    """Change the mode used for selection masking in curves sculpt mode

    :type execution_context: int | str | None
    :type undo: bool | None
    :param domain: Domain
    :type domain: bpy.stub_internal.rna_enums.AttributeCurvesDomainItems | None
    """

def snap_curves_to_surface(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    attach_mode: typing.Literal["NEAREST", "DEFORM"] | None = "NEAREST",
) -> None:
    """Move curves so that the first point is exactly on the surface mesh

        :type execution_context: int | str | None
        :type undo: bool | None
        :param attach_mode: Attach Mode, How to find the point on the surface to attach to

    NEAREST
    Nearest -- Find the closest point on the surface for the root point of every curve and move the root there.

    DEFORM
    Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
        :type attach_mode: typing.Literal['NEAREST','DEFORM'] | None
    """

def split(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Split selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    number_cuts: int | None = 1,
) -> None:
    """Subdivide selected curve segments

    :type execution_context: int | str | None
    :type undo: bool | None
    :param number_cuts: Number of Cuts
    :type number_cuts: int | None
    """

def surface_set(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Use the active object as surface for selected curves objects and set it as the parent

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def switch_direction(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Reverse the direction of the selected curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def tilt_clear(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Clear the tilt of selected control points

    :type execution_context: int | str | None
    :type undo: bool | None
    """
