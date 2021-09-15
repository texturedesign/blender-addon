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
    from bpy.props import EnumProperty, BoolProperty, FloatProperty
    from .preferences import AddonPreferences

    WindowManager.td_resolution = EnumProperty(
        name = "Resolution",
        items = [
            ("1k", "1k", "1k", 1),
            ("2k", "2k", "2k", 2),
        ],
        # update = changeResolution,
    )

    WindowManager.td_isDownloading = BoolProperty(
        default = False,
    )

    WindowManager.td_DownloadProcess= FloatProperty(
        default = 0,
        min = 0.0,
        max = 100.0,
        soft_min = 0.0,
        soft_max = 100.0,
        name = "Downloading..."
    )

    bpy.utils.register_class(AddonPreferences)


def unregister():
    import bpy.utils
    from bpy.types import WindowManager
    from .preferences import AddonPreferences

    del WindowManager.td_isDownloading
    del WindowManager.td_DownloadProcess
    del WindowManager.td_resolution

    bpy.utils.unregister_class(AddonPreferences)


if __name__ == "__main__":
    register()
