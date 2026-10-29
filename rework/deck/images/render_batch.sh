#!/bin/bash
# Batch renderer for the deck images, one Blender process at a time (the host has 8 GB of RAM).
# Each image is tried at LONG (default 3840, 4K); if that Blender run fails or writes no PNG, it is
# retried once at FALLBACK_LONG (default 2048, 2K). Progress goes to OUT/batch_status.txt.
#
#   bash render_batch.sh OUT_DIR [IDS...]
#   env: LONG=3840 FALLBACK_LONG=2048 SAMPLES=192 SHADOWS="1 0" KNOWN_4K_FAIL_PIXELS=0
#   SHADOWS: 1 = soft contact shadow kept in the alpha, 0 = bare cut-out. "1 0" renders both.
#   KNOWN_4K_FAIL_PIXELS: pixel count of an image that already failed at LONG (for example the host
#   ran out of memory on a 3840 x 2880 frame). Images with at least 90% of that many pixels go straight
#   to FALLBACK_LONG instead of repeating the failed attempt; smaller images still try LONG first.
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$HERE/render_deck_images.py"
OUT="$1"; shift
IDS=("$@"); [ ${#IDS[@]} -eq 0 ] && IDS=(P1 P2 P3 P4 P5 P6)
LONG="${LONG:-3840}"; FALLBACK_LONG="${FALLBACK_LONG:-2048}"; SAMPLES="${SAMPLES:-192}"; SHADOWS="${SHADOWS:-1 0}"
FAIL_PIX="${KNOWN_4K_FAIL_PIXELS:-0}"
declare -A PCT=( [P1]=80 [P2]=75 [P3]=75 [P4]=75 [P5]=75 [P6]=25 )   # pixels = LONG^2 * pct / 100
mkdir -p "$OUT/logs"
STATUS="$OUT/batch_status.txt"; : > "$STATUS"

run_one() {  # id shadow long
  local id="$1" sh="$2" long="$3" marker
  marker="$OUT/logs/.marker_${id}_${sh}_${long}"; : > "$marker"
  local t0=$SECONDS
  "$BL" -b -P "$SCRIPT" -- --id "$id" --out-dir "$OUT" --long "$long" --samples "$SAMPLES" --shadow "$sh" \
      > "$OUT/logs/${id}_shadow${sh}_${long}.txt" 2>&1
  local rc=$? newest
  newest=$(find "$OUT" -maxdepth 1 -name "${id}_*.png" -newer "$marker" | head -1)
  if [ $rc -eq 0 ] && [ -n "$newest" ]; then
    python -I "$HERE/postprocess_alpha.py" "$newest" >> "$OUT/logs/${id}_shadow${sh}_${long}.txt" 2>&1
    echo "$id shadow=$sh long=$long OK $((SECONDS-t0))s $(basename "$newest")" >> "$STATUS"; return 0
  fi
  echo "$id shadow=$sh long=$long FAILED rc=$rc $((SECONDS-t0))s" >> "$STATUS"; return 1
}

for id in "${IDS[@]}"; do
  pix=$(( LONG * LONG * ${PCT[$id]} / 100 ))
  for sh in $SHADOWS; do
    if [ "$FAIL_PIX" -gt 0 ] && [ "$pix" -ge $(( FAIL_PIX * 9 / 10 )) ] && [ "$FALLBACK_LONG" -gt 0 ] && [ "$FALLBACK_LONG" -lt "$LONG" ]; then
      echo "$id shadow=$sh skip long=$LONG (pixels $pix, a frame of $FAIL_PIX already failed on host memory)" >> "$STATUS"
      run_one "$id" "$sh" "$FALLBACK_LONG"
    elif ! run_one "$id" "$sh" "$LONG"; then
      if [ "${FALLBACK_LONG:-0}" -gt 0 ] && [ "$FALLBACK_LONG" -lt "$LONG" ]; then
        echo "$id shadow=$sh downgrading to ${FALLBACK_LONG}" >> "$STATUS"
        run_one "$id" "$sh" "$FALLBACK_LONG" && { [ "$FAIL_PIX" -eq 0 ] || [ "$pix" -lt "$FAIL_PIX" ]; } && FAIL_PIX=$pix
      fi
    fi
  done
done
echo BATCH_DONE >> "$STATUS"
