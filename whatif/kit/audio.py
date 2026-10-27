"""Upbeat background music + cartoon SFX, mixed under the voice -> ASSETS/mix.wav

usage: python3 audio.py ASSETS_DIR TOTAL_SECONDS SPEC_DIR/sfx.json [SEED]
sfx.json: [[time, name, gain], ...]  names: boing boing_big boing_low whoosh ding sizzle sizzle_short
          slide_up slide_down scratch rimshot thud.  Put a whoosh on every scene change and a boing/rimshot on punchlines.
SEED (e.g. the date as 20261028) changes the melody/key a little so every reel sounds different.
"""
import json, sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
REEL = sys.argv[1]
TOTAL = float(sys.argv[2])
SFX = json.load(open(sys.argv[3]))
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 7
rng = np.random.default_rng(SEED)
N = int(TOTAL * SR)

def t_(d): return np.arange(int(d * SR)) / SR
def env_ad(n, a=0.005, d=0.3):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)
def note(f): return 440 * 2 ** ((f - 69) / 12)

# ---------------- music: 118 bpm, C - G - Am - F, marimba + bass + light drums ----------------
bpm = 108 + (SEED % 5) * 4; beat = 60 / bpm; bar = 4 * beat
KEY = [0, 2, 5, 7, -3][SEED % 5]
music = np.zeros(N)
PROGS = [[(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69])],
         [(48, [60, 64, 67, 72]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69]), (43, [59, 62, 67, 71])],
         [(41, [57, 60, 65, 69]), (43, [59, 62, 67, 71]), (48, [60, 64, 67, 72]), (48, [60, 64, 67, 72])]]
chords = [(r + KEY, [n + KEY for n in ns]) for r, ns in PROGS[(SEED // 5) % 3]]
melody_pat = [[0, 2, 1, 3, 2, 1, 3, 2], [0, 1, 2, 3, 2, 3, 1, 2], [3, 2, 0, 2, 1, 2, 0, 3]][SEED % 3]
def add(buf, start, sig, g):
    i = int(start * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += g * sig[: j - i]
def marimba(f, d=0.35):
    t = t_(d); return (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.05)) * env_ad(len(t), 0.002, 0.12)
def bass(f, d=0.45):
    t = t_(d); s = np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t); return s * env_ad(len(t), 0.004, 0.25)
def kick():
    t = t_(0.25); f = 50 + 90 * np.exp(-t / 0.04); return np.sin(2*np.pi*np.cumsum(f)/SR) * env_ad(len(t), 0.001, 0.12)
def clap():
    n = rng.standard_normal(int(0.18 * SR)); return bp(n, 900, 3000) * env_ad(len(n), 0.001, 0.05)
def shaker():
    n = rng.standard_normal(int(0.06 * SR)); return hp(n, 6000) * env_ad(len(n), 0.002, 0.02)
t0 = 0.0; b = 0
while t0 < TOTAL:
    root, tones = chords[b % 4]
    add(music, t0, bass(note(root - 12 + 12)), 0.5); add(music, t0 + 2 * beat, bass(note(root)), 0.45)
    for k in range(8):
        add(music, t0 + k * beat / 2, marimba(note(tones[melody_pat[k]] + 12)), 0.28 if k % 2 == 0 else 0.2)
    for k in range(4):
        add(music, t0 + k * beat, kick() if k % 2 == 0 else clap(), 0.55 if k % 2 == 0 else 0.35)
    for k in range(16):
        add(music, t0 + k * beat / 4, shaker(), 0.12 if k % 2 else 0.07)
    t0 += bar; b += 1
music = music / np.abs(music).max()
fade = np.ones(N); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl)
music *= fade

# ---------------- SFX ----------------
def boing(d=0.6, base=170):
    t = t_(d); f = base + 260 * t + 90 * np.sin(2*np.pi*14*t) * np.exp(-t/0.25)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * env_ad(len(t), 0.003, 0.25)
def whoosh(d=0.38):
    n = rng.standard_normal(int(d * SR)); t = np.arange(len(n)) / SR
    out = np.zeros_like(n); seg = int(0.01 * SR)
    for i in range(0, len(n), seg):
        c = 500 + 3500 * np.sin(np.pi * i / len(n)); out[i:i+seg] = bp(n[i:i+seg+256], c*0.6, c*1.4)[:len(n[i:i+seg])]
    return out * np.sin(np.pi * t / d) ** 2 * 1.6
def ding(f=1320, d=0.9):
    t = t_(d); return (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2.01*f*t)) * env_ad(len(t), 0.002, 0.3) * 0.7
def sizzle(d=1.4):
    n = hp(rng.standard_normal(int(d * SR)), 3500)
    crack = (rng.random(len(n)) > 0.9985).astype(float); crack = lp(crack, 3000) * 25
    t = np.arange(len(n)) / SR; e = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2)
    return (0.35 * n + crack) * e
def slide(f0, f1, d=0.45):
    t = t_(d); f = f0 + (f1 - f0) * (t / d) ** 0.8
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.minimum(1, t/0.02) * np.minimum(1, (d-t)/0.05) * 0.6
def scratch(d=0.42):
    t = t_(d); f = 260 + 900 * np.abs(np.sin(2*np.pi*3.2*t))
    s = np.sign(np.sin(2*np.pi*np.cumsum(f)/SR)) * 0.4 + bp(rng.standard_normal(len(t)), 600, 4000) * 0.8
    return s * np.minimum(1, t/0.01) * np.minimum(1, (d-t)/0.05)
def tom(f0, f1, d=0.16):
    t = t_(d); f = f1 + (f0 - f1) * np.exp(-t/0.04); return np.sin(2*np.pi*np.cumsum(f)/SR) * env_ad(len(t), 0.001, 0.07)
def rimshot():
    out = np.zeros(int(1.0 * SR)); add(out, 0, tom(240, 170), 1); add(out, 0.16, tom(180, 120), 1)
    cym = hp(rng.standard_normal(int(0.7 * SR)), 5000) * env_ad(int(0.7 * SR), 0.002, 0.25)
    add(out, 0.34, cym, 0.7); return out
def thud():
    return tom(120, 60, 0.3) * 1.2

BANK = {"boing": boing, "boing_big": lambda: boing(0.8, 140), "boing_low": lambda: boing(0.5, 110), "whoosh": whoosh, "ding": ding,
        "sizzle": sizzle, "sizzle_short": lambda: sizzle(0.6), "slide_up": lambda: slide(380, 1300), "slide_down": lambda: slide(1300, 300, 0.6),
        "scratch": scratch, "rimshot": rimshot, "thud": thud}
cues = SFX
sfx = np.zeros(N)
for t, name, g in cues:
    s = BANK[name](); add(sfx, t, s / (np.abs(s).max() + 1e-9), g)

# ---------------- mix with ducking under the voice ----------------
voice, vsr = sf.read(f"{REEL}/voice.wav", dtype="float64"); assert vsr == SR
v = np.zeros(N); v[: min(N, len(voice))] = voice[:N]
win = int(0.05 * SR)
venv = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, mode="same"))
duck = 1 - 0.55 * np.clip(venv / 0.08, 0, 1)
duck = np.convolve(duck, np.ones(int(0.12 * SR)) / int(0.12 * SR), mode="same")
mix = 1.0 * v + 0.17 * music * duck + 0.55 * sfx
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix / np.abs(mix).max() * 0.95
sf.write(f"{REEL}/mix.wav", np.stack([mix, mix], axis=1).astype(np.float32), SR)
print("mix ok", round(len(mix) / SR, 2), "s")
