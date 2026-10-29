"""Lemon Soda deck images P1 to P6, rendered with Cycles (Blender 5.2) on the GPU, 4K, transparent.

Run headless, one image per Blender process (keeps memory low):

    blender.exe -b -P render_deck_images.py -- --id P3 --out-dir ./out

Ids and canvases (long side 3840 px, aspect = the Canva frame it fills):
    P1  4:5   cover, one cube, lower centre, empty space above   (3072 x 3840)
    P2  4:3   executive summary, one cube, centred               (3840 x 2880)
    P3  4:3   slide 6 phase 1, one whole cube, ~40% of height    (3840 x 2880)
    P4  4:3   slide 6 phase 2, ten fragments broken from a cube   (3840 x 2880)
    P5  4:3   slide 6 phase 3, three very small fragments         (3840 x 2880)
    P6  4:1   slide 12, row of five cubes in flavour colours      (3840 x  960)

The background is removed: film_transparent is on and the PNG is RGBA. With --shadow 1 (default)
the floor is a shadow catcher, so the soft contact shadow stays in the alpha channel and the image
sits flat on the slide paper tone (#F6F4EE). With --shadow 0 the floor is invisible to the camera
and the PNG is the bare cut-out of the cubes.

Scope (rework/deck/image_placeholders.md): no glass, water, bubbles, fizz, fruit, bottle, can,
alcohol cue, text or logo. The cube is a pressed tablet, 14 mm, satin matte, granular, rounded edges.
Materials are procedural (no downloaded textures, no network). 1 Blender unit = 10 mm, so the cube
side is 1.4 units.
"""
import sys
import math
import random
import argparse

import bpy
import bmesh
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

CUBE = 1.4  # side in Blender units (14 mm)

SPECS = {
    "P1": dict(name="P1_cover", aspect=(4, 5), kind="whole", az=33, el=28, yaw=8,
               fit=dict(h=0.30, w=None, c=(0.5, 0.31))),
    "P2": dict(name="P2_exec_summary", aspect=(4, 3), kind="whole", az=33, el=27, yaw=8,
               fit=dict(h=0.46, w=None, c=(0.5, 0.50))),
    "P3": dict(name="P3_phase1_cube", aspect=(4, 3), kind="whole", az=33, el=27, yaw=8,
               fit=dict(h=0.40, w=None, c=(0.5, 0.50))),
    "P4": dict(name="P4_phase2_fragments", aspect=(4, 3), kind="fragments", count=10, az=22, el=36,
               fit=dict(h=0.62, w=0.74, c=(0.5, 0.50))),
    "P5": dict(name="P5_phase3_residue", aspect=(4, 3), kind="fragments", count=3, az=22, el=34,
               fit=dict(h=0.26, w=0.34, c=(0.5, 0.50))),
    "P6": dict(name="P6_flavour_row", aspect=(4, 1), kind="row", az=0, el=20, yaw=24,
               fit=dict(h=0.62, w=0.86, c=(0.5, 0.50))),
}

FLAVOURS = ["#F7D23A", "#E9DC7B", "#C8453B", "#8E5A7C", "#E9A3B4"]  # lemon, yuzu, red, ume, pink
PAPER = "#F6F4EE"


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, choices=sorted(SPECS))
    p.add_argument("--out-dir", required=True)
    p.add_argument("--long", type=int, default=3840, help="long side in pixels")
    p.add_argument("--samples", type=int, default=192)
    p.add_argument("--shadow", type=int, default=1, help="1 keeps the soft contact shadow in the alpha")
    p.add_argument("--device", choices=["gpu", "cpu"], default="gpu")
    p.add_argument("--seed", type=int, default=20261021)
    p.add_argument("--exposure", type=float, default=-0.15)
    p.add_argument("--suffix", default="")
    p.add_argument("--save-blend", default="")
    return p.parse_args(argv)


# ----------------------------------------------------------------------------- colour helpers
def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def hex_linear(h, mix_white=0.0, mix_black=0.0):
    r, g, b = (srgb_to_linear(c) for c in hex_rgb(h))
    r, g, b = (c + (1 - c) * mix_white for c in (r, g, b))
    r, g, b = (c * (1 - mix_black) for c in (r, g, b))
    return (r, g, b, 1.0)


