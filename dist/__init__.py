# MX Blackbody
# Copyright (C) 2022 Hendrik Meinl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name": "MX Blackbody",
    "description": "Kelvin to RGB converter",
    "author": "Hendrik Meinl",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > MX Blackbody",
    "doc_url": "https://github.com/maxgrafik/MXBlackbody",
    "tracker_url": "https://github.com/maxgrafik/MXBlackbody/issues",
    "category": "Lighting",
}

if "bpy" in locals():
    import importlib
    importlib.reload(globvars)
    importlib.reload(specrend)
    importlib.reload(panels)
else:
    from . import globvars, specrend, panels


import bpy


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

modules = (
    globvars,
    specrend,
    panels
)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
