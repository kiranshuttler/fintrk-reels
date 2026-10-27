#!/usr/bin/env bash
# One-time (per session) setup for building What If reels for free.
# usage: source whatif/kit/setup.sh   (sets WORK, KIT, HYPERFRAMES_* env vars)
set -e
export KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export WORK="${WORK:-$HOME/whatif-build}"
mkdir -p "$WORK/tts"
cd "$WORK"
if [ ! -d node_modules/hyperframes ]; then
  npm init -y >/dev/null
  npm install --silent hyperframes@0.8.186 gsap@3.14.2 @fontsource/baloo-2@5.3.0 >/dev/null
fi
python3 -c "import kokoro_onnx, soundfile, librosa, scipy" 2>/dev/null || pip install --break-system-packages -q kokoro-onnx soundfile librosa scipy
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
for f in voices-v1.0.bin kokoro-v1.0.onnx; do
  for i in 1 2 3 4 5 6; do curl -sSL -C - -o "$WORK/tts/$f" "$REL/$f" && break; sleep 2; done
done
python3 -c "import onnxruntime as o; o.InferenceSession('$WORK/tts/kokoro-v1.0.onnx')" || { echo "voice model download incomplete"; exit 1; }
export HYPERFRAMES_SKIP_SKILLS=1
export HYPERFRAMES_BROWSER_PATH="$(ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | head -1)"
[ -n "$HYPERFRAMES_BROWSER_PATH" ] || export HYPERFRAMES_BROWSER_PATH="$(ls /opt/pw-browsers/chromium-*/chrome-linux64/chrome | head -1)"
npx hyperframes telemetry disable >/dev/null 2>&1 || true
echo "setup ok: WORK=$WORK KIT=$KIT browser=$HYPERFRAMES_BROWSER_PATH"
