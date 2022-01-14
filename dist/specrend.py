import bpy
import math
from .definitions import *


# ------------------------------------------------------------------------
#    Functions
# ------------------------------------------------------------------------

def upvp_to_xy(up, vp):
    xc = (9 * up) / ((6 * up) - (16 * vp) + 12)
    yc = (4 * vp) / ((6 * up) - (16 * vp) + 12)
    return xc, yc

def xy_to_upvp(xc, yc):
    up = (4 * xc) / ((-2 * xc) + (12 * yc) + 3)
    vp = (9 * yc) / ((-2 * xc) + (12 * yc) + 3)
    return up, vp

def xyz_to_rgb(cs, xc, yc, zc):
    xr = cs[0] # xRed
    yr = cs[1] # yRed
    zr = 1 - (xr + yr)

    xg = cs[2] # xGreen
    yg = cs[3] # yGreen
    zg = 1 - (xg + yg)

    xb = cs[4] # xBlue
    yb = cs[5] # yBlue
    zb = 1 - (xb + yb)

    xw = cs[6][0] # xWhite
    yw = cs[6][1] # yWhite
    zw = 1 - (xw + yw)

    rx = (yg * zb) - (yb * zg)
    ry = (xb * zg) - (xg * zb)
    rz = (xg * yb) - (xb * yg)

    gx = (yb * zr) - (yr * zb)
    gy = (xr * zb) - (xb * zr)
    gz = (xb * yr) - (xr * yb)

    bx = (yr * zg) - (yg * zr)
    by = (xg * zr) - (xr * zg)
    bz = (xr * yg) - (xg * yr)

    rw = ((rx * xw) + (ry * yw) + (rz * zw)) / yw
    gw = ((gx * xw) + (gy * yw) + (gz * zw)) / yw
    bw = ((bx * xw) + (by * yw) + (bz * zw)) / yw

    rx = rx / rw
    ry = ry / rw
    rz = rz / rw

    gx = gx / gw
    gy = gy / gw
    gz = gz / gw

    bx = bx / bw
    by = by / bw
    bz = bz / bw

    r = (rx * xc) + (ry * yc) + (rz * zc)
    g = (gx * xc) + (gy * yc) + (gz * zc)
    b = (bx * xc) + (by * yc) + (bz * zc)

    return r, g, b


def inside_gamut(r, g, b):
    return (r >= 0) and (g >= 0) and (b >= 0)


def constrain_rgb(r, g, b):
    w = 0 if 0 < r else r
    w = w if w < g else g
    w = w if w < b else b
    w = -w;

    if (w > 0):
        r += w
        g += w
        b += w

    return r, g, b


def gamma_correct(cs, c):
    gamma = cs[7]

    if (gamma == GAMMA_REC709):
        cc = 0.018
        if (c < cc):
            c *= ((1.099 * math.pow(cc, 0.45)) - 0.099) / cc
        else:
            c = (1.099 * math.pow(c, 0.45)) - 0.099
    else:
        c = math.pow(c, 1.0 / gamma)

    return c


def gamma_correct_rgb(cs, r, g, b):
    r = gamma_correct(cs, r)
    g = gamma_correct(cs, g)
    b = gamma_correct(cs, b)

    return r, g, b


def norm_rgb(r, g, b):
    greatest = max(r, max(g, b))

    if (greatest > 0):
        r = r / greatest
        g = g / greatest
        b = b / greatest

    return r, g, b


def bb_spectrum(wavelength, bbTemp):
    wlm = wavelength * 1e-9
    return (3.74183e-16 * math.pow(wlm, -5.0)) / (math.exp(1.4388e-2 / (wlm * bbTemp)) - 1.0)


def spectrum_to_xyz(bbTemp):
    X = Y = Z = i = 0

    for l in range(380, 785, 5):
        Me = bb_spectrum(l, bbTemp)
        X += Me * CIE_Colour_Match[i][0]
        Y += Me * CIE_Colour_Match[i][1]
        Z += Me * CIE_Colour_Match[i][2]
        i += 1

    XYZ = (X + Y + Z)
    x = X / XYZ
    y = Y / XYZ
    z = Z / XYZ

    return x, y, z


# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------

class MXBLACKBODY_OT_getRGBColor(bpy.types.Operator):
    bl_label = "Get RGB Color"
    bl_idname = "mxblackbody.get_rgb_color"

    def execute(self, context):
        MXBlackbody = context.scene.MXBlackbody

        tmp = MXBlackbody.temperature
        cs = ColorSystems.get(MXBlackbody.color_system)

        x, y, z = spectrum_to_xyz(tmp)
        r, g, b = xyz_to_rgb(cs, x, y, z)
        r, g, b = constrain_rgb(r, g, b)
        r, g, b = norm_rgb(r, g, b)
        r, g, b = gamma_correct_rgb(cs, r, g, b)

        MXBlackbody.rgb_color = (r, g, b)

        return {'FINISHED'}


class MXBLACKBODY_OT_setColorSystem(bpy.types.Operator):
    bl_label = "Set Color System"
    bl_idname = "mxblackbody.set_color_system"

    color_system: bpy.props.StringProperty(
        name = "Color System Name",
        default = "CIE Rec. 709"
    )

    def execute(self, context):
        MXBlackbody = context.scene.MXBlackbody
        MXBlackbody.color_system = self.color_system
        return {'FINISHED'}


class MXBLACKBODY_OT_setBBTemp(bpy.types.Operator):
    bl_label = "Set Blackbody Temperature"
    bl_idname = "mxblackbody.set_bb_temp"

    preset: bpy.props.StringProperty(
        name = "Preset Name",
        default = ""
    )

    def execute(self, context):
        MXBlackbody = context.scene.MXBlackbody
        MXBlackbody.preset = self.preset
        MXBlackbody.temperature = Presets.get(self.preset)
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MXBLACKBODY_OT_getRGBColor,
    MXBLACKBODY_OT_setColorSystem,
    MXBLACKBODY_OT_setBBTemp,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