# ----------------------------------------------------------------------------- device
def set_device(scene, want):
    scene.cycles.device = "CPU"
    if want != "gpu":
        return "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "CUDA"
        prefs.get_devices()
        used = False
        for d in prefs.devices:
            d.use = (d.type == "CUDA")
            used = used or d.use
        if used:
            scene.cycles.device = "GPU"
            return "GPU CUDA"
    except Exception as e:
        print("GPU setup failed, using CPU:", e)
    return "CPU"


# ----------------------------------------------------------------------------- material
def tablet_material(name, hex_colour):
    """Pressed powder tablet: grain bump, roughness mottling, soft colour variation, sheen."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes, links = nt.nodes, nt.links
    bsdf = nodes["Principled BSDF"]

    def setv(key, value):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = value

    setv("Metallic", 0.0)
    setv("IOR", 1.45)
    setv("Specular IOR Level", 0.38)
    setv("Coat Weight", 0.05)
    setv("Coat Roughness", 0.35)
    setv("Sheen Weight", 0.16)
    setv("Sheen Roughness", 0.55)
    setv("Subsurface Weight", 0.12)
    setv("Subsurface Scale", 0.03)
    if "Subsurface Radius" in bsdf.inputs:
        bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.6, 0.25)

    # per-object random offset so pieces of one material do not repeat the same grain
    texco = nodes.new("ShaderNodeTexCoord")
    objinfo = nodes.new("ShaderNodeObjectInfo")
    rnd = nodes.new("ShaderNodeMath")
    rnd.operation = "MULTIPLY"
    rnd.inputs[1].default_value = 57.0
    links.new(objinfo.outputs["Random"], rnd.inputs[0])
    comb = nodes.new("ShaderNodeCombineXYZ")
    for i in range(3):
        links.new(rnd.outputs[0], comb.inputs[i])
    mapping = nodes.new("ShaderNodeMapping")
    links.new(texco.outputs["Object"], mapping.inputs["Vector"])
    links.new(comb.outputs["Vector"], mapping.inputs["Location"])

    def noise(scale, detail, rough):
        n = nodes.new("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value = scale
        n.inputs["Detail"].default_value = detail
        n.inputs["Roughness"].default_value = rough
        links.new(mapping.outputs["Vector"], n.inputs["Vector"])
        return n

    fine = noise(240.0, 6.0, 0.66)      # grain, 4 to 8 px at 2K, large enough to survive the denoiser
    medium = noise(70.0, 6.0, 0.62)     # coarser granules
    cloud = noise(9.0, 3.0, 0.50)       # slow colour drift across the face

    vor = nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "F1"
    vor.inputs["Scale"].default_value = 150.0
    links.new(mapping.outputs["Vector"], vor.inputs["Vector"])

    # colour: two tones of the flavour colour driven by the slow cloud and the fine grain
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = hex_linear(hex_colour, mix_black=0.025)
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = hex_linear(hex_colour, mix_white=0.03)
    links.new(cloud.outputs["Fac"], ramp.inputs["Fac"])
    # grey grain mask: speckle in the colour itself (the denoiser keeps colour detail, it smooths bump)
    grain_grey = nodes.new("ShaderNodeValToRGB")
    grain_grey.color_ramp.elements[0].position = 0.38
    grain_grey.color_ramp.elements[0].color = (0.45, 0.45, 0.45, 1.0)
    grain_grey.color_ramp.elements[1].position = 0.62
    grain_grey.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(fine.outputs["Fac"], grain_grey.inputs["Fac"])
    grain_tone = nodes.new("ShaderNodeMix")
    grain_tone.data_type = "RGBA"
    grain_tone.blend_type = "MULTIPLY"
    grain_tone.inputs[0].default_value = 0.42
    links.new(ramp.outputs["Color"], grain_tone.inputs[6])
    links.new(grain_grey.outputs["Color"], grain_tone.inputs[7])
    links.new(grain_tone.outputs[2], bsdf.inputs["Base Color"])
    if "Sheen Tint" in bsdf.inputs:
        bsdf.inputs["Sheen Tint"].default_value = hex_linear(hex_colour, mix_white=0.35)
    if "Subsurface Radius" in bsdf.inputs:
        pass

    # roughness: mottled, satin
    mapr = nodes.new("ShaderNodeMapRange")
    mapr.inputs["To Min"].default_value = 0.52
    mapr.inputs["To Max"].default_value = 0.80
    links.new(medium.outputs["Fac"], mapr.inputs["Value"])
    links.new(mapr.outputs["Result"], bsdf.inputs["Roughness"])

    # normal: rounded-edge bevel, then fine grain, medium granules and shallow pits
    bevel = nodes.new("ShaderNodeBevel")
    bevel.inputs["Radius"].default_value = 0.012
    bevel.samples = 6
    b1 = nodes.new("ShaderNodeBump")
    b1.inputs["Strength"].default_value = 0.55
    b1.inputs["Distance"].default_value = 0.006
    links.new(fine.outputs["Fac"], b1.inputs["Height"])
    links.new(bevel.outputs["Normal"], b1.inputs["Normal"])
    b2 = nodes.new("ShaderNodeBump")
    b2.inputs["Strength"].default_value = 0.30
    b2.inputs["Distance"].default_value = 0.008
    links.new(medium.outputs["Fac"], b2.inputs["Height"])
    links.new(b1.outputs["Normal"], b2.inputs["Normal"])
    b3 = nodes.new("ShaderNodeBump")
    b3.inputs["Strength"].default_value = 0.16
    b3.inputs["Distance"].default_value = 0.006
    links.new(vor.outputs["Distance"], b3.inputs["Height"])
    links.new(b2.outputs["Normal"], b3.inputs["Normal"])
    links.new(b3.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


# ----------------------------------------------------------------------------- geometry
def finish_object(obj, mat, bevel_w, seed_tex):
    """Bevel, smooth, slight surface irregularity, material."""
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = bevel_w
    bev.segments = 6
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(25)
    sub = obj.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    disp = obj.modifiers.new("Irregular", "DISPLACE")
    disp.texture = seed_tex
    disp.strength = 0.0022
    disp.mid_level = 0.5
    disp.texture_coords = "OBJECT"
    for poly in obj.data.polygons:
        poly.use_smooth = True
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def make_cube(name, side, loc, yaw_deg, mat, tex):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=side)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (0, 0, math.radians(yaw_deg))
    finish_object(obj, mat, side * 0.062, tex)
    return obj


def make_fragment(name, ref, rng, mat, tex):
    """A chunk broken from the cube: a box of random size with a few chipped corners, convex."""
    dx, dy, dz = (ref * rng.uniform(0.62, 1.0) for _ in range(3))
    corners = [Vector((sx * dx / 2, sy * dy / 2, sz * dz / 2)) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    chipped = rng.sample(range(8), rng.randint(2, 4))
    pts = []
    for i, c in enumerate(corners):
        if i in chipped:
            c = c * rng.uniform(0.52, 0.78)
        pts.append(c + Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * ref * 0.03)
    bm = bmesh.new()
    verts = [bm.verts.new(p) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=verts)
    interior = res.get("geom_interior", [])
    unused = res.get("geom_unused", [])
    bmesh.ops.delete(bm, geom=[g for g in interior + unused if getattr(g, "is_valid", True)], context="VERTS")
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    finish_object(obj, mat, ref * 0.07, tex)
    return obj


def evaluated_zrange(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    eo = obj.evaluated_get(dg)
    me = eo.to_mesh()
    mw = eo.matrix_world
    zs = [(mw @ v.co).z for v in me.vertices]
    eo.to_mesh_clear()
    return min(zs), max(zs)


def rest_on_floor(obj):
    """Shift so the lowest point of the evaluated mesh touches z = 0."""
    bpy.context.view_layer.update()
    zmin, _ = evaluated_zrange(obj)
    obj.location.z -= zmin
    bpy.context.view_layer.update()


def settle(objs, frames=140):
    """Drop the fragments on a slab with rigid-body physics so they rest in natural poses."""
    scene = bpy.context.scene
    bpy.ops.rigidbody.world_add()
    rbw = scene.rigidbody_world
    rbw.point_cache.frame_start = 1
    rbw.point_cache.frame_end = frames
    rbw.substeps_per_frame = 20
    rbw.solver_iterations = 40
    slab = bpy.data.objects.get("Floor")
    for o in [slab] + objs:
        with bpy.context.temp_override(object=o, active_object=o, selected_objects=[o]):
            bpy.ops.rigidbody.object_add(type="PASSIVE" if o is slab else "ACTIVE")
    slab.rigid_body.collision_shape = "BOX"
    slab.rigid_body.friction = 0.9
    slab.rigid_body.restitution = 0.0
    for o in objs:
        rb = o.rigid_body
        rb.collision_shape = "CONVEX_HULL"
        rb.mass = 1.0
        rb.friction = 0.85
        rb.restitution = 0.03
        rb.linear_damping = 0.30
        rb.angular_damping = 0.45
        rb.collision_margin = 0.002
    for f in range(1, frames + 1):
        scene.frame_set(f)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    final = {o.name: o.evaluated_get(dg).matrix_world.copy() for o in objs}
    bpy.ops.rigidbody.world_remove()
    scene.frame_set(1)
    for o in objs:
        o.matrix_world = final[o.name]
    bpy.context.view_layer.update()


def scatter_positions(rng, n, area, radii):
    """n well-separated xy positions; the spacing rule relaxes until every piece is placed."""
    for spacing in (1.35, 1.2, 1.05, 0.9, 0.75):
        pos = []
        for _ in range(4000):
            if len(pos) == n:
                break
            p = Vector((rng.uniform(-area[0], area[0]), rng.uniform(-area[1], area[1]), 0))
            i = len(pos)
            if all((p - q).length > (radii[i] * 0.6 + radii[j] * 0.6) * spacing for j, q in enumerate(pos)):
                pos.append(p)
        if len(pos) == n:
            return pos
    raise RuntimeError("could not place %d fragments" % n)


# ----------------------------------------------------------------------------- camera and light
def subject_points(objs):
    pts = []
    for o in objs:
        pts += [o.matrix_world @ v.co for v in o.data.vertices]
    return pts


def aim(obj, loc, target):
    obj.location = loc
    obj.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def frame_camera(scene, cam, pts, az, el, fit):
    W, H = scene.render.resolution_x, scene.render.resolution_y
    maxdim = max(W, H)
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    cen = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2))
    a, e = math.radians(az), math.radians(el)
    direction = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    extent = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs), CUBE)
    d = extent * 14.0
    sx = sy = 0.0
    tw, th, (tcx, tcy) = fit["w"], fit["h"], fit["c"]
    for _ in range(14):
        cam.data.shift_x, cam.data.shift_y = sx, sy
        aim(cam, cen + direction * d, cen)
        bpy.context.view_layer.update()
        vs = [world_to_camera_view(scene, cam, p) for p in pts]
        x0, x1 = min(v.x for v in vs), max(v.x for v in vs)
        y0, y1 = min(v.y for v in vs), max(v.y for v in vs)
        w, h = x1 - x0, y1 - y0
        ratio = max(w / tw if tw else 0.0, h / th if th else 0.0)
        d *= ratio ** 0.9
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        sx += -(tcx - cx) * (W / maxdim) * 0.8
        sy += -(tcy - cy) * (H / maxdim) * 0.8
    cam.data.shift_x, cam.data.shift_y = sx, sy
    aim(cam, cen + direction * d, cen)
    bpy.context.view_layer.update()
    vs = [world_to_camera_view(scene, cam, p) for p in pts]
    print("framed: bbox w=%.3f h=%.3f centre=(%.3f, %.3f) distance=%.2f" % (
        max(v.x for v in vs) - min(v.x for v in vs), max(v.y for v in vs) - min(v.y for v in vs),
        (max(v.x for v in vs) + min(v.x for v in vs)) / 2, (max(v.y for v in vs) + min(v.y for v in vs)) / 2, d))
    return cen, extent


def add_area(name, loc, size, energy, target, colour=(1, 1, 1)):
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.size = size
    light.data.color = colour
    light.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return light


def three_point(cen, extent):
    k = max(extent, CUBE) / CUBE
    c = Vector(cen)
    # only the key casts a shadow, so the floor carries one soft contact shadow instead of three
    add_area("Key", c + Vector((-2.2, -2.2, 4.2)) * k, 3.4 * k, 175 * k * k, c, (1.0, 0.985, 0.955))
    fill = add_area("Fill", c + Vector((3.4, -1.8, 2.0)) * k, 3.6 * k, 55 * k * k, c, (0.96, 0.98, 1.0))
    rim = add_area("Rim", c + Vector((1.2, 3.6, 2.8)) * k, 2.4 * k, 95 * k * k, c)
    fill.data.use_shadow = False
    rim.data.use_shadow = False


# ----------------------------------------------------------------------------- main
def main():
    args = parse_args()
    spec = SPECS[args.id]
    rng = random.Random(args.seed + int(args.id[1:]))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    device = set_device(scene, args.device)
    cy = scene.cycles
    cy.samples = args.samples
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.01
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
        cy.denoising_prefilter = "ACCURATE"
    except Exception:
        pass
    try:
        cy.denoising_use_gpu = (device != "CPU")
    except Exception:
        pass
    cy.max_bounces = 8
    cy.diffuse_bounces = 4
    cy.glossy_bounces = 4
    cy.transmission_bounces = 2
    cy.caustics_reflective = False
    cy.caustics_refractive = False
    cy.sample_clamp_indirect = 4.0
    try:
        cy.tile_size = 2048
    except Exception:
        pass
    cy.seed = args.seed

    aw, ah = spec["aspect"]
    if aw >= ah:
        W, H = args.long, round(args.long * ah / aw)
    else:
        W, H = round(args.long * aw / ah), args.long
    scene.render.resolution_x, scene.render.resolution_y = W, H
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.filter_size = 1.2
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = args.exposure

    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    wb = world.node_tree.nodes["Background"]
    wb.inputs["Color"].default_value = hex_linear(PAPER)
    wb.inputs["Strength"].default_value = 0.80
    scene.world = world

    # floor slab: shadow catcher (shadow variant) or invisible bounce card (cut-out variant)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -1.0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.scale = (300, 300, 2.0)
    fm = bpy.data.materials.new("FloorMat")
    fm.use_nodes = True
    fb = fm.node_tree.nodes["Principled BSDF"]
    fb.inputs["Base Color"].default_value = hex_linear(PAPER)
    fb.inputs["Roughness"].default_value = 0.95
    floor.data.materials.append(fm)
    if args.shadow:
        floor.is_shadow_catcher = True
    else:
        floor.visible_camera = False

    tex = bpy.data.textures.new("Irregular", "CLOUDS")
    tex.noise_scale = 0.22
    tex.noise_depth = 2

    subject = []
    if spec["kind"] == "whole":
        mat = tablet_material("Lemon", FLAVOURS[0])
        cube = make_cube("Cube", CUBE, (0, 0, CUBE / 2), spec["yaw"], mat, tex)
        rest_on_floor(cube)
        subject = [cube]
    elif spec["kind"] == "row":
        spacing = CUBE * 2.55
        for i, hx in enumerate(FLAVOURS):
            mat = tablet_material("Flavour%d" % i, hx)
            x = (i - 2) * spacing
            cube = make_cube("Cube%d" % i, CUBE, (x, 0, CUBE / 2), spec["yaw"], mat, tex)
            rest_on_floor(cube)
            subject.append(cube)
    else:
        mat = tablet_material("Lemon", FLAVOURS[0])
        n = spec["count"]
        if n == 10:
            refs = [CUBE * rng.uniform(0.27, 0.50) for _ in range(n)]
            area = (2.7, 1.8)
        else:
            refs = [CUBE * rng.uniform(0.13, 0.19) for _ in range(n)]
            area = (0.62, 0.42)
        pos = scatter_positions(rng, n, area, refs)
        for i, (ref, p) in enumerate(zip(refs, pos)):
            frag = make_fragment("Piece%d" % i, ref, rng, mat, tex)
            frag.location = (p.x, p.y, ref * 0.9 + rng.uniform(0.02, 0.35))
            frag.rotation_euler = (rng.uniform(0, 6.28), rng.uniform(0, 6.28), rng.uniform(0, 6.28))
            subject.append(frag)
        settle(subject)
        for o in subject:
            zmin, zmax = evaluated_zrange(o)
            if -0.02 < zmin < 0.06:
                o.location.z -= zmin
        bpy.context.view_layer.update()
        for o in subject:
            zmin, zmax = evaluated_zrange(o)
            print("piece %s at (%.2f, %.2f) z %.3f..%.3f" % (o.name, o.location.x, o.location.y, zmin, zmax))

    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    cam.data.lens = 85
    cam.data.sensor_width = 36
    cam.data.clip_start = 0.1
    cam.data.clip_end = 600
    scene.camera = cam
    cen, extent = frame_camera(scene, cam, subject_points(subject), spec["az"], spec["el"], spec["fit"])
    three_point(cen, extent)

    out = "%s/%s_%dx%d%s%s.png" % (args.out_dir.rstrip("/\\"), spec["name"], W, H,
                                   "" if args.shadow else "_noshadow", args.suffix)
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 15
    scene.render.filepath = out
    if args.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=args.save_blend)
    print("rendering", args.id, W, "x", H, "samples", args.samples, "device", device, "shadow", args.shadow)
    bpy.ops.render.render(write_still=True)
    print("saved", out)


if __name__ == "__main__":
    main()
