"""Hero product shot for the lime cube (working name: Plunk Lime Cube; sodium-free status pending, see 48 section 7.3).

Run headless from this folder (Blender 5.2, Cycles on CPU):

    blender.exe -b -P build_cube_scene.py -- --out cube_hero.png --samples 128

Options:
    --out PATH       output PNG (required)
    --label PATH     front artwork (default: label_front.png beside this script)
    --tokens PATH    style tokens (default: style_tokens.json beside this script)
    --width N        default 2560
    --height N       default 1440
    --samples N      default 128 (use 64 if a render would run past the time limit)

Scene: a single-serve pouch of the stated size and one lime compressed cube resting on the
same matte floor beside it, under soft three-point studio light. No glass, no water and no
bubbles are drawn. Glassware and bubble imagery are excluded on every occasion (48 section
3.3, decision D7, rule S2). Built only from Blender primitives and procedural node materials.
No downloaded textures and no network access. The .blend file is never saved. The PNG is
rewritten with every text chunk removed, so it carries no author, software or path data.

ASSUMPTION LIST. No value in this scene is SOURCED. Values read from style_tokens.json are
design choices and are marked ASSUMPTION there. DERIVED means arithmetic on those values or
on the stated assumptions in 48 section 6.1. Everything else is an ASSUMPTION: a design or
rendering choice with no measured or published source behind it.

A1  Pack width and height, 70 x 90 mm: ASSUMPTION (design choice), read from dimensions_mm
    in the tokens file (pack_w, pack_h). The 20 mm depth is an ASSUMPTION recorded there.
A2  Pouch: a pillow shape, 70 x 90 mm, 20 mm deep. Each face bulges from a flat seal flange 1 mm
    thick to 10 mm from the centre plane. The bulge rises over 6 mm from the side seals and 7 mm
    from the top and bottom seals. The seal crimp is simplified to that flange. ASSUMPTION (shape).
A3  Pouch film: off-white token, roughness 0.25, IOR 1.575 (PET, sourced), with a fine
    micro-texture. The label is printed on the front face only. The colours are ASSUMPTION
    (design choice).
A4  Front artwork: label_front.png wrapped over the whole front face, 70 x 90 mm. The artwork is
    1050 by 1350 px, the same portrait proportion, so it is not stretched; the script stops if the
    aspects differ. ASSUMPTION (layout).
A5  Cube: 15 mm side, DERIVED from ASSUMPTION inputs (48 section 6.1). Colour: lime token,
    ASSUMPTION (design choice). A 3 mm edge bevel in 6 segments and one level of subdivision give
    a pressed, rounded surface. Roughness 0.75 and a fine noise bump add a granular finish:
    ASSUMPTION. Rotated 18 degrees about Z only, so the
    base sits flat on the floor, its centre 7.5 mm above the floor, beside the pouch:
    ASSUMPTION (staging).
A6  Cyclorama and matte floor: background token colour, roughness 0.95, curve radius 120 mm.
    The colour is ASSUMPTION (design choice). The matte finish and the curve radius are
    ASSUMPTION. The world adds a soft fill at strength 0.25 in the background colour:
    ASSUMPTION.
A7  Lights: three soft square area lights (key, fill, rim). Powers and sizes are ASSUMPTION,
    tuned by eye for exposure. Nothing is measured.
A8  Camera: 85 mm lens on a 36 mm sensor, 4:3 frame, looking down about 14 degrees. ASSUMPTION
    (composition).
A9  Render: Cycles on CPU, Standard view transform, exposure -1.2 stops (ASSUMPTION, set by
    measuring the backdrop against the background token), OpenImageDenoise if the build
    provides it, caustics off, up to 32 light bounces. The colour is the scene colour, not a
    print or colour-proof match.

B. Rules applied to the content (see the brand style-matching note):
B1 Bubbles are not drawn. Bubble imagery is held back under rule S2 (carbonation is not
   measured).
B2 No glass is drawn. Glassware is excluded on every occasion (decision D7, 48 section 3.3).
   The brief asked for a clear tumbler. Keeping one needs rule 5 reopened in writing by the
   owner before judging. This script does not draw it.
B3 No organiser name, logo, emblem, wordmark or trademark is drawn. The only text in the scene
   is the front artwork, which comes from the label step.
"""

