# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import bpy.props
import bpy.types


class TextureProperties(bpy.types.PropertyGroup):
    """Container for all the properties used by this addon.  It can be accessed from
    `context.window_manager`.
    """

    material_brief: bpy.props.StringProperty(
        name="Brief",
        description="Describe your material with words",
        default=""
    )

    material_path: bpy.props.StringProperty(
        name="Path",
        description="Location from which to load material",
        subtype="DIR_PATH",
        default=""
    )

    material_uuid: bpy.props.StringProperty(
        name="UUID",
        description="UUID of material to load",
        default=""
    )
