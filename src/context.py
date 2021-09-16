# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import bpy.props
import bpy.types


class TextureProperties(bpy.types.PropertyGroup):
    """Container for all the properties used by this addon.  It can be accessed from
    `context.window_manager`.
    """

    user_request: bpy.props.StringProperty(
        name="Brief",
        description="Describe your material with words.",
        default=""
    )
