"""Reusable cartoon props for What If reels. Use in scenes.html as {{name}} or {{name:arg1:arg2}}.
Every prop is an inline <svg width=100% height=100%>; put it inside a positioned <div class="abs" style="left..;top..;width..;height..">.
Animated parts carry classes whose svgOrigin is already set in base.html:
  sun: .sun-rays | robot: .rb-head .rb-hot .rb-steam .rb-dosa .rb-armL .rb-armR .rb-ok .rb-msg | ceilfan: .cf-blades
  ladle: .batter | therm: .merc (scaleY 0.25 -> 1 to fill)
Draw new props the same way: thick #2B1B12 outlines (stroke-width 7-8, round joins), flat fills from the reel's theme.
"""
import math
def burst(c1, c2, n=16, r=160):
    parts = [f'<rect x="-100" y="-100" width="200" height="200" fill="{c1}"/>']
    for k in range(0, n, 2):
        a1, a2 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        parts.append(f'<path d="M0 0 L{r*math.cos(a1):.1f} {r*math.sin(a1):.1f} L{r*math.cos(a2):.1f} {r*math.sin(a2):.1f} Z" fill="{c2}"/>')
    return "".join(parts)

SUN = """<svg viewBox="0 0 300 300" width="100%" height="100%"><g stroke="#2B1B12" stroke-width="7" stroke-linejoin="round">
<g class="sun-rays">""" + "".join(
    f'<rect x="140" y="6" width="20" height="54" rx="10" fill="#FFB703" transform="rotate({a} 150 150)"/>' for a in range(0, 360, 30)
) + """</g>
<circle cx="150" cy="150" r="86" fill="#FFD23F"/>
<path d="M88 128 L140 128 Q140 166 114 166 Q88 166 88 128Z" fill="#2B1B12"/>
<path d="M160 128 L212 128 Q212 166 186 166 Q160 166 160 128Z" fill="#2B1B12"/>
<path d="M140 136 L160 136" stroke-width="7"/>
<path d="M98 136 L110 136" stroke="#FFFFFF" stroke-width="5"/><path d="M170 136 L182 136" stroke="#FFFFFF" stroke-width="5"/>
<path d="M112 196 Q150 226 188 196" fill="none" stroke-width="8"/>
<circle cx="92" cy="184" r="13" fill="#FF8C69" stroke="none"/><circle cx="208" cy="184" r="13" fill="#FF8C69" stroke="none"/>
</g></svg>"""

def robot(*_):
    return """<svg viewBox="0 0 360 540" width="100%" height="100%" overflow="visible"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round" stroke-linecap="round">
<g class="rb-steam" opacity="0" fill="#E8E4DF" stroke-width="5"><circle cx="110" cy="-10" r="20"/><circle cx="180" cy="-30" r="26"/><circle cx="250" cy="-8" r="18"/></g>
<g class="rb-armL"><rect x="14" y="240" width="46" height="150" rx="23" fill="#AEBBC7"/><circle cx="37" cy="402" r="27" fill="#CBD5DF"/></g>
<g class="rb-armR"><rect x="300" y="240" width="46" height="150" rx="23" fill="#AEBBC7"/><circle cx="323" cy="402" r="27" fill="#CBD5DF"/></g>
<rect x="110" y="420" width="52" height="78" rx="18" fill="#AEBBC7"/><rect x="198" y="420" width="52" height="78" rx="18" fill="#AEBBC7"/>
<rect x="92" y="488" width="86" height="38" rx="19" fill="#8996A3"/><rect x="182" y="488" width="86" height="38" rx="19" fill="#8996A3"/>
<rect x="56" y="214" width="248" height="214" rx="44" fill="#C3CED9"/>
<rect x="96" y="252" width="168" height="118" rx="18" fill="#1E2A38" stroke-width="6"/>
<g class="rb-ok"><text x="180" y="328" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="56" fill="#5FF3A0" stroke="none">OK ✓</text></g>
<g class="rb-msg" opacity="0" stroke="none" font-family="Baloo" font-weight="800" text-anchor="middle">
  <text x="180" y="292" font-size="30" fill="#FF5A5F">OVERHEATED!</text>
  <text x="180" y="326" font-size="24" fill="#5FF3FF">TRY AGAIN IN</text>
  <text x="180" y="356" font-size="28" fill="#FFE066">NOVEMBER</text>
</g>
<rect x="160" y="196" width="40" height="26" fill="#8996A3"/>
<g class="rb-head">
  <line x1="180" y1="44" x2="180" y2="10"/><circle cx="180" cy="8" r="13" fill="#D7263D"/>
  <rect x="70" y="40" width="220" height="162" rx="38" fill="#D8E1EA"/>
  <rect class="rb-hot" x="70" y="40" width="220" height="162" rx="38" fill="#FF4D1F" opacity="0"/>
  <rect x="95" y="80" width="170" height="62" rx="30" fill="#1E2A38" stroke-width="6"/>
  <circle cx="145" cy="111" r="14" fill="#5FF3FF" stroke="none"/><circle cx="215" cy="111" r="14" fill="#5FF3FF" stroke="none"/>
  <rect x="140" y="160" width="80" height="20" rx="9" fill="#8996A3" stroke-width="5"/>
  <path d="M160 162 L160 178 M180 162 L180 178 M200 162 L200 178" stroke-width="4"/>
  <g class="rb-dosa" opacity="0"><ellipse cx="180" cy="34" rx="128" ry="24" fill="#E8A33D" stroke-width="7"/>
    <circle cx="130" cy="30" r="6" fill="#B86B1E" stroke="none"/><circle cx="190" cy="40" r="7" fill="#B86B1E" stroke="none"/><circle cx="240" cy="28" r="5" fill="#B86B1E" stroke="none"/><circle cx="160" cy="42" r="4" fill="#B86B1E" stroke="none"/></g>
</g>
</g></svg>"""