import argparse
import json
import math
import os
import struct
import sys
import time

import bmesh
import bpy
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 0.001  # the scene is built in metres; 1 mm = 0.001 m

PACK_X_MM = -38.0    # pouch centre, left of centre
CUBE_X_MM = 26.0     # cube centre, right of the pouch
CUBE_Z_MM = 7.5      # cube centre height: half the 15 mm side, so the base rests on the floor
TARGET_MM = (-20.0, 0.0, 60.0)      # centred on the pouch and the cube together
CAMERA_MM = (-20.0, -550.0, 200.0)
CAMERA_FRONT_MM = (-20.0, -520.0, 45.0)  # straight-on, at pack height
TARGET_FRONT_MM = (-20.0, 0.0, 45.0)
ARGS_VIEW = "front"  # set from the command line in main()


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(description="Build and render the lime cube hero shot.")
    p.add_argument("--out", required=True, help="output PNG path")
    p.add_argument("--label", default=os.path.join(HERE, "label_front.png"))
    p.add_argument("--tokens", default=os.path.join(HERE, "style_tokens.json"))
    p.add_argument("--width", type=int, default=2560)
    p.add_argument("--height", type=int, default=1440)
    p.add_argument("--samples", type=int, default=128)
    p.add_argument("--view", choices=["hero", "front"], default="front",
                   help="front: straight-on product view; hero: three-quarter composition")
    p.add_argument("--exposure", type=float, default=-1.2,
                   help="view exposure in stops, set so the backdrop matches the background token")
    p.add_argument("--device", choices=["cpu", "gpu"], default="gpu",
                   help="gpu (default): Cycles on the CUDA device; falls back to the CPU if none is found. cpu: CPU only")
    return p.parse_args(argv)


# ---------------------------------------------------------------- colour helpers

def hex_to_srgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_linear(h):
    return tuple(srgb_to_linear(c) for c in hex_to_srgb(h))


# ---------------------------------------------------------------- material helpers

def set_input(node, name, value):
    if name not in node.inputs:
        raise KeyError("input %r is missing on node %r" % (name, node.name))
    node.inputs[name].default_value = value


def principled(name, base_lin, roughness, extra=None):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (*base_lin, 1.0))
    set_input(bsdf, "Roughness", roughness)
    for key, value in (extra or {}).items():
        set_input(bsdf, key, value)
    return mat, bsdf


# ---------------------------------------------------------------- mesh helpers

def link(name, mesh, mat, smooth):
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    mesh.materials.append(mat)
    if smooth:
        for poly in mesh.polygons:
            poly.use_smooth = True
    return obj


