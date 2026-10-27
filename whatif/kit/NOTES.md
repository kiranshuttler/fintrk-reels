# What If & Why So — free reel kit (no HeyGen)

Builds a 30–40 s vertical reel locally: hand-drawn SVG scenes animated with GSAP, rendered by the
open-source HyperFrames CLI, narrated by **Whiskers** with an offline voice (Kokoro TTS, pitch-shifted),
plus synthesized music and cartoon sound effects. Cost: zero. Render time: ~2–3 min.

`example-enthiran/` is a complete, approved reel (posted 27 Oct 2026). **Copy its structure for every new reel.**

## Steps
```bash
source whatif/kit/setup.sh                      # NOT piped (| tail) or the env vars are lost
SPEC=$WORK/specs/<key>; mkdir -p $SPEC           # write reel.json first (title, total, voice, theme_css, lines)
bash $KIT/make_reel.sh $SPEC voice               # prints each line's start/end seconds
#  -> write caps.json, scenes.html, pops.html, scenes.js, sfx.json using those timings
bash $KIT/make_reel.sh $SPEC build               # must say 0 error(s) (warnings are fine)
bash $KIT/make_reel.sh $SPEC snap 0.0,<mid of every scene>,<every pop + 0.3>   # then Read $WORK/reel-<key>/snaps/contact-sheet*.jpg
bash $KIT/make_reel.sh $SPEC render <SEED> $WORK/out.mp4   # SEED = YYYYMMDD*10+slot -> different music each reel
```

## Files in a spec folder
- `reel.json` — `{"title","total","voice":{"name":"hm_psi","pitch":1.4,"speed":1.17},"theme","theme_css","lines":[{"text","pause"}]}`
  - `lines` = the voiceover, one entry per beat. Write numbers as words ("ten A.M.", "thirty-five degrees").
  - `total` = last line's end + ~1.7 s (end card hold). Keep 28–40 s.
  - `theme_css` = `:root{--bg1:#..;--bg2:#..;--bg3:#..;--accent:#..;--accent2:#..}` (see themes below).
- `caps.json` — `[{"id","start","end","html"}]`. One caption per spoken line, split long lines at sentence
  boundaries (estimate the split time by character share). Max ~70 characters (2 lines). Use digits/°C here.
  Highlight 1–3 punch words with `<span class='hl'>` (accent) or `<span class='hl2'>`. No caption for the hook line
  (the title card shows it) or the closing line (the end card shows it). Caption `end` = next caption's `start`.
- `scenes.html` — `<section id="sN" class="scene clip" data-start=".." data-duration="..">` per beat.
  Make each scene last until 0.22 s after the next one starts (the whip-in covers it). Scene 1 starts at 0 and must
  already show the hook title card at frame 0. Last scene = end card (tag-a-friend card + `.follow` card).
  Props: `{{burst:#hex:#hex}}` (rotating sunburst bg), `{{sun}}`, `{{robot}}`, `{{car}}`, `{{ladle}}`, `{{ceilfan}}`,
  `{{phone:LINE|LINE|LINE:BIG:small:emoji}}`, `{{therm:LABEL:bulb text}}` (no ":" inside args). Draw anything else
  as inline SVG in the same style: flat fills, `stroke="#2B1B12" stroke-width="8" stroke-linejoin="round"`.
- `pops.html` — meme words: `<div class="pop clip" id="p-x" data-start=".." data-duration="~1.0" style="left;top;transform: rotate(-8deg)">WAIT WHAT?! </div>`.
  At 128px each character is ~70px wide: keep `left + width` under 1000 (use font-size 104–112px for long ones).
- `scenes.js` — the scene timeline. Helpers from base.html: `whip(sel,t)`, `place(t,px,py,scale,dur)`, `pop(sel,t)`,
  `stampIn(sel,t,rot)`, `shake(t,amt)`, `punch(sel,t)`, `shock(t,hold)`, `smug(t,d)`, `cry(t,d)`, `sweat(t,d)`,
  `smoke(t,d)`, `wave(t,n)`, `earWiggle(t,n)`, `fanFrantic(t,d)`, `show(sel,t,on)`, `wx/wy`, and `L[i].start/.end`
  (voice line times). Toasted ears: tween `#wk-earL-toast,#wk-earR-toast` opacity. Lip sync is automatic.
