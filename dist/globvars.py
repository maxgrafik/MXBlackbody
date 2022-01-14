import bpy


# ------------------------------------------------------------------------
#    Globals
# ------------------------------------------------------------------------

class MXBlackbody(bpy.types.PropertyGroup):

    def updateColor(self, context):
        bpy.ops.mxblackbody.get_rgb_color()

    preset: bpy.props.StringProperty(
        name = "Preset",
        default = "Presets",
        update = updateColor
        )

    color_system: bpy.props.StringProperty(
        name = "Color System",
        default = "CIE Rec. 709",
        update = updateColor
        )

    temperature: bpy.props.IntProperty(
        name = "Kelvin",
        min=1000,
        max=12000,
        step=100,
        default = 6500,
        update = updateColor
        )

    rgb_color: bpy.props.FloatVectorProperty(
        name = "RGB Color",
        subtype='COLOR',
        size=3,
        default=(1.0, 0.968879, 0.995617)
        )


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MXBlackbody,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.MXBlackbody = bpy.props.PointerProperty(type=MXBlackbody)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.MXBlackbody
