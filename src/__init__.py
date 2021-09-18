# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

__version__ = "dev"

bl_info = {
    "name": "texture·design for Blender",
    "author": "texture·design",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    "location": "Properties > Material",
    "description": "Create materials and apply them to surfaces.",
    "tracker_url": "https://github.com/texturedesign/blender-addon/issues",
    "support": "COMMUNITY",
    "category": "Import",
}

import bpy.utils
import bpy.types


from .context import TextureProperties
from .operators import (
    OBJECT_OT_CreateMaterialFromPath,
    OBJECT_OT_CreateMaterialFromUUID,
    OBJECT_OT_ScanLocalDirectory
)
from .preferences import TexturePreferences
from .panel import MATERIAL_PT_DesignPanel

CLASSES = [
    TextureProperties,
    OBJECT_OT_CreateMaterialFromPath,
    OBJECT_OT_CreateMaterialFromUUID,
    OBJECT_OT_ScanLocalDirectory,
    TexturePreferences,
    MATERIAL_PT_DesignPanel,
]


def register():
    from bpy.props import PointerProperty

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.td_context = PointerProperty(type=TextureProperties)


def unregister():
    del bpy.types.WindowManager.td_context

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
