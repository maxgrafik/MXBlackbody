import bpy
from .definitions import ColorSystems, Presets


# ------------------------------------------------------------------------
#    Panels
# ------------------------------------------------------------------------

class VIEW3D_PT_MXBlackbodyPanel(bpy.types.Panel):
    bl_label = "MX Blackbody"
    bl_idname = "VIEW3D_PT_MXBlackbodyPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MX Blackbody"

    def draw(self, context):
        MXBlackbody = context.scene.MXBlackbody

        layout = self.layout

        row = layout.row()
        row.menu("MXBLACKBODY_MT_preset", text = MXBlackbody.preset)

        row = layout.row()
        row.menu("MXBLACKBODY_MT_colorSystem", text = MXBlackbody.color_system)

        row = layout.row()
        row.prop(MXBlackbody, "temperature")

        row = layout.row()
        row.prop(MXBlackbody, "rgb_color", text = "")


# ------------------------------------------------------------------------
#    UI
# ------------------------------------------------------------------------

class MXBLACKBODY_MT_colorSystem(bpy.types.Menu):
    """Color System for conversion"""
    bl_label = "Color Systems"
    bl_idname = "MXBLACKBODY_MT_colorSystem"

    def draw(self, context):
        layout = self.layout

        for cs in ColorSystems:
            op = layout.operator("mxblackbody.set_color_system", text = cs)
            op.color_system = cs


class MXBLACKBODY_MT_preset(bpy.types.Menu):
    """Common blackbody temperatures"""
    bl_label = "Presets"
    bl_idname = "MXBLACKBODY_MT_preset"

    def draw(self, context):
        layout = self.layout

        for p in Presets:
            op = layout.operator("mxblackbody.set_bb_temp", text = p)
            op.preset = p


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MXBLACKBODY_MT_preset,
    MXBLACKBODY_MT_colorSystem,
    VIEW3D_PT_MXBlackbodyPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
