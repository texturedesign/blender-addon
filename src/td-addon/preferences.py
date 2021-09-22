# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import os
import bpy.types
import bpy.props


class TexturePreferences(bpy.types.AddonPreferences):
    bl_idname = "texturedesign"

    material_path: bpy.props.StringProperty(
        description = "Material Path",
        subtype = "DIR_PATH",
        default = os.path.realpath(os.path.expanduser("~/Documents/texture·design"))
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "material_path")

        row = layout.row()
        row.operator("td.scan")
