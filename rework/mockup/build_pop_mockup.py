"""Build and render a schematic 3D mockup of the leaf-wrapped frozen pop.

Run headless:
  blender -b -P build_pop_mockup.py -- <label_png> <output_png>

Dimensions are assumptions (see rework/08_pop_label_dieline.svg notes):
  core radius 19 mm, leaf radius 20.5 mm, label band radius 20.85 mm (131 mm wide),
  leaf height 100 mm, core height 150 mm. Not measured; replace with prototype dimensions.
"""
import math
import sys

import bpy

argv = sys.argv
args = argv[argv.index("--") + 1:] if "--" in argv else []
if len(args) < 2:
    raise SystemExit("usage: blender -b -P build_pop_mockup.py -- <label_png> <output_png>")
label_path, out_path = args[0], args[1]

# Clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Render settings (Cycles, CPU, moderate samples for a quick schematic)
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 96
scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = out_path


def make_material(name, rgb, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True


def add_cylinder(name, radius, depth, z_center, fill="NGON", verts=72):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=depth,
        location=(0.0, 0.0, z_center), end_fill_type=fill,
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


# Frozen core (blue), with rounded ends
core = add_cylinder("Core", radius=0.0190, depth=0.150, z_center=0.075)
bevel = core.modifiers.new("Bevel", "BEVEL")
bevel.width = 0.006
bevel.segments = 6
smooth(core)
core.data.materials.append(make_material("FrozenBlue", (0.45, 0.70, 0.88), roughness=0.25))

# Leaf wrap (green), covers the lower 100 mm of the core
leaf = add_cylinder("LeafWrap", radius=0.0205, depth=0.100, z_center=0.050)
leaf.data.materials.append(make_material("LeafGreen", (0.13, 0.36, 0.08), roughness=0.6))
smooth(leaf)

# Label band (dieline artwork), 60 mm tall, 131 mm around
label_radius = 0.131 / (2 * math.pi)
band = add_cylinder("LabelBand", radius=label_radius, depth=0.060, z_center=0.050, fill="NOTHING")
label_mat = bpy.data.materials.new("LabelMat")
label_mat.use_nodes = True
nt = label_mat.node_tree
bsdf = nt.nodes.get("Principled BSDF")
bsdf.inputs["Roughness"].default_value = 0.35
img_node = nt.nodes.new("ShaderNodeTexImage")
img_node.image = bpy.data.images.load(label_path)
nt.links.new(img_node.outputs["Color"], bsdf.inputs["Base Color"])
band.data.materials.append(label_mat)
smooth(band)
# Turn the label so the front panel (left of the label) faces the camera
band.rotation_euler = (0.0, 0.0, math.radians(107))

# Ground
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, 0.0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (0.5, 0.5, 1.0)
ground.data.materials.append(make_material("Ground", (0.85, 0.85, 0.85), roughness=0.9))

# Lights
bpy.ops.object.light_add(type="SUN", location=(0.3, -0.3, 0.5))
sun = bpy.context.active_object
sun.data.energy = 1.5
sun.rotation_euler = (math.radians(50), 0.0, math.radians(35))

bpy.ops.object.light_add(type="AREA", location=(-0.15, -0.20, 0.20))
area = bpy.context.active_object
area.data.energy = 25.0
area.data.size = 0.20

# World
world = bpy.data.worlds.new("World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.6, 0.6, 0.6, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
scene.world = world

# Camera, tracking a target at the middle of the pop
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0.0, 0.0, 0.075))
target = bpy.context.active_object
target.name = "Target"

bpy.ops.object.camera_add(location=(0.36, -0.43, 0.17))
cam = bpy.context.active_object
cam.name = "Camera"
cam.data.lens = 85
track = cam.constraints.new("TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
scene.camera = cam

bpy.ops.render.render(write_still=True)
print("MOCKUP_WRITTEN", out_path)
