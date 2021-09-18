# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import io
import os
import zipfile
from urllib.request import urlopen

import bpy
import bpy.types



class OBJECT_OT_ScanLocalDirectory(bpy.types.Operator):

    bl_idname = "td.scan"
    bl_label = "Scan Materials"
    bl_description = "Re-scan the local directory."

    def execute(self, context):
        return {"FINISHED"}


def loadImageCached(path, colorspace="Linear", default=None):
    if os.path.isfile(path):
        image = bpy.data.images.load(path, check_existing=True)
        image.colorspace_settings.name = colorspace
        return image
    else:
        assert default is not None
        image = bpy.data.images.new(os.path.split(path)[-1], 1, 1)
        image.colorspace_settings.name = colorspace
        image.pixels.foreach_set((default, default, default, 1.0))
        return image


def create_material(base_path, name="Material_4K"):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    principle_node = material.node_tree.nodes["Principled BSDF"]
    output_node = material.node_tree.nodes["Material Output"]

    occlusion_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    occlusion_node.location = (-1080, 400)
    occlusion_node.image = loadImageCached(os.path.join(base_path, "occlusion.jpg"), "sRGB", 1.0)
    occlusion_node.name = "Ambient Occlusion"

    albedo_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    albedo_node.location = (-680, 387)
    albedo_node.image = loadImageCached(os.path.join(base_path, "diffuse.jpg"), "sRGB")
    albedo_node.name = "Diffuse Color"

    displacement_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    displacement_node.location = (20, -388)
    displacement_node.image = loadImageCached(os.path.join(base_path, "displacement.jpg"), default=0.5)
    displacement_node.name = "Displacement"

    normal_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    normal_node.location = (-680, -388)
    normal_node.image = loadImageCached(os.path.join(base_path, "normal.jpg"))
    normal_node.name = "Normal"

    roughness_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    roughness_node.location = (-680, -130)
    roughness_node.image = loadImageCached(os.path.join(base_path, "roughness.jpg"), default=0.5)
    roughness_node.name = "Roughness"

    specular_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    specular_node.location = (-680, 135)
    specular_node.name = "Specularity"
    specular_node.image = loadImageCached(os.path.join(base_path, "specular.jpg"), default=0.0)

    valToRGB_node = material.node_tree.nodes.new("ShaderNodeValToRGB")
    valToRGB_node.location = (-680, 627)

    mixRGB_node = material.node_tree.nodes.new("ShaderNodeMixRGB")
    mixRGB_node.location = (-343, 559)
    mixRGB_node.blend_type = "MULTIPLY"
    mixRGB_node.inputs[0].default_value = 1.0

    normalMap_node = material.node_tree.nodes.new("ShaderNodeNormalMap")
    normalMap_node.location = (-327, -262)

    material.node_tree.links.new(occlusion_node.outputs[0], valToRGB_node.inputs[0])
    material.node_tree.links.new(valToRGB_node.outputs[0], mixRGB_node.inputs[2])
    material.node_tree.links.new(albedo_node.outputs[0], mixRGB_node.inputs[1])
    material.node_tree.links.new(mixRGB_node.outputs[0], principle_node.inputs[0])
    material.node_tree.links.new(specular_node.outputs[0], principle_node.inputs[7])
    material.node_tree.links.new(roughness_node.outputs[0], principle_node.inputs[9])
    material.node_tree.links.new(normal_node.outputs[0], normalMap_node.inputs[1])
    material.node_tree.links.new(normalMap_node.outputs[0], principle_node.inputs[22])
    material.node_tree.links.new(displacement_node.outputs[0], output_node.inputs[2])

    bpy.context.object.material_slots[0].material = material


class OBJECT_OT_CreateMaterialFromPath(bpy.types.Operator):

    bl_idname = "td.create_from_path"
    bl_label = "Create Material From Path"
    bl_description = "Create a new material from specified path."

    def execute(self, context):
        td_context = context.window_manager.td_context
        base_path = td_context.material_path
        create_material(base_path)
        return {"FINISHED"}


def download_material(root_path, material_uuid):
    tmp_dir = os.path.join(root_path, "." + material_uuid)
    target_dir = os.path.join(root_path, material_uuid)

    if os.path.isdir(target_dir):
        return

    response = urlopen(f"https://dl.texture.design/v2/{material_uuid}/4K-JPG.zip")
    archive = zipfile.ZipFile(io.BytesIO(response.read()))

    archive.extractall(tmp_dir)

    os.rename(tmp_dir, target_dir)


class OBJECT_OT_CreateMaterialFromUUID(bpy.types.Operator):

    bl_idname = "td.create_from_uuid"
    bl_label = "Create Material From UUID"
    bl_description = "Create a new material from specified UUID."

    def execute(self, context):
        td_context = context.window_manager.td_context
        td_prefs = context.preferences.addons[__package__].preferences

        root_path = os.path.realpath(td_prefs.material_path)
        mat_uuid = td_context.material_uuid.strip("\t ")

        mat_path = os.path.join(root_path, mat_uuid, "4K-JPG")
        if not os.path.isdir(mat_path):
            download_material(root_path, mat_uuid)

        create_material(mat_path)
        return {"FINISHED"}
