"""Assemble reel/index.html from kit/base.html + a reel spec folder.

usage: python3 build.py SPEC_DIR REEL_DIR
SPEC_DIR holds: reel.json, scenes.html, pops.html, scenes.js, caps.json
REEL_DIR holds: assets/timing.json (from make_voice.py); index.html is written there.
"""
import json, pathlib, re, sys

KIT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KIT))
from props import PROPS

spec, reel = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
cfg = json.loads((spec / "reel.json").read_text())
timing = json.loads((reel / "assets" / "timing.json").read_text())
total = float(cfg["total"])

def expand(html):
    def sub(m):
        name, *args = m.group(1).split(":") if not m.group(1).startswith("burst") else m.group(1).split(":")
        if name not in PROPS:
            raise SystemExit(f"unknown prop {{{{{m.group(1)}}}}}; known: {sorted(PROPS)}")
        return PROPS[name](*args)
    return re.sub(r"\{\{([^{}]+)\}\}", sub, html)

caps = json.loads((spec / "caps.json").read_text())   # [{id,start,end,html}]
caps_html = "\n".join(
    f'<div class="cap clip" id="{c["id"]}" data-start="{c["start"]}" data-duration="{round(c["end"] - c["start"], 3)}">{c["html"]}</div>'
    for c in caps)
data = {"total": total, "env": timing["env"], "lines": [{"start": l["start"], "end": l["end"]} for l in timing["lines"]],
        "caps": [{"id": c["id"], "start": c["start"]} for c in caps]}

html = (KIT / "base.html").read_text()
for k, v in {
    "__THEME_CSS__": cfg.get("theme_css", ""),
    "__EXTRA_CSS__": cfg.get("extra_css", ""),
    "__SCENES__": expand((spec / "scenes.html").read_text()),
    "__POPS__": (spec / "pops.html").read_text(),
    "__CAPTIONS__": caps_html,
    "__WHISKERS__": (KIT / "whiskers.svg.html").read_text(),
    "__SCENE_JS__": (spec / "scenes.js").read_text(),
    "__DATA__": json.dumps(data),
    "__TOTAL__": str(total),
}.items():
    html = html.replace(k, v)
left = re.findall(r"__[A-Z_]+__|\{\{[^{}]+\}\}", html)
if left:
    raise SystemExit(f"unfilled placeholders: {left[:5]}")
(reel / "index.html").write_text(html)
print("wrote", reel / "index.html", len(html), "bytes; total", total, "s")
