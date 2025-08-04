import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops.transform
import bpy.stub_internal.rna_enums
import bpy.types
import mathutils

def cyclic_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["CYCLIC_U", "CYCLIC_V"] | None = "CYCLIC_U",
) -> None:
    """Make active spline closed/opened loop

    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to make surface cyclic in
    :type direction: typing.Literal['CYCLIC_U','CYCLIC_V'] | None
    """

def de_select_first(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """(De)select first of visible part of each NURBS

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def de_select_last(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """(De)select last of visible part of each NURBS

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def decimate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 1.0,
) -> None:
    """Simplify selected curves

    :type execution_context: int | str | None
    :type undo: bool | None
    :param ratio: Ratio
    :type ratio: float | None
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["VERT", "SEGMENT"] | None = "VERT",
) -> None:
    """Delete selected control points or segments

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Which elements to delete
    :type type: typing.Literal['VERT','SEGMENT'] | None
    """

def dissolve_verts(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Delete selected control points, correcting surrounding handles

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
) -> None:
    """Draw a freehand spline

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
    """

def duplicate(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Duplicate selected control points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVE_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
) -> None:
    """Duplicate curve and move

    :type execution_context: int | str | None
    :type undo: bool | None
    :param CURVE_OT_duplicate: Duplicate Curve, Duplicate selected control points
    :type CURVE_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def extrude(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: bpy.stub_internal.rna_enums.TransformModeTypeItems | None = "TRANSLATION",
) -> None:
    """Extrude selected control point(s)

    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: bpy.stub_internal.rna_enums.TransformModeTypeItems | None
    """

def extrude_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVE_OT_extrude: extrude | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
) -> None:
    """Extrude curve and move result

    :type execution_context: int | str | None
    :type undo: bool | None
    :param CURVE_OT_extrude: Extrude, Extrude selected control point(s)
    :type CURVE_OT_extrude: extrude | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def handle_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "AUTOMATIC", "VECTOR", "ALIGNED", "FREE_ALIGN", "TOGGLE_FREE_ALIGN"
    ]
    | None = "AUTOMATIC",
) -> None:
    """Set type of handles for selected control points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Spline type
    :type type: typing.Literal['AUTOMATIC','VECTOR','ALIGNED','FREE_ALIGN','TOGGLE_FREE_ALIGN'] | None
    """

def hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> None:
    """Hide (un)selected control points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param unselected: Unselected, Hide unselected rather than selected
    :type unselected: bool | None
    """

def make_segment(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Join two curves by their selected ends

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def match_texture_space(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Match texture space to object's bounding box

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def normals_make_consistent(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    calc_length: bool | None = False,
) -> None:
    """Recalculate the direction of selected handles

    :type execution_context: int | str | None
    :type undo: bool | None
    :param calc_length: Length, Recalculate handle length
    :type calc_length: bool | None
    """

def pen(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
    deselect_all: bool | None = False,
    select_passthrough: bool | None = False,
    extrude_point: bool | None = False,
    extrude_handle: typing.Literal["AUTO", "VECTOR"] | None = "VECTOR",
    delete_point: bool | None = False,
    insert_point: bool | None = False,
    move_segment: bool | None = False,
    select_point: bool | None = False,
    move_point: bool | None = False,
    close_spline: bool | None = True,
    close_spline_method: typing.Literal["OFF", "ON_PRESS", "ON_CLICK"] | None = "OFF",
    toggle_vector: bool | None = False,
    cycle_handle_type: bool | None = False,
) -> None:
    """Construct and edit splines

        :type execution_context: int | str | None
        :type undo: bool | None
        :param extend: Extend, Extend selection instead of deselecting everything first
        :type extend: bool | None
        :param deselect: Deselect, Remove from selection
        :type deselect: bool | None
        :param toggle: Toggle Selection, Toggle the selection
        :type toggle: bool | None
        :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor
        :type deselect_all: bool | None
        :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected
        :type select_passthrough: bool | None
        :param extrude_point: Extrude Point, Add a point connected to the last selected point
        :type extrude_point: bool | None
        :param extrude_handle: Extrude Handle Type, Type of the extruded handle
        :type extrude_handle: typing.Literal['AUTO','VECTOR'] | None
        :param delete_point: Delete Point, Delete an existing point
        :type delete_point: bool | None
        :param insert_point: Insert Point, Insert Point into a curve segment
        :type insert_point: bool | None
        :param move_segment: Move Segment, Delete an existing point
        :type move_segment: bool | None
        :param select_point: Select Point, Select a point or its handles
        :type select_point: bool | None
        :param move_point: Move Point, Move a point or its handles
        :type move_point: bool | None
        :param close_spline: Close Spline, Make a spline cyclic by clicking endpoints
        :type close_spline: bool | None
        :param close_spline_method: Close Spline Method, The condition for close spline to activate

    OFF
    None.

    ON_PRESS
    On Press -- Move handles after closing the spline.

    ON_CLICK
    On Click -- Spline closes on release if not dragged.
        :type close_spline_method: typing.Literal['OFF','ON_PRESS','ON_CLICK'] | None
        :param toggle_vector: Toggle Vector, Toggle between Vector and Auto handles
        :type toggle_vector: bool | None
        :param cycle_handle_type: Cycle Handle Type, Cycle between all four handle types
        :type cycle_handle_type: bool | None
    """

def primitive_bezier_circle_add(
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
    """Construct a Bézier Circle

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