CAR = """<svg viewBox="0 0 300 180" width="100%" height="100%"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round">
<path d="M20 110 Q20 80 50 78 L85 40 Q92 30 110 30 L200 30 Q215 30 225 42 L255 78 Q282 80 282 110 L282 128 Q282 138 270 138 L32 138 Q20 138 20 128Z" fill="#2BB3A3"/>
<path d="M98 76 L116 46 L158 46 L158 76Z" fill="#D9F4FF" stroke-width="6"/><path d="M172 76 L172 46 L204 46 L228 76Z" fill="#D9F4FF" stroke-width="6"/>
<circle cx="80" cy="140" r="27" fill="#2B1B12"/><circle cx="80" cy="140" r="10" fill="#CFCFCF" stroke-width="4"/>
<circle cx="222" cy="140" r="27" fill="#2B1B12"/><circle cx="222" cy="140" r="10" fill="#CFCFCF" stroke-width="4"/>
<circle cx="268" cy="100" r="8" fill="#FFE066" stroke-width="4"/></g></svg>"""

LADLE = """<svg viewBox="0 0 520 390" width="100%" height="100%" overflow="visible"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round" stroke-linecap="round">
<rect class="batter" x="418" y="132" width="24" height="250" rx="12" fill="#F6E7C1" stroke-width="5"/>
<rect x="-30" y="150" width="210" height="92" rx="22" fill="#6E9F4F"/>
<rect x="160" y="146" width="30" height="100" rx="12" fill="#F4B41A"/>
<line x1="235" y1="185" x2="408" y2="118" stroke-width="22"/><line x1="235" y1="185" x2="408" y2="118" stroke="#8A5A2B" stroke-width="12"/>
<path d="M378 104 Q428 186 478 104 Z" fill="#A7B1BC"/>
<ellipse cx="228" cy="196" rx="52" ry="44" fill="#C98A5C"/>
<path d="M206 176 Q228 168 250 178" fill="none" stroke-width="5"/></g></svg>"""

CEILFAN = """<svg viewBox="0 0 600 520" width="100%" height="100%"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round">
<rect x="290" y="-10" width="20" height="260" fill="#8996A3"/>
<g class="cf-blades">""" + "".join(
    f'<ellipse cx="455" cy="300" rx="165" ry="32" fill="#FFF4DC" transform="rotate({a} 300 300)"/>' for a in (0, 120, 240)
) + """</g><circle cx="300" cy="300" r="42" fill="#D7263D"/><circle cx="300" cy="300" r="14" fill="#FFF4DC"/></g></svg>"""

def phone(lines="MADE FOR|WEATHER|UP TO", big="35°C", small="", emoji="😅"):
    rows = lines.split("|")
    t = "".join(f'<text x="165" y="{140 + 46*i}" font-size="40">{r}</text>' for i, r in enumerate(rows[:4]))
    return f"""<svg viewBox="0 0 330 560" width="100%" height="100%"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round">
<rect x="10" y="10" width="310" height="540" rx="48" fill="#2B1B12"/>
<rect x="34" y="60" width="262" height="440" rx="26" fill="#FFF4DC" stroke-width="5"/>
<rect x="125" y="24" width="80" height="16" rx="8" fill="#444" stroke="none"/>
<g stroke="none" font-family="Baloo" font-weight="800" text-anchor="middle" fill="#2B1B12">{t}
<text x="165" y="330" font-size="92" fill="#2BB3A3">{big}</text>
<text x="165" y="400" font-size="26" fill="#7A6A5C">{small}</text>
<text x="165" y="470" font-size="54">{emoji}</text></g></g></svg>"""

def therm(label="CITY", bulb=""):
    return f"""<svg viewBox="0 0 320 680" width="100%" height="100%" overflow="visible"><g stroke="#2B1B12" stroke-width="8" stroke-linejoin="round">
<text x="160" y="40" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="46" fill="#FFF4DC" stroke-width="10" paint-order="stroke fill">{label}</text>
<rect x="118" y="62" width="84" height="520" rx="42" fill="#FFFFFF"/>
<rect class="merc" x="140" y="70" width="40" height="540" rx="20" fill="#D7263D" stroke="none"/>
<circle cx="160" cy="608" r="66" fill="#D7263D"/>
<g stroke-width="5"><path d="M202 140 L226 140"/><path d="M202 220 L226 220"/><path d="M202 300 L226 300"/><path d="M202 380 L226 380"/><path d="M202 460 L226 460"/></g>
<text x="160" y="620" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="34" fill="#FFF4DC" stroke="none">{bulb}</text></g></svg>"""


PROPS = {"burst": burst, "sun": lambda *a: SUN, "robot": robot, "car": lambda *a: CAR, "ladle": lambda *a: LADLE,
         "ceilfan": lambda *a: CEILFAN, "phone": phone, "therm": therm}
