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


def register():
    import bpy.utils
    from bpy.types import WindowManager
    from bpy.props import PointerProperty

    from .context import TextureProperties
    from .preferences import TexturePreferences
    from .panel import Material_PT_DesignPanel

    bpy.utils.register_class(TexturePreferences)
    bpy.utils.register_class(TextureProperties)
    bpy.utils.register_class(Material_PT_DesignPanel)

    WindowManager.td_context = PointerProperty(type=TextureProperties)


def unregister():
    import bpy.utils
    from bpy.types import WindowManager

    del WindowManager.td_context

    from .context import TextureProperties
    from .preferences import TexturePreferences
    from .panel import Material_PT_DesignPanel

    bpy.utils.unregister_class(Material_PT_DesignPanel)
    bpy.utils.register_class(TextureProperties)
    bpy.utils.unregister_class(TexturePreferences)


if __name__ == "__main__":
    register()
