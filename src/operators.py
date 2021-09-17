# blender-addon — Copyright (c) 2021, texture·design.  See LICENSE for details.

import os
import bpy
import bpy.types


class OBJECT_OT_ScanLocalDirectory(bpy.types.Operator):

    bl_idname = "td.scan"
    bl_label = "Scan Materials"
    bl_description = "Re-scan the local directory."

    def execute(self, context):
        return {"FINISHED"}


def loadImageCached(path, colorspace="Linear"):
    for image in bpy.data.images:
        if os.path.abspath(image.filepath) == os.path.abspath(path):
            return image
    
    image = bpy.data.images.load(path)
    image.colorspace_settings.name = colorspace
    return image


class OBJECT_OT_CreateMaterial(bpy.types.Operator):

    bl_idname = "td.create"
    bl_label = "Create Material"
    bl_description = "Create a new material from the brief."

    def execute(self, context):
        td_context = context.window_manager.td_context
        base_path = td_context.material_path

        material = bpy.data.materials.new(name=f"Material_2K")
        material.use_nodes = True

        principle_node = material.node_tree.nodes["Principled BSDF"]
        output_node = material.node_tree.nodes["Material Output"]

        occlusion_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        occlusion_node.location = (-1080, 400)
        occlusion_node.image = loadImageCached(os.path.join(base_path, "occlusion.jpg"), "sRGB")
        occlusion_node.name = "Ambient Occlusion"

        albedo_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        albedo_node.location = (-680, 387)
        albedo_node.image = loadImageCached(os.path.join(base_path, "albedo.jpg"), "sRGB")
        albedo_node.name = "Diffuse Color"

        displacement_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        displacement_node.location = (0, -388)
        displacement_node.image = loadImageCached(os.path.join(base_path, "height.jpg"))
        displacement_node.name = "Displacement"

        normal_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        normal_node.location = (-680, -388)
        normal_node.image = loadImageCached(os.path.join(base_path, "normal.jpg"))
        normal_node.name = "Normal"

        roughness_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        roughness_node.location = (-680, -130)
        roughness_node.image = loadImageCached(os.path.join(base_path, "roughness.jpg"))
        roughness_node.name = "Roughness"

        specular_node = material.node_tree.nodes.new("ShaderNodeTexImage")
        specular_node.location = (-680, 135)
        specular_node.name = "Specularity"
        specular_node.image = loadImageCached(os.path.join(base_path, "specular.jpg"))

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

        return {"FINISHED"}
