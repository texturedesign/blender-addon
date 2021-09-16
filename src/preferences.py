# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import bpy.types
import bpy.props


class TexturePreferences(bpy.types.AddonPreferences):
    bl_idname = "texturedesign"

    local_path: bpy.props.StringProperty(
        description = "Local Path",
        subtype = "DIR_PATH",
        default = "//Materials"
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "local_path")

        row = layout.row()
        row.operator("td.scan")
