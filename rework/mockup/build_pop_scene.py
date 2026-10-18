"""Schematic 3D product scene for the leaf-wrapped frozen pop: still and marketing video.

Run headless:
  blender -b -P build_pop_scene.py -- still  <label_png> <out_png>  <width> <height> <samples>
  blender -b -P build_pop_scene.py -- video  <label_png> <out_mp4>  <width> <height> <samples> <frames>

Dimensions are assumptions (see rework/08_pop_label_dieline.svg notes):
  core radius 19 mm, leaf radius 20.5 mm, label band radius 20.85 mm (131 mm around),
  leaf height 100 mm, core height 150 mm. Not measured; replace with prototype dimensions.

Renders with Cycles on the GPU (CUDA) when available, otherwise CPU. Denoised.

Materials use public CC0 textures (ambientCG Leaf001, Ice002, Paper002; 1K maps in textures/) and
published optical values (ice index, coconut-milk colour). Sources and assumptions: MATERIALS.md.
"""
import math
import os
import sys

import bpy

argv = sys.argv
args = argv[argv.index("--") + 1:] if "--" in argv else []
if len(args) < 6:
    raise SystemExit("usage: see module docstring")
mode, label_path, out_path = args[0], args[1], args[2]
width, height, samples = int(args[3]), int(args[4]), int(args[5])
frames = int(args[6]) if len(args) > 6 else 1

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Cycles on the GPU when CUDA is available; fall back to CPU
scene.render.engine = "CYCLES"
gpu_ok = False
try:
    cprefs = bpy.context.preferences.addons["cycles"].preferences
    cprefs.compute_device_type = "CUDA"
    cprefs.get_devices()
    for dev in cprefs.devices:
        dev.use = dev.type in ("CUDA", "CPU")
    gpu_ok = any(d.type == "CUDA" and d.use for d in cprefs.devices)
except Exception as exc:  # noqa: BLE001
    print("GPU setup failed, using CPU:", exc)
scene.cycles.device = "GPU" if gpu_ok else "CPU"
print("CYCLES DEVICE:", scene.cycles.device)
scene.cycles.samples = samples
scene.cycles.use_denoising = os.environ.get("POP_DENOISE", "1") == "1"
scene.cycles.denoiser = "OPENIMAGEDENOISE"
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.render.resolution_x = width
scene.render.resolution_y = height
scene.render.resolution_percentage = 100

# Filmic-neutral colour so greens keep their saturation
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = -2.0


def set_input(bsdf, name, value):
    if name in bsdf.inputs:
        bsdf.inputs[name].default_value = value


def base_material(name, rgb, roughness, **extras):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*rgb, 1.0))
    set_input(bsdf, "Roughness", roughness)
    for key, value in extras.items():
        set_input(bsdf, key, value)
    return mat


# Sourced values and their assumptions are listed in rework/mockup/MATERIALS.md
TEX_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "textures")
FROZEN_BASE_SRGB = (0.7937, 0.7860, 0.7376)  # coconut milk: Hunter L 80.6, b 6.4 (sourced); a -1.5 assumed; sRGB, D65
ICE_IOR = 1.311                              # ice Ih at 550 nm, Warren and Brandt (2008), sourced


def tex(pack, name):
    return os.path.join(TEX_DIR, pack, name)


def image_node(nt, path, colorspace):
    node = nt.nodes.new("ShaderNodeTexImage")
    node.image = bpy.data.images.load(path, check_existing=True)
    node.image.colorspace_settings.name = colorspace
    return node


def normal_from_map(nt, bsdf, path, strength):
    img = image_node(nt, path, "Non-Color")
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.inputs["Strength"].default_value = strength
    nt.links.new(img.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])


