"""Lemon Soda product visuals, rendered with Cycles (Blender 5.2) for the presentation mocks.

Run headless from this folder:

    blender.exe -b -P render_lemon_cube.py -- --variant whole --out product_whole.png

Variants:
    whole       one compressed lemon cube, 14 mm side scaled, on a matte floor
    fragments   the cube broken into ten pieces on the same floor
    residue     three small pieces left after the cube has broken up

Scope: no glass, no water and no bubbles are drawn (anti-slop filter; glassware is held
until the Gate 7 ruling, see rework/submission/12 and rework/48). The floor and the world
use the slide background colour, so the render sits flat on the slide.

Materials are procedural Principled BSDF networks: a granular noise bump, a noise-driven
roughness map, a satin coat and a small subsurface term for a pressed tablet. No downloaded
textures and no network access.
"""
import sys
import math
import random
import argparse

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--variant", choices=["whole", "fragments", "residue"], default="whole")
    p.add_argument("--out", required=True)
    p.add_argument("--width", type=int, default=960)
    p.add_argument("--height", type=int, default=720)
    p.add_argument("--samples", type=int, default=48)
    return p.parse_args(argv)


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_linear(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), 1.0)


def set_gpu(scene):
    scene.cycles.device = "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "CUDA"
        prefs.get_devices()
        used = False
        for d in prefs.devices:
            if d.type != "CPU":
                d.use = True
                used = True
        if used:
            scene.cycles.device = "GPU"
    except Exception as e:  # fall back to CPU, and say so in the log
        print("GPU setup failed, using CPU:", e)


def lemon_material(name="LemonCube"):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes["Principled BSDF"]

    def inp(n, key, default=None):
        return n.inputs[key]

    bsdf.inputs["Base Color"].default_value = hex_linear("#F7D23A")
    bsdf.inputs["Roughness"].default_value = 0.45
    for key, value in [("Coat Weight", 0.25), ("Coat Roughness", 0.2), ("Specular IOR Level", 0.45),
                       ("Subsurface Weight", 0.06)]:
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = value
    if "Subsurface Radius" in bsdf.inputs:
        bsdf.inputs["Subsurface Radius"].default_value = (0.012, 0.008, 0.003)

    # Granular surface: a fine noise drives both the bump and the roughness.
    tex = nodes.new("ShaderNodeTexNoise")
    tex.inputs["Scale"].default_value = 160.0
    tex.inputs["Detail"].default_value = 9.0
    tex.inputs["Roughness"].default_value = 0.62
    mapr = nodes.new("ShaderNodeMapRange")
    mapr.inputs["From Min"].default_value = 0.0
    mapr.inputs["From Max"].default_value = 1.0
    mapr.inputs["To Min"].default_value = 0.42
    mapr.inputs["To Max"].default_value = 0.68
    links.new(tex.outputs["Fac"], mapr.inputs["Value"])
    links.new(mapr.outputs["Result"], bsdf.inputs["Roughness"])

    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.10
    bump.inputs["Distance"].default_value = 0.004
    links.new(tex.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def floor_material(bg_hex):
    mat = bpy.data.materials.new("Floor")
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hex_linear(bg_hex)
    b.inputs["Roughness"].default_value = 0.95
    return mat


def bevelled_cube(name, side, loc, rot, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (side / 2, side / 2, side / 2)
    obj.rotation_euler = rot
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = 0.14
    bev.segments = 6
    bev.limit_method = "ANGLE"
    sub = obj.modifiers.new("Subdivision", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(mat)
    return obj


def add_area(name, loc, size, energy, target):
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.size = size
    direction = Vector(target) - Vector(loc)
    light.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def main():
    args = parse_args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    set_gpu(scene)
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    try:
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = -0.35

    bg = "#F6F4EE"
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    wb = world.node_tree.nodes["Background"]
    wb.inputs["Color"].default_value = hex_linear(bg)
    wb.inputs["Strength"].default_value = 0.55
    scene.world = world

    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.data.materials.append(floor_material(bg))

    lemon = lemon_material()
    rng = random.Random(20261020)

    if args.variant == "whole":
        bevelled_cube("LemonCube", 1.4, (0, 0, 0.7), (0.0, 0.0, math.radians(18)), lemon)
        target = (0, 0, 0.55)
        cam_loc = (2.2, -3.0, 3.6)
    elif args.variant == "fragments":
        for i in range(10):
            s = rng.uniform(0.32, 0.46)
            loc = (rng.uniform(-0.9, 0.9), rng.uniform(-0.8, 0.8), s / 2)
            rot = (rng.uniform(0, 1.2), rng.uniform(0, 1.2), rng.uniform(0, 3.1))
            bevelled_cube(f"Piece{i}", s, loc, rot, lemon)
        target = (0, 0, 0.25)
        cam_loc = (2.2, -2.8, 3.4)
    else:  # residue
        for i in range(3):
            s = rng.uniform(0.10, 0.16)
            loc = (rng.uniform(-0.35, 0.35), rng.uniform(-0.3, 0.3), s / 2)
            rot = (rng.uniform(0, 1.2), rng.uniform(0, 1.2), rng.uniform(0, 3.1))
            bevelled_cube(f"Residue{i}", s, loc, rot, lemon)
        target = (0, 0, 0.1)
        cam_loc = (1.6, -2.0, 2.4)

    add_area("Key", (2.6, -2.4, 3.6), 3.0, 230, (0, 0, 0.5))
    add_area("Fill", (-3.2, -1.6, 2.2), 3.5, 70, (0, 0, 0.5))
    add_area("Rim", (-1.8, 3.4, 2.6), 2.2, 110, (0, 0, 0.5))

    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.data.lens = 70
    cam.data.dof.use_dof = False
    direction = Vector(target) - Vector(cam_loc)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam

    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    scene.render.filepath = args.out
    print("rendering", args.variant, args.width, "x", args.height, "samples", args.samples, "device", scene.cycles.device)
    bpy.ops.render.render(write_still=True)
    print("saved", args.out)


if __name__ == "__main__":
    main()
