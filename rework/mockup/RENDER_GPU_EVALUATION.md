# Rendering on the local GPU (19 October 2026)

Status: measured on this machine, 19 October 2026. Two test sizes, one run each for the GPU. No repeats.

## 1. Hardware and software

- GPU: NVIDIA GeForce GTX 1650, 4 GB VRAM, driver 617.42 (from `nvidia-smi`), compute capability 7.5. The card has no RT cores.
- CPU: AMD Ryzen 5 5500U. RAM: 8 GB total, about 7.5 GB visible.
- Blender 5.2.2 LTS, headless. Cycles lists the CUDA device. OptiX is listed too, but without RT cores CUDA is the right choice. The HIP warning is for AMD and is harmless here.

## 2. Results (same scene, same settings, same script)

| Test | CPU | GPU (CUDA) | Image difference, GPU against CPU |
|---|---|---|---|
| 960 by 540, 32 samples | 29.4 s (this session) | 8.1 s | mean 0.0, largest 9 of 255 |
| 2560 by 1440, 64 samples | 291 s and 369 s (earlier runs) | 83.4 s | mean 0.0, largest 5 of 255 |

The 2K CPU time comes from earlier runs, not from the same session. The GPU is about 3.5 times faster at 2K, and about 3.6 times faster at the preview size.

## 3. Memory

- **Host RAM is the binding limit.** The GPU render's Blender process reached a working set of about 2.1 GB, the same order as the CPU render. Free RAM fell to about 254 MB during the 2K GPU run, with Claude processes holding about 1.2 GB. The GPU saves time, not host RAM.
- **VRAM:** 839 MiB used during setup. The peak was not captured. A 2K frame fits, and a 4K frame is untested.

## 4. Usage

```
blender -b -P build_cube_scene.py -- --out X.png --width 2560 --height 1440 --samples 64 --device gpu
```

From 19 October 2026 the default is `gpu`, so ongoing renders use the GTX 1650. If no CUDA device is found, the script falls back to the CPU and says so. `--device cpu` forces the CPU. With the GPU active the script prints "GPU devices in use".

## 5. Batch options

- **Animation frames:** one Blender process with a frame range (`--render-anim`) loads the scene once, which saves the start-up cost on each frame. Not yet wired into `build_cube_scene.py`, which renders one still per run.
- **Several stills (for example label variants):** a loop inside one process would render them without reloading the scene. That needs a small change to `main()`.
- **Tiles:** Cycles on the GPU does its own tiling, so no setting is needed.

## 6. Estimate for the storyboard animation (not measured)

About 170 frames. At 2K, 83 s a frame gives about 4 hours. At 1280 by 720, about a quarter of that, roughly one hour. The 1280 by 720 figure is an estimate from the 2K time, not a test.

## 7. Limits

- One GPU run per size. No timing repeats.
- A 4K frame or a long animation may exceed the 4 GB VRAM. Untested.
- Host RAM is the constraint. Close other applications before long renders.
- Colour is compared on pixels only. No colour-management check beyond that.

## 8. Recommendation

Use `--device gpu` for previews and 2K stills, and keep `cpu` as the fallback. For the storyboard clip, add a frame-range render to the script, then render in one process at 1280 by 720.