def leaf_material():
    """Leaf wrap: interior crop of a CC0 leaf photo (ambientCG Leaf001) for colour, roughness and normal."""
    mat = bpy.data.materials.new("LeafWrap")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    colour = image_node(nt, tex("leaf001", "Leaf001_Color_interior512.jpg"), "sRGB")
    nt.links.new(colour.outputs["Color"], bsdf.inputs["Base Color"])
    rough = image_node(nt, tex("leaf001", "Leaf001_Roughness_interior512.jpg"), "Non-Color")
    nt.links.new(rough.outputs["Color"], bsdf.inputs["Roughness"])
    normal_from_map(nt, bsdf, tex("leaf001", "Leaf001_NormalGL_interior512.jpg"), 0.6)
    # ASSUMPTION: no sourced leaf transmittance; translucency is set by hand
    set_input(bsdf, "Subsurface Weight", 0.25)
    set_input(bsdf, "Subsurface Radius", (0.2, 0.4, 0.1))
    set_input(bsdf, "Subsurface Scale", 0.004)
    return mat


def frozen_drink_material():
    """Frozen coconut-pandan core: sourced ice index and coconut-milk colour, ice normal and roughness."""
    mat = bpy.data.materials.new("FrozenDrink")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*FROZEN_BASE_SRGB, 1.0))
    set_input(bsdf, "IOR", ICE_IOR)
    rough = image_node(nt, tex("ice002", "Ice002_Roughness_1K.jpg"), "Non-Color")
    nt.links.new(rough.outputs["Color"], bsdf.inputs["Roughness"])
    normal_from_map(nt, bsdf, tex("ice002", "Ice002_NormalGL_1K.jpg"), 0.3)
    # ASSUMPTION: transmission and subsurface are not sourced for a frozen drink
    set_input(bsdf, "Transmission Weight", 0.35)
    set_input(bsdf, "Subsurface Weight", 0.10)
    set_input(bsdf, "Subsurface Radius", (0.4, 0.7, 1.0))
    return mat


def label_material(artwork_path):
    """Printed label: artwork as colour; CC0 paper roughness and fibre normal (ambientCG Paper002)."""
    mat = bpy.data.materials.new("LabelPaper")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    art = image_node(nt, artwork_path, "sRGB")
    nt.links.new(art.outputs["Color"], bsdf.inputs["Base Color"])
    rough = image_node(nt, tex("paper002", "Paper002_Roughness_1K.jpg"), "Non-Color")
    nt.links.new(rough.outputs["Color"], bsdf.inputs["Roughness"])
    normal_from_map(nt, bsdf, tex("paper002", "Paper002_NormalGL_1K.jpg"), 0.2)
    return mat


