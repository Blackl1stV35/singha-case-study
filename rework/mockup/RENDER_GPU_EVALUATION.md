# Rendering on the local GPU (19 October 2026)

Status: measured on this machine on 19 October 2026. The render logs are saved in `rework/screen/render_logs/` (index in `LOG_INDEX.md`). Each timing below cites its log. Readings without a log are marked **not logged**. One GPU run per size, so no repeats.

## 1. Hardware and software

- GPU: NVIDIA GeForce GTX 1650, 4 GB VRAM, compute capability 7.5, no RT cores. Driver 617.42 from `nvidia-smi` (**not logged**).
- CPU: AMD Ryzen 5 5500U, as listed by Blender's device list in this session (**not logged**).
- RAM: 8 GB total, about 7.5 GB visible, from a PowerShell reading (**not logged**).
- Blender: 5.2.2 LTS, as printed at the end of the render logs.

## 2. Timings (from the render logs)

| Test | CPU runs (log) | GPU (log) | Image difference, GPU against CPU |
|---|---|---|---|
| 960 by 540, 32 samples | 29.4 s (`bench_cpu.log`) | 8.1 s (`bench_gpu.log`) | mean 0.0, largest 9 of 255 |
| 2560 by 1440, 64 samples | 291.6 s (`render_tarlo_2k.log`), 324.2 s (`render_front_2k.log`), 340.5 s (`render_2k.log`), 369.0 s (`render_lime_cube_clean_2k.log`) | 83.4 s (`bench_gpu_2k.log`) | mean 0.0, largest 5 of 255 |

Speed-up:
- At 960 by 540: 29.4 / 8.1 = **3.6 times**.
- At 2560 by 1440: from 291.6 / 83.4 = 3.5 to 369.0 / 83.4 = 4.4 times. The four CPU runs are not repeats of one setting, so the range is the honest figure.

The image comparison is pixel-level only. No colour-management check was made.

## 3. Memory

- **Host RAM is the binding limit.** A 2K render's Blender process was observed at about 2.1 GB working set (one reading, **not logged**). Free RAM fell to about 254 MB during the 2K GPU run (one reading, **not logged**). The GPU saves time, not host RAM.
- **VRAM:** 839 MiB used when sampled during setup (**not logged**). The peak was not captured.

## 4. Usage

```
blender -b -P build_cube_scene.py -- --out X.png --width 2560 --height 1440 --samples 64
```

The default is now `gpu` (from 19 October 2026), so the flag is optional. The script falls back to the CPU and says so when no CUDA device is found. `--device cpu` forces the CPU. With the GPU active, the script prints "GPU devices in use".

## 5. Batch options

- **Animation frames:** one Blender process with a frame range (`--render-anim`) loads the scene once. The script renders one still per run, so this needs a small change before it is used.
- **Several stills:** a loop inside one process would render label variants without reloading the scene. This needs a small change to `main()`.
- **Tiles:** Cycles on the GPU does its own tiling, so no setting is needed.

## 6. Estimate for the storyboard animation (an estimate, not measured)

About 170 frames. At 2K, 83.4 s a frame gives about 3.9 hours (170 x 83.4 s). At 1280 by 720, about a quarter of the pixels, so roughly one hour. The 1280 by 720 figure is an estimate from the 2K timing, not a test.

## 7. Limits

- One GPU run per size. Several readings above are **not logged** and are marked as such.
- A 4K frame or a long animation may exceed the 4 GB of VRAM. Untested.
- Host RAM is the constraint. Close other applications before long renders.
- The GPU and CPU images are compared on pixels only.

## 8. Recommendation

Use the default GPU for previews and 2K stills, and keep the CPU as the fallback. For the storyboard clip, add a frame-range render to the script, then render in one process at 1280 by 720.