def box_mesh(name, centre_mm, size_mm, bevel_mm=0.0, segments=3, rot_deg=(0.0, 0.0, 0.0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    sx, sy, sz = (s * MM for s in size_mm)
    for v in bm.verts:
        v.co = Vector((v.co.x * sx, v.co.y * sy, v.co.z * sz))
    if any(rot_deg):
        rot = Euler(tuple(math.radians(a) for a in rot_deg)).to_matrix()
        for v in bm.verts:
            v.co = rot @ v.co
    cx, cy, cz = (c * MM for c in centre_mm)
    for v in bm.verts:
        v.co = v.co + Vector((cx, cy, cz))
    if bevel_mm > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel_mm * MM, offset_type="OFFSET",
                        segments=segments, profile=0.5, affect="EDGES", clamp_overlap=True)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def cyclorama_mesh(name, half_width_m=1.2):
    """Floor, a curved cove and a back wall, extruded across X. Quads wind so normals face up and forward."""
    prof = [(-1.2, 0.0), (0.04, 0.0)]
    for k in range(1, 13):
        phi = (math.pi / 2) * k / 12.0
        prof.append((0.04 + 0.12 * math.sin(phi), 0.12 - 0.12 * math.cos(phi)))
    prof.append((0.16, 1.2))
    bm = bmesh.new()
    pairs = []
    for y, z in prof:
        pairs.append((bm.verts.new((-half_width_m, y, z)), bm.verts.new((half_width_m, y, z))))
    for i in range(len(pairs) - 1):
        (x0a, x1a), (x0b, x1b) = pairs[i], pairs[i + 1]
        bm.faces.new((x0a, x1a, x1b, x0b))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


# ---------------------------------------------------------------- scene parts

def build_materials(tok, label_img):
    col = tok["colour"]
    lin = {k: hex_linear(v) for k, v in col.items()}
    mats = {}

    # PET film: IOR 1.575 (isotropic average at about 589 nm; sourced, see MATERIALS_cube.md).
    # Laminate: PET outer (IOR 1.575, sourced) over a foil barrier, so the film carries a metallic sheen under the print.
    body_mat, body_bsdf = principled("PackFilm", lin["paper"], 0.25, {"IOR": 1.575, "Metallic": 0.35})
    # Fine micro-texture for a printed laminate (ASSUMPTION: strength and scale, no measured source).
    film_noise = body_mat.node_tree.nodes.new("ShaderNodeTexNoise")
    film_noise.inputs["Scale"].default_value = 1400.0
    film_noise.inputs["Detail"].default_value = 4.0
    film_bump = body_mat.node_tree.nodes.new("ShaderNodeBump")
    film_bump.inputs["Strength"].default_value = 0.07
    film_bump.inputs["Distance"].default_value = 0.0003
    body_mat.node_tree.links.new(film_noise.outputs["Fac"], film_bump.inputs["Height"])
    body_mat.node_tree.links.new(film_bump.outputs["Normal"], body_bsdf.inputs["Normal"])
    mats["body"] = body_mat
    # Rim (seal flange): aluminium foil layer with a PE sealant tint. ASSUMPTION colour; the foil is the visible barrier.
    mats["rim"] = principled("PackLaminateEdge", hex_linear("#C4C9CE"), 0.30, {"Metallic": 0.9, "IOR": 1.5})[0]

    label_mat, label_bsdf = principled("PackLabel", (1.0, 1.0, 1.0), 0.35)
    label_tex = label_mat.node_tree.nodes.new("ShaderNodeTexImage")
    label_tex.image = label_img
    label_mat.node_tree.links.new(label_tex.outputs["Color"], label_bsdf.inputs["Base Color"])
    # Ink build-up: the printed areas stand a few micrometres proud, shown as a faint relief from the artwork.
    ink_gray = label_mat.node_tree.nodes.new("ShaderNodeRGBToBW")
    ink_bump = label_mat.node_tree.nodes.new("ShaderNodeBump")
    ink_bump.inputs["Strength"].default_value = 0.03  # ASSUMPTION: relief strength, no measured source
    ink_bump.inputs["Distance"].default_value = 0.0002
    label_mat.node_tree.links.new(label_tex.outputs["Color"], ink_gray.inputs["Color"])
    label_mat.node_tree.links.new(ink_gray.outputs["Val"], ink_bump.inputs["Height"])
    label_mat.node_tree.links.new(ink_bump.outputs["Normal"], label_bsdf.inputs["Normal"])
    mats["label"] = label_mat

    # Compressed powder: matte, lightly granular, slight subsurface (ASSUMPTION, no measured source).
    cube_mat, cube_bsdf = principled("CubeLime", lin["lime"], 0.75,
                                     {"Subsurface Weight": 0.10,
                                      "Subsurface Radius": (0.003, 0.002, 0.0015)})
    noise = cube_mat.node_tree.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 260.0
    noise.inputs["Detail"].default_value = 6.0
    bump = cube_mat.node_tree.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.0005
    cube_mat.node_tree.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    cube_mat.node_tree.links.new(bump.outputs["Normal"], cube_bsdf.inputs["Normal"])
    mats["cube"] = cube_mat

    mats["cyc"] = principled("Cyclorama", hex_linear(tok["background"]), 0.95,
                             {"Specular IOR Level": 0.2})[0]
    return mats


PILLOW_EDGE_MM = 1.0     # ASSUMPTION: flange thickness at the seal line, each face
SEAL_SIDE_MM = 6.0       # ASSUMPTION: width over which a face bulges up from a side seal
SEAL_TOP_MM = 7.0        # ASSUMPTION: same, from the top and bottom seals
GRID_U, GRID_V = 60, 80  # mesh resolution across the width and the height of the pouch


def smooth01(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


def pillow_half_thickness(xd_mm, zd_mm, half_depth_mm):
    """Distance of a face from the centre plane, at xd_mm from the side seal and zd_mm from the top or bottom seal."""
    bulge = math.sqrt(smooth01(xd_mm / SEAL_SIDE_MM) * smooth01(zd_mm / SEAL_TOP_MM))
    return PILLOW_EDGE_MM + (half_depth_mm - PILLOW_EDGE_MM) * bulge


def pillow_mesh(name, w, h, half_depth, cx):
    """Closed pillow pouch: front and back faces bulge from a flat seal flange, joined by a rim.
    Material 1 (label) is the front face with UV 0..1 across the whole face; material 0 is the film."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    front, back, grid_uv = {}, {}, {}
    for i in range(GRID_U + 1):
        u = i / GRID_U
        xd = min(u, 1.0 - u) * w
        x = (cx + (u - 0.5) * w) * MM
        for j in range(GRID_V + 1):
            v = j / GRID_V
            zd = min(v, 1.0 - v) * h
            t = pillow_half_thickness(xd, zd, half_depth) * MM
            z = v * h * MM
            front[i, j] = bm.verts.new((x, -t, z))
            back[i, j] = bm.verts.new((x, t, z))
            grid_uv[front[i, j]] = (u, v)
    faces = []
    for i in range(GRID_U):
        for j in range(GRID_V):
            quad = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            faces.append(([front[k] for k in quad], 1))
            faces.append(([back[k] for k in quad], 0))
    ring = ([(i, 0) for i in range(GRID_U)] + [(GRID_U, j) for j in range(GRID_V)]
            + [(i, GRID_V) for i in range(GRID_U, 0, -1)] + [(0, j) for j in range(GRID_V, 0, -1)])
    for k, p in enumerate(ring):
        q = ring[(k + 1) % len(ring)]
        faces.append(([front[p], front[q], back[q], back[p]], 2))
    for verts, mat_index in faces:
        f = bm.faces.new(verts)
        f.material_index = mat_index
        if mat_index == 1:
            for loop in f.loops:
                loop[uv].uv = grid_uv[loop.vert]
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


def build_pack(tok, aspect, mats):
    dims = tok["dimensions_mm"]
    w = dims["pack_w"]["value"]
    h = dims["pack_h"]["value"]
    d = dims["pack_d"]["value"]
    if abs(aspect - w / h) > 0.005:
        raise SystemExit("label aspect %.4f does not match the pouch front %.4f" % (aspect, w / h))
    mesh = pillow_mesh("PackPouch", w, h, d / 2.0, PACK_X_MM)
    obj = bpy.data.objects.new("PackPouch", mesh)
    bpy.context.scene.collection.objects.link(obj)
    mesh.materials.append(mats["body"])   # slot 0: laminate film (back face)
    mesh.materials.append(mats["label"])  # slot 1: printed front face
    mesh.materials.append(mats["rim"])    # slot 2: foil and sealant rim
    for poly in mesh.polygons:
        poly.use_smooth = True
    print("pouch %.0f x %.0f mm, %.0f mm deep, label on the whole front face" % (w, h, d))


def build_cube(mats):
    cube = box_mesh("Cube", (CUBE_X_MM, 0.0, CUBE_Z_MM), (15.0, 15.0, 15.0),
                    bevel_mm=3.0, segments=6, rot_deg=(0.0, 0.0, 18.0))
    obj = link("Cube", cube, mats["cube"], smooth=True)
    sub = obj.modifiers.new("Round", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2


def build_cyclorama(mats):
    link("Cyclorama", cyclorama_mesh("Cyclorama"), mats["cyc"], smooth=False)


def aim(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_area(name, loc_m, size_m, energy_w):
    data = bpy.data.lights.new(name, type="AREA")
    data.shape = "SQUARE"
    data.size = size_m
    data.energy = energy_w
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = Vector(loc_m)
    aim(obj, (0.0, 0.0, 0.07))
    return obj


def build_lights():
    # Three-point studio set-up. Powers and sizes are ASSUMPTION, tuned for exposure.
    add_area("KeyLight", (-0.35, -0.55, 0.45), 0.5, 12.0)
    add_area("FillLight", (0.45, -0.45, 0.30), 0.8, 4.0)
    add_area("RimLight", (0.15, 0.40, 0.45), 0.3, 8.0)


def build_camera():
    data = bpy.data.cameras.new("Camera")
    data.lens = 85.0
    data.sensor_width = 36.0
    cam = bpy.data.objects.new("Camera", data)
    bpy.context.scene.collection.objects.link(cam)
    if ARGS_VIEW == "front":
        cam.location = Vector(tuple(c * MM for c in CAMERA_FRONT_MM))
        aim(cam, tuple(c * MM for c in TARGET_FRONT_MM))
    else:
        cam.location = Vector(tuple(c * MM for c in CAMERA_MM))
        aim(cam, tuple(c * MM for c in TARGET_MM))
    bpy.context.scene.camera = cam


def build_world(scene, bg_hex):
    world = bpy.data.worlds.new("Studio")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    set_input(bg, "Color", (*hex_linear(bg_hex), 1.0))
    set_input(bg, "Strength", 0.25)  # ASSUMPTION: soft fill only
    scene.world = world


def strip_png_text(path):
    """Rewrite the PNG keeping only the critical and colour-space chunks. Text chunks go."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError("output is not a PNG")
    keep = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"gAMA", b"sRGB", b"pHYs"}
    out = [data[:8]]
    removed = []
    pos = 8
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos:pos + 12 + length]
        if ctype in keep:
            out.append(chunk)
        else:
            removed.append(ctype.decode("ascii", "replace"))
        pos += 12 + length
        if ctype == b"IEND":
            break
    with open(path, "wb") as fh:
        fh.write(b"".join(out))
    print("PNG chunks removed:", removed if removed else "none")