def smooth(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True


def add_cylinder(name, radius, depth, z_center, fill="NGON", verts=96):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts, radius=radius, depth=depth,
        location=(0.0, 0.0, z_center), end_fill_type=fill,
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


# Frozen core: translucent ice-like drink, rounded ends
core = add_cylinder("Core", radius=0.0190, depth=0.150, z_center=0.075)
core_bevel = core.modifiers.new("Bevel", "BEVEL")
core_bevel.width = 0.006
core_bevel.segments = 8
smooth(core)
core.data.materials.append(frozen_drink_material())

# Leaf wrap: CC0 leaf photo for colour, roughness and normal
leaf = add_cylinder("LeafWrap", radius=0.0205, depth=0.100, z_center=0.050)
smooth(leaf)
leaf.data.materials.append(leaf_material())

# Label band: paper with the dieline artwork
label_radius = 0.131 / (2 * math.pi)
band = add_cylinder("LabelBand", radius=label_radius, depth=0.060, z_center=0.050, fill="NOTHING")
band.rotation_euler = (0.0, 0.0, math.radians(107))
smooth(band)
band.data.materials.append(label_material(label_path))

# Studio ground and cyclorama backdrop
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, 0.0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.scale = (2.0, 2.0, 1.0)
ground.data.materials.append(base_material("Ground", (0.82, 0.82, 0.82), 0.85))

# Lights: soft key, soft fill, rim
bpy.ops.object.light_add(type="SUN", location=(0.3, -0.3, 0.5))
sun = bpy.context.active_object
sun.data.energy = 1.5
sun.data.angle = math.radians(6.0)
sun.rotation_euler = (math.radians(50), 0.0, math.radians(35))

bpy.ops.object.light_add(type="AREA", location=(-0.20, -0.25, 0.25))
key = bpy.context.active_object
key.data.energy = 20.0
key.data.size = 0.25

bpy.ops.object.light_add(type="AREA", location=(0.20, 0.30, 0.20))
rim = bpy.context.active_object
rim.data.energy = 6.0
rim.data.size = 0.15

# World: neutral grey studio light
world = bpy.data.worlds.new("World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.6, 0.6, 0.6, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
scene.world = world

# Camera and target
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0.0, 0.0, 0.075))
target = bpy.context.active_object
target.name = "Target"
# Same start as the video's first key (0.75 m, 300 deg, z 0.13): a 16:9 frame that keeps the whole pop
bpy.ops.object.camera_add(location=(0.375, -0.6495, 0.13))
cam = bpy.context.active_object
cam.name = "Camera"
cam.data.lens = 85
cam.data.dof.use_dof = True
cam.data.dof.focus_object = target
cam.data.dof.aperture_fstop = 4.0
track = cam.constraints.new("TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
scene.camera = cam


def orbit_point(theta_deg, radius, z):
    t = math.radians(theta_deg)
    return (radius * math.cos(t), radius * math.sin(t), z)


if mode == "still":
    scene.frame_start = scene.frame_end = 1
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print("STILL_WRITTEN", out_path)

elif mode == "video":
    # Keyframed camera: orbit (frames 1-72), macro push-in on the leaf (73-120), pull-out (121-end)
    # 16:9 frame: 0.75 m keeps the full 150 mm pop in view; macro uses f/8 so the leaf stays sharp
    keys = [
        (1,      300, 0.75, 0.13, (0.0, 0.0, 0.075), 5.6),
        (72,     390, 0.75, 0.13, (0.0, 0.0, 0.075), 5.6),
        (96,     390, 0.20, 0.10, (0.0, 0.0, 0.070), 16.0),
        (120,    410, 0.20, 0.09, (0.0, 0.0, 0.070), 16.0),
        (frames, 450, 0.85, 0.15, (0.0, 0.0, 0.075), 5.6),
    ]
    # Sample the path densely (every 4 frames, eased) so the orbit follows the arc,
    # not the straight chord between sparse keys, which pulls the camera inward.
    def smooth(t):
        return t * t * (3.0 - 2.0 * t)

    dense = []
    for (f0, th0, r0, z0, _look0, s0), (f1, th1, r1, z1, _look1, s1) in zip(keys[:-1], keys[1:]):
        for f in list(range(f0, f1, 4)) + [f1]:
            t = smooth((f - f0) / float(f1 - f0))
            dense.append((f,
                          th0 + (th1 - th0) * t,
                          r0 + (r1 - r0) * t,
                          z0 + (z1 - z0) * t,
                          s0 + (s1 - s0) * t))
    seen = set()
    for frame, theta, radius, z, fstop in dense:
        if frame in seen:
            continue
        seen.add(frame)
        cam.location = orbit_point(theta, radius, z)
        cam.keyframe_insert(data_path="location", frame=frame)
        if fstop > 6:
            # Macro: focus on the label surface facing the camera, not the axis
            look = (0.0208 * math.cos(math.radians(theta)), 0.0208 * math.sin(math.radians(theta)), 0.070)
        else:
            look = (0.0, 0.0, 0.075)
        target.location = look
        target.keyframe_insert(data_path="location", frame=frame)
        cam.data.dof.aperture_fstop = fstop
        cam.data.dof.keyframe_insert(data_path="aperture_fstop", frame=frame)
    # POP_FRAME_START lets an interrupted render resume at the first missing frame
    scene.frame_start = int(os.environ.get("POP_FRAME_START", "1"))
    scene.frame_end = frames
    scene.render.fps = 24
    if out_path.endswith("_"):
        # PNG sequence for frame review: out_path like ".../frame_"
        scene.render.image_settings.file_format = "PNG"
    else:
        # Blender 5.x: video is a media type, not an image file format
        if hasattr(scene.render, "media_type"):
            scene.render.media_type = "VIDEO"
        else:
            scene.render.image_settings.file_format = "FFMPEG"
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.ffmpeg.constant_rate_factor = "HIGH"
    scene.render.filepath = out_path
    bpy.ops.render.render(animation=True)
    print("VIDEO_WRITTEN", out_path)

else:
    raise SystemExit("mode must be 'still' or 'video'")
