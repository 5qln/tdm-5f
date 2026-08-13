"""
The visible face — render the engine running.

Run:  uv run --with pillow make_gif.py
Out:  /opt/data/wiki/fractal dialog/assets/pentagon-running.gif

The loop tells the whole story:
    flat Codex (the ground) → the page stands up → cycle walk (R) →
    star walk (720°, deposits B'') → the fractal draws itself again →
    contraction (C*) back to the nine lines.
"""

from PIL import Image, ImageDraw, ImageFont

import sys, os

import pentagon as P

W = H = 640
BG = (10, 14, 26)
GOLD = (212, 175, 55)
TEAL = (127, 212, 193)
WHITE = (235, 238, 245)
DIM = (96, 106, 128)
CX = CY = W // 2
RADIUS = 185
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "tdm-5f-demo.gif")

FONT_CANDIDATES = {
    "code": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/dejavu-core/DejaVuSansMono.ttf",
    ],
    "reg": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu-core/DejaVuSans.ttf",
    ],
    "bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu-core/DejaVuSans-Bold.ttf",
    ],
}


def _font(kind, size):
    """Resolve a font across common DejaVu locations; fall back to the default."""
    for p in FONT_CANDIDATES[kind]:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def fade(c, t):
    """Interpolate color c toward the background by t."""
    return tuple(int(c[i] + (BG[i] - c[i]) * t) for i in range(3))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertex(d, k, s=1.0):
    x, y = P.vertex_xy(d, k, cx=CX, cy=CY, radius=RADIUS)
    return CX + (x - CX) * s, CY + (y - CY) * s


def draw_codex(dr, t, y0=52, x0=36):
    f = _font("code", 15)
    for i, line in enumerate(P.CODEX):
        dr.text((x0, y0 + i * 34), line, font=f, fill=fade(WHITE, 1 - t))


def draw_pentagon(dr, depth, s, edge_color, dot_color, letters=True):
    f_l = _font("bold", 24)
    pts = [vertex(depth, k, s) for k in range(5)]
    for i in range(5):
        dr.line([pts[i], pts[(i + 1) % 5]], fill=edge_color, width=3)
    for k in range(5):
        x, y = pts[k]
        dr.ellipse([x - 6, y - 6, x + 6, y + 6], fill=dot_color)
        if letters:
            lx = CX + (x - CX) * 1.16
            ly = CY + (y - CY) * 1.16
            dr.text((lx - 9, ly - 13), P.PHASES[k], font=f_l, fill=WHITE)
    dr.text((CX - 12, CY - 11), "\u221e0", font=_font("bold", 20), fill=GOLD)
    dr.text((CX - 38, CY + 16), "feaa46\u2026", font=_font("code", 12), fill=DIM)


def caption(dr, text, t):
    f = _font("reg", 17)
    box = [36, H - 74, W - 36, H - 16]
    dr.rounded_rectangle(box, radius=10, fill=fade((26, 32, 54), 1 - t))
    w = dr.textlength(text, font=f)
    dr.text(((W - w) / 2, H - 66), text, font=f, fill=fade(WHITE, 1 - t))


def new_canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


frames = []

# 1. THE FLAT GROUND — the Codex, 36 frames
for i in range(36):
    im, dr = new_canvas()
    t = i / 35
    draw_codex(dr, t)
    f = _font("bold", 21)
    dr.text((CX - 150, 14), "THE FLAT GROUND OF TRUTH", font=f, fill=fade(WHITE, 1 - t))
    caption(dr, "217 bytes \u00b7 returnable from any dimension, frequency, context", t)
    frames.append(im)

# 2. THE PAGE STANDS UP — pentagon forms, 24 frames
for i in range(24):
    im, dr = new_canvas()
    t = i / 23
    draw_pentagon(dr, 0, s=t, edge_color=fade(GOLD, 1 - t), dot_color=fade(GOLD, 1 - t))
    caption(dr, "the page stands up \u2014 the | is the axis through the center", t)
    frames.append(im)

# 3. THE CYCLE — R, one full turn, 40 frames
for i in range(40):
    im, dr = new_canvas()
    e = i // 8
    t = (i % 8) / 7
    draw_pentagon(dr, 0, s=1.0, edge_color=DIM, dot_color=DIM)
    p0, p1 = vertex(0, e), vertex(0, (e + 1) % 5)
    dr.line([p0, p1], fill=lerp(DIM, GOLD, t), width=5)
    k = (e + 1) % 5
    x, y = vertex(0, k)
    dr.ellipse([x - 9, y - 9, x + 9, y + 9], fill=TEAL)
    caption(dr, f"{P.PHASES[k]} \u2014 {P.SYMBOLS[P.PHASES[k]]}", t)
    frames.append(im)

