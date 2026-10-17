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
# AgX desaturates greens; Standard keeps the leaf colour
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = -2.0
scene.render.filepath = out_path


def make_material(name, rgb, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def make_textured_material(name, color_a, color_b, scale, bump_strength, roughness, wave_bump=False):
    """Principled material with a noise-driven colour ramp and bump (leaf veining, frost)."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes.get("Principled BSDF")
    coords = nodes.new("ShaderNodeTexCoord")
    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.6
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*color_a, 1.0)
    ramp.color_ramp.elements[1].color = (*color_b, 1.0)
    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = bump_strength
    bump.inputs["Distance"].default_value = 0.002
    links.new(coords.outputs["Object"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    if wave_bump:
        # Diagonal wavy bands read as leaf veins
        wave = nodes.new("ShaderNodeTexWave")
        wave.wave_type = "BANDS"
        wave.bands_direction = "DIAGONAL"
        wave.inputs["Scale"].default_value = 35.0
        wave.inputs["Distortion"].default_value = 6.0
        wave.inputs["Detail"].default_value = 2.0
        links.new(wave.outputs["Fac"], bump.inputs["Height"])
    else:
        links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
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
core.data.materials.append(make_textured_material("FrozenBlue", (0.40, 0.65, 0.85), (0.66, 0.85, 0.96), scale=30.0, bump_strength=0.08, roughness=0.3))

# Leaf wrap (green), covers the lower 100 mm of the core
leaf = add_cylinder("LeafWrap", radius=0.0205, depth=0.100, z_center=0.050)
leaf.data.materials.append(make_textured_material("LeafGreen", (0.05, 0.20, 0.04), (0.16, 0.36, 0.08), scale=45.0, bump_strength=0.25, roughness=0.55, wave_bump=True))
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

# Rim light from behind, so the pop edges read against the grey backdrop
bpy.ops.object.light_add(type="AREA", location=(0.20, 0.30, 0.20))
rim = bpy.context.active_object
rim.data.energy = 6.0
rim.data.size = 0.15

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