def setup_render(scene, args, bg_hex):
    scene.render.engine = "CYCLES"
    cy = scene.cycles
    cy.device = "GPU" if args.device == "gpu" else "CPU"
    if args.device == "gpu":
        # Enable the CUDA device and no other; the CPU stays available for the host work.
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "CUDA"
        prefs.get_devices()
        if any(dev.type == "CUDA" for dev in prefs.devices):
            for dev in prefs.devices:
                dev.use = dev.type == "CUDA"
            print("GPU devices in use:", [dev.name for dev in prefs.devices if dev.use])
        else:
            cy.device = "CPU"
            print("No CUDA device found; rendering on the CPU")
    cy.samples = args.samples
    cy.use_adaptive_sampling = True
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except TypeError as exc:
        print("denoiser not set:", exc)
    cy.caustics_reflective = False
    cy.caustics_refractive = False
    cy.max_bounces = 32
    cy.transmission_bounces = 32
    try:
        scene.view_layers[0].cycles.use_denoising = True
    except AttributeError:
        pass

    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = args.exposure
    scene.view_settings.gamma = 1.0

    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    try:
        scene.render.use_stamp = False
    except AttributeError:
        pass

    img = scene.render.image_settings
    img.file_format = "PNG"
    img.color_mode = "RGB"
    img.color_depth = "8"
    img.compression = 15
    build_world(scene, bg_hex)


def main():
    global ARGS_VIEW
    args = parse_args()
    ARGS_VIEW = args.view
    t0 = time.time()
    with open(args.tokens, encoding="utf-8") as fh:
        tok = json.load(fh)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene

    label_img = bpy.data.images.load(os.path.abspath(args.label), check_existing=True)
    aspect = label_img.size[0] / float(label_img.size[1])
    print("label artwork %dx%d, aspect %.3f" % (label_img.size[0], label_img.size[1], aspect))

    mats = build_materials(tok, label_img)
    build_cyclorama(mats)
    build_pack(tok, aspect, mats)
    build_cube(mats)
    build_lights()
    build_camera()
    setup_render(scene, args, tok["background"])

    out_path = os.path.abspath(args.out)
    scene.render.filepath = out_path
    print("rendering %dx%d, %d samples, %s" % (args.width, args.height, args.samples, args.device.upper()))
    bpy.ops.render.render(write_still=True)
    strip_png_text(out_path)
    print("done in %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
