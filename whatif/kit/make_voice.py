"""Whiskers' comical voice (offline Kokoro TTS + pitch shift) -> REEL_DIR/assets/voice.wav + timing.json

usage: python3 make_voice.py SPEC_DIR/reel.json REEL_DIR/assets MODEL_DIR
reel.json: {"lines": [{"text": "...", "pause": 0.4}, ...], "voice": {"name": "hm_psi", "pitch": 1.4, "speed": 1.17}}
Write numbers as words in "text" (e.g. "ten A.M.", "thirty-five degrees") so they are spoken right.
"""
import json, subprocess, sys, tempfile, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

cfg = json.load(open(sys.argv[1])); out = sys.argv[2]; model = sys.argv[3]
v = cfg.get("voice", {})
VOICE, PITCH, SPEED = v.get("name", "hm_psi"), float(v.get("pitch", 1.4)), float(v.get("speed", 1.17))
SR = 48000
k = Kokoro(os.path.join(model, "kokoro-v1.0.onnx"), os.path.join(model, "voices-v1.0.bin"))
tmp = tempfile.mkdtemp()
segs, timing, t = [np.zeros(int(0.25 * SR), dtype=np.float32)], [], 0.25
for i, line in enumerate(cfg["lines"]):
    a, sr = k.create(line["text"], voice=VOICE, speed=SPEED, lang="en-us")
    sf.write(f"{tmp}/raw.wav", a, sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/raw.wav", "-af",
                    f"rubberband=pitch={PITCH}:formant=shifted,aresample={SR}", "-ac", "1", f"{tmp}/p.wav"], check=True)
    b, _ = sf.read(f"{tmp}/p.wav", dtype="float32")
    thr = 10 ** (-42 / 20) * np.abs(b).max()
    idx = np.where(np.abs(b) > thr)[0]
    b = b[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.06 * SR)]
    dur = len(b) / SR
    timing.append({"i": i, "start": round(t, 3), "end": round(t + dur, 3), "text": line["text"]})
    pause = float(line.get("pause", 0.4))
    segs += [b, np.zeros(int(pause * SR), dtype=np.float32)]
    t += dur + pause
vo = np.concatenate(segs)
vo = vo / (np.abs(vo).max() + 1e-9) * 0.89
sf.write(f"{out}/voice.wav", vo, SR)
hop = SR // 30
env = [float(np.sqrt(np.mean(vo[j:j + hop] ** 2))) for j in range(0, len(vo), hop)]
m = max(env); env = [round(min(1.0, (e / m) * 1.6), 3) for e in env]
json.dump({"duration": round(len(vo) / SR, 3), "lines": timing, "env": env}, open(f"{out}/timing.json", "w"))
print(json.dumps({"voice_duration": round(len(vo) / SR, 2), "lines": [[l["i"], l["start"], l["end"]] for l in timing]}))
