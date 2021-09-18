# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import bpy.types


class MATERIAL_PT_DesignPanel(bpy.types.Panel):
    bl_label = "Design"
    bl_idname = "MATERIAL_PT_DesignPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        td_context = context.window_manager.td_context

        row = layout.row()
        row.label(text="Browse path for material.")

        row = layout.row()
        row.prop(td_context, "material_path")

        row = layout.row()
        row.operator("td.create_from_path")

        layout.separator()
        row = layout.row()
        row.label(text="Enter UUID of a material.")

        row = layout.row()
        row.prop(td_context, "material_uuid")

        row = layout.row()
        row.operator("td.create_from_uuid")