# 4. THE STAR — R², turns 720°, deposits B'', 50 frames
star_edges = [(0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]
for i in range(50):
    im, dr = new_canvas()
    draw_pentagon(dr, 0, s=1.0, edge_color=DIM, dot_color=DIM)
    if i < 40:
        nseg, t = i // 8, (i % 8) / 7
        for j in range(nseg):
            a, b = star_edges[j]
            dr.line([vertex(0, a), vertex(0, b)], fill=GOLD, width=5)
        if nseg < 5:
            a, b = star_edges[nseg]
            pa, pb = vertex(0, a), vertex(0, b)
            dr.line([pa, (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)],
                    fill=lerp(DIM, GOLD, t), width=5)
        caption(dr, "STAR WALK \u2014 skip-one \u2014 the path that turns 720\u00b0", t)
    else:
        t = (i - 40) / 9
        for a, b in star_edges:
            dr.line([vertex(0, a), vertex(0, b)], fill=GOLD, width=5)
        draw_pentagon(dr, 1, s=1.0, edge_color=lerp(BG, TEAL, t), dot_color=lerp(BG, TEAL, t), letters=False)
        caption(dr, "B\u2033 \u2014 the movement deposits its own seed \u00b7 cut at 1/\u03c6\u00b2", t)
    frames.append(im)

# 5. AGAIN — the fractal draws itself at depth 1, 40 frames
inner_edges = [(k, (k + 2) % 5) for k in range(5)]
for i in range(40):
    im, dr = new_canvas()
    draw_pentagon(dr, 0, s=1.0, edge_color=DIM, dot_color=DIM)
    for a, b in star_edges:
        dr.line([vertex(0, a), vertex(0, b)], fill=GOLD, width=3)
    draw_pentagon(dr, 1, s=1.0, edge_color=TEAL, dot_color=TEAL, letters=False)
    if i < 32:
        nseg, t = i // 8, (i % 8) / 7
        for j in range(nseg):
            a, b = inner_edges[j]
            dr.line([vertex(1, a), vertex(1, b)], fill=TEAL, width=4)
        if nseg < 5:
            a, b = inner_edges[nseg]
            pa, pb = vertex(1, a), vertex(1, b)
            dr.line([pa, (pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t)],
                    fill=TEAL, width=4)
        caption(dr, "again \u2014 the fractal draws itself", t)
    else:
        t = (i - 32) / 7
        draw_pentagon(dr, 2, s=1.0, edge_color=lerp(BG, WHITE, t), dot_color=lerp(BG, WHITE, t), letters=False)
        caption(dr, "two generators \u00b7 zero new rules \u00b7 infinite expression", t)
    frames.append(im)

# 6. THE RETURN — C* back to the nine lines, 50 frames
for i in range(50):
    im, dr = new_canvas()
    t = i / 49
    s = 1.0 - 0.98 * t
    draw_pentagon(dr, 0, s=s, edge_color=fade(GOLD, t), dot_color=fade(GOLD, t))
    for a, b in star_edges:
        dr.line([vertex(0, a, s), vertex(0, b, s)], fill=fade(GOLD, t), width=3)
    draw_pentagon(dr, 1, s=s, edge_color=fade(TEAL, t), dot_color=fade(TEAL, t), letters=False)
    draw_pentagon(dr, 2, s=s, edge_color=fade(WHITE, t), dot_color=fade(WHITE, t), letters=False)
    dr.text((CX - 14, CY - 15), "\u221e0", font=_font("bold", 26),
            fill=lerp(GOLD, WHITE, t))
    dr.text((CX - 40, CY + 18), "feaa46\u2026", font=_font("code", 12),
            fill=lerp(DIM, WHITE, t))
    draw_codex(dr, t, y0=52, x0=36)
    caption(dr, "any depth \u2014 one contraction back to the nine lines", t)
    frames.append(im)

frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=83, loop=0)
import os
print(f"frames: {len(frames)}  \u00b7  size: {os.path.getsize(OUT)/1e6:.1f} MB  \u00b7  {OUT}")