def primitive_bezier_curve_add(
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
    """Construct a Bézier Curve

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

def primitive_nurbs_circle_add(
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
    """Construct a Nurbs Circle

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

def primitive_nurbs_curve_add(
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
    """Construct a Nurbs Curve

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

def primitive_nurbs_path_add(
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
    """Construct a Path

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

def radius_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
) -> None:
    """Set per-point radius which is used for bevel tapering

    :type execution_context: int | str | None
    :type undo: bool | None
    :param radius: Radius
    :type radius: float | None
    """

def reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> None:
    """Reveal hidden control points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param select: Select
    :type select: bool | None
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

def select_less(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Deselect control points at the boundary of each selection region

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select all control points linked to the current selection

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
    """Select all control points linked to already selected ones

    :type execution_context: int | str | None
    :type undo: bool | None
    :param deselect: Deselect, Deselect linked control points rather than selecting them
    :type deselect: bool | None
    """

def select_more(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select control points at the boundary of each selection region

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_next(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select control points following already selected ones along the curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_nth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    skip: int | None = 1,
    nth: int | None = 1,
    offset: int | None = 0,
) -> None:
    """Deselect every Nth point starting from the active one

    :type execution_context: int | str | None
    :type undo: bool | None
    :param skip: Deselected, Number of deselected elements in the repetitive sequence
    :type skip: int | None
    :param nth: Selected, Number of selected elements in the repetitive sequence
    :type nth: int | None
    :param offset: Offset, Offset from the starting point
    :type offset: int | None
    """

def select_previous(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select control points preceding already selected ones along the curves

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
) -> None:
    """Randomly select some control points

        :type execution_context: int | str | None
        :type undo: bool | None
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: float | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: int | None
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Literal['SELECT','DESELECT'] | None
    """

def select_row(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select a row of control points including active one. Successive use on the same point switches between U/V directions

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_similar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["TYPE", "RADIUS", "WEIGHT", "DIRECTION"] | None = "WEIGHT",
    compare: typing.Literal["EQUAL", "GREATER", "LESS"] | None = "EQUAL",
    threshold: float | None = 0.1,
) -> None:
    """Select similar curve points by property type

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['TYPE','RADIUS','WEIGHT','DIRECTION'] | None
    :param compare: Compare
    :type compare: typing.Literal['EQUAL','GREATER','LESS'] | None
    :param threshold: Threshold
    :type threshold: float | None
    """

def separate(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Separate selected points from connected unselected points into a new object

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shade_flat(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Set shading to flat

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shade_smooth(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Set shading to smooth

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shortest_path_pick(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Select shortest path between two selections

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def smooth(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Flatten angles of selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def smooth_radius(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Interpolate radii of selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def smooth_tilt(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Interpolate tilt of selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def smooth_weight(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Interpolate weight of selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    """

def spin(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    center: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    axis: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> None:
    """Extrude selected boundary row around pivot point and current view axis

    :type execution_context: int | str | None
    :type undo: bool | None
    :param center: Center, Center in global view space
    :type center: collections.abc.Sequence[float] | mathutils.Vector | None
    :param axis: Axis, Axis in global view space
    :type axis: collections.abc.Sequence[float] | mathutils.Vector | None
    """

def spline_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["POLY", "BEZIER", "NURBS"] | None = "POLY",
    use_handles: bool | None = False,
) -> None:
    """Set type of active spline

    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Spline type
    :type type: typing.Literal['POLY','BEZIER','NURBS'] | None
    :param use_handles: Handles, Use handles when converting Bézier curves into polygons
    :type use_handles: bool | None
    """

def spline_weight_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    weight: float | None = 1.0,
) -> None:
    """Set softbody goal weight for selected points

    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight: Weight
    :type weight: float | None
    """

def split(execution_context: int | str | None = None, undo: bool | None = None) -> None:
    """Split off selected points from connected unselected points

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
    """Subdivide selected segments

    :type execution_context: int | str | None
    :type undo: bool | None
    :param number_cuts: Number of Cuts
    :type number_cuts: int | None
    """

def switch_direction(
    execution_context: int | str | None = None, undo: bool | None = None
) -> None:
    """Switch direction of selected splines

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

def vertex_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
) -> None:
    """Add a new control point (linked to only selected end-curve one, if any)

    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location, Location to add new vertex at
    :type location: collections.abc.Sequence[float] | mathutils.Vector | None
    """
