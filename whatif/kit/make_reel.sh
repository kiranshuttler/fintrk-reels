#!/usr/bin/env bash
# Build one reel from a spec folder.  Run after: source whatif/kit/setup.sh
# usage: bash make_reel.sh SPEC_DIR STEP   where STEP is one of:
#   voice    -> REEL/assets/voice.wav + timing.json   (then write caps.json/scenes.js using the timings)
#   build    -> REEL/index.html + lint
#   snap T1,T2,...  -> stills + contact sheet in REEL/snaps (look at them!)
#   render SEED OUT.mp4 -> music/SFX mix, render, encode to Instagram spec
set -e
SPEC="$(cd "$1" && pwd)"; STEP="$2"
REEL="$WORK/reel-$(basename "$SPEC")"
mkdir -p "$REEL/assets" "$REEL/fonts"
cp -n "$KIT/reel-skeleton/"* "$REEL/" 2>/dev/null || true
cp "$WORK/node_modules/gsap/dist/gsap.min.js" "$REEL/"
cp "$WORK/node_modules/@fontsource/baloo-2/files/baloo-2-latin-800-normal.woff2" "$WORK/node_modules/@fontsource/baloo-2/files/baloo-2-latin-700-normal.woff2" "$REEL/fonts/"
[ -f "$REEL/meta.json" ] || printf '{"id":"%s","name":"%s"}' "$(basename "$SPEC")" "$(basename "$SPEC")" > "$REEL/meta.json"
TOTAL=$(python3 -c "import json;print(json.load(open('$SPEC/reel.json'))['total'])")
case "$STEP" in
  voice)  python3 "$KIT/make_voice.py" "$SPEC/reel.json" "$REEL/assets" "$WORK/tts" ;;
  build)  python3 "$KIT/build.py" "$SPEC" "$REEL" && (cd "$REEL" && npx hyperframes lint 2>&1 | grep -E "✗|error\(s\)") ;;
  snap)   rm -rf "$REEL/snaps"; (cd "$REEL" && npx hyperframes snapshot --at "$3" --no-end -o "$REEL/snaps" 2>&1 | grep -E "contact|rror") ;;
  render)
    SEED="${3:-7}"; OUT="$4"
    python3 "$KIT/audio.py" "$REEL/assets" "$TOTAL" "$SPEC/sfx.json" "$SEED"
    (cd "$REEL" && npx hyperframes render --quality high --fps 30 --workers 2 -o "$REEL/silent.mp4" 2>&1 | tail -3)
    ffmpeg -hide_banner -loglevel error -y -i "$REEL/silent.mp4" -i "$REEL/assets/mix.wav" -map 0:v:0 -map 1:a:0 \
      -c:v libx264 -preset veryfast -profile:v high -pix_fmt yuv420p -r 30 -b:v 4M -maxrate 4.5M -bufsize 9M -g 60 -keyint_min 60 -sc_threshold 0 \
      -c:a aac -b:a 128k -ar 48000 -ac 2 -shortest -movflags +faststart "$OUT"
    ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_name,width,height -of compact "$OUT" ;;
  *) echo "unknown step $STEP"; exit 1 ;;
esac
