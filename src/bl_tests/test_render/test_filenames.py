import bpy


def test_one():
    bpy.ops.mcr.render('INVOKE_DEFAULT', animation=False)