- `sfx.json` — `[[t,"name",gain]]`: whoosh (0.45) on every scene change, boing/boing_big/rimshot/slide_down/scratch
  (0.4–0.6) on punchlines, ding on stamps, sizzle for heat. See audio.py for names.

## Layout (1080×1920; Instagram covers the top ~250 px, bottom ~360 px and a right-hand button column)
- Keep text inside x 60–1000, y 260–1560.
- Title/label zone y 270–620 (hook title card `.abs.title.card`, clock pill `.abs.card.clock`, stamp `.abs.stamp`).
- Stage y 420–1180 for props. Whiskers: `place(t, px, 1390, s)` → feet at y 1390, s 0.66–1.0
  (height = 680·s). Captions sit at y 1392–1560 (`.cap`), on top of his feet.
- Put Whiskers left (px≈220–330) when a prop needs the right side, centre (px 540) for his own gags.

## Animation rules (learned the hard way)
- GSAP only on opacity, x, y, scale, scaleX, scaleY, rotation. No Math.random / Date.
- For any NEW SVG part you rotate/scale, call `gsap.set(sel, {svgOrigin: "x y"})` ONCE at the top of scenes.js
  (coords in that SVG's own viewBox). NEVER pass transformOrigin/svgOrigin inside a tween — it bakes in an
  offset and the part drifts (this broke the mercury and the dosa in the first draft).
- Fill-level / pour effects: scaleY from 0.25→1 with the origin at the bottom/top set beforehand.
- Pops & captions are timed `.clip` elements; animate them with `pop()` / they animate automatically.
- First frame must already be readable (hook). Last ~2 s: end card with `wave()`.

## Review checklist (look at the contact sheet before rendering)
Nothing clipped at the edges (pops, emoji), no pop covering the joke prop, captions readable and ≤2 lines,
Whiskers' face not hidden, every scene's gag visible at its midpoint, end card handle spelled `@_what.if.why.so_`.

## Themes (theme_css values; cards stay cream #FFF4DC with ink #2B1B12 outlines)
| Theme | --bg1 | --bg2 | --bg3 | --accent | --accent2 |
|---|---|---|---|---|---|
| Mango Monsoon | #FFB347 | #8FA3B8 | #5E9E4A | #E8590C | #3B6E9E |
| Peacock Night | #0F6E73 | #2A2A72 | #12403F | #C99A06 | #0F6E73 |
| Holi Pop | #FF3FA4 | #A3E635 | #38BDF8 | #D6246E | #0284C7 |
| Chalkboard Classroom | #2F5D3A | #23452B | #3F7A4C | #B45309 | #2F5D3A |
| Desert Sunset | #E07A5F | #F2CC8F | #F4A6B7 | #C2410C | #3D405B |
| Kerala Backwaters | #1B8A5A | #7B4B2A | #3FA7D6 | #0E7A4E | #2B7BB9 |
| Retro Cinema Hall | #C1121F | #1A1A1A | #FDF0D5 | #C1121F | #B8860B |
| Space Lab | #14213D | #0B132B | #1C2E5A | #F77F00 | #0096C7 |
| Spice Market | #F4B41A | #6E9F4F | #D7263D | #D7263D | #2BB3A3 |
| Comic Newsprint | #FFF3D6 | #1D4E89 | #E63946 | #E63946 | #1D4E89 |
| Paper Cutout | #FFD6E0 | #C1E1C1 | #BDE0FE | #E5487C | #3A86FF |
| Neon Arcade | #3C096C | #10002B | #240046 | #FF006E | #0096C7 |
| Marigold Festival | #F7B32B | #F28C28 | #0F7173 | #D1495B | #0F7173 |
On dark backgrounds, loose text (not in a card) should be cream with an ink stroke
(`-webkit-text-stroke: 8px #2B1B12; paint-order: stroke fill`).

## Publish
Copy the MP4 to `whatif/<YYYY-MM-DD>-slotN-<slug>.mp4` in the fintrk-reels repo, commit, `git fetch origin main &&
git rebase origin/main`, push to main, then check
`https://raw.githubusercontent.com/kiranshuttler/fintrk-reels/main/whatif/<file>` returns 200 before posting.
Never touch `reels/` (that is @fintrk.pro's).
