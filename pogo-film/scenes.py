"""Graphic scenes for the Convair Pogo film. Usage: python3 scenes.py OUTDIR [scene ...]"""
import sys, math
from PIL import Image, ImageDraw
import gfx
from gfx import SS, W, H, AMBER, STEEL, OFFWHITE, RED, GREEN, GREY, GRAPHITE, ease, text

def arrow(d, a, b, color, width=4, head=18, dash=0):
    (x1, y1), (x2, y2) = a, b
    if dash:
        L = math.hypot(x2 - x1, y2 - y1); n = int(L / dash)
        for i in range(0, n, 2):
            p = (x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n); q = (x1 + (x2 - x1) * (i + 1) / n, y1 + (y2 - y1) * (i + 1) / n)
            d.line([(p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)], fill=color, width=width * SS)
    else:
        d.line([(x1 * SS, y1 * SS), (x2 * SS, y2 * SS)], fill=color, width=width * SS)
    ang = math.atan2(y2 - y1, x2 - x1)
    for s in (-1, 1):
        d.line([(x2 * SS, y2 * SS), ((x2 - head * math.cos(ang + s * 0.45)) * SS, (y2 - head * math.sin(ang + s * 0.45)) * SS)], fill=color, width=width * SS)

def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

# S01: typewriter date (alpha overlay for the archival film; also a preview over black)
def s01_typewriter(t, i, alpha=False):
    img = Image.new("RGBA" if alpha else "RGB", (W * SS, H * SS), (0, 0, 0, 0) if alpha else (10, 10, 12))
    d = ImageDraw.Draw(img)
    s = "NOVEMBER 1954"; n = min(len(s), int(max(0, t - 0.3) / 0.11))
    shown = s[:n] + ("|" if int(t * 2.5) % 2 == 0 else " ")
    text(d, (960, 90), shown, 46, AMBER, path=gfx.F_MONO)
    return img

# S09: title card
def s09_title(t, i):
    img = gfx.background(); d = ImageDraw.Draw(img)
    a = ease(t / 0.8)
    col = tuple(int(c * a) for c in OFFWHITE)
    text(d, (960, 470), "HANGAR PHYSICS", 92, col, spacing=18)
    w = 520 * ease((t - 0.4) / 0.8)
    d.line([((960 - w) * SS, 545 * SS), ((960 + w) * SS, 545 * SS)], fill=AMBER, width=3 * SS)
    b = ease((t - 0.9) / 0.8)
    text(d, (960, 600), "Every strange aircraft is the answer to a problem.", 30, tuple(int(c * b) for c in AMBER))
    return img

GROUND_Y = 900

def ground(d, alpha=1.0, label=True):
    c = tuple(int(v * alpha) for v in GREY)
    d.line([(160 * SS, GROUND_Y * SS), (1760 * SS, GROUND_Y * SS)], fill=c, width=3 * SS)
    for x in range(160, 1760, 40):
        d.line([(x * SS, GROUND_Y * SS), ((x - 18) * SS, (GROUND_Y + 18) * SS)], fill=c, width=2 * SS)
    if label: text(d, (1700, GROUND_Y + 40), "GROUND", 22, c, anchor="rm")

# S18: "the ground is behind his back"
def s18_ground_behind(t, i):
    img = gfx.background(); d = ImageDraw.Draw(img)
    cx, sc = 1060, 20; cy = gfx.stand_cy(GROUND_Y, sc)
    gfx.draw_pogo(img, 90, cx, cy, sc, props_spin=t * 3); d = ImageDraw.Draw(img); ground(d)
    px, py = gfx.pogo_point(gfx.COCKPIT, 90, cx, cy, sc)
    nx, ny = gfx.pogo_point((36.5, 0), 90, cx, cy, sc)
    r = 9; d.ellipse([(px - r) * SS, (py - r) * SS, (px + r) * SS, (py + r) * SS], fill=AMBER)
    if t > 0.6: text(d, (px + 60, py), "PILOT", 26, AMBER, anchor="lm")
    k = ease((t - 1.2) / 1.0)
    if k > 0:
        arrow(d, (nx, ny - 30), lerp((nx, ny - 30), (nx, 40), k), STEEL, 4)
        if k > 0.9: text(d, (nx + 30, 60), "FACING: SKY", 30, STEEL, anchor="lm")
    k2 = ease((t - 2.6) / 1.4)
    if k2 > 0:
        pts = [(px - 20, py + 5), (px - 330, py + 150), (px - 380, GROUND_Y - 25)]
        end = lerp(pts[1], pts[2], k2) if k2 > 0.5 else lerp(pts[0], pts[1], k2 * 2)
        arrow(d, pts[0], end if k2 <= 0.5 else pts[1], AMBER, 4, head=0 if k2 > 0.5 else 18, dash=14)
        if k2 > 0.5: arrow(d, pts[1], end, AMBER, 4, dash=14)
        if k2 > 0.95: text(d, (px - 360, py + 100), "GROUND: BEHIND HIM", 36, AMBER, anchor="rm")
    return img

# S33: level flight -> pitch up to vertical -> sink tail-first
def s33_pitch_up(t, i):
    img = gfx.background(); d = ImageDraw.Draw(img)
    rot = 90 * ease((t - 1.0) / 2.6)
    top = 520; land = gfx.stand_cy(GROUND_Y, 16)
    cx, cy = 960, top + (land - top) * ease((t - 4.0) / 2.4)
    g = ease((t - 3.2) / 0.8)
    if g > 0: ground(d, g)
    gfx.draw_pogo(img, rot, cx, cy, 16, props_spin=t * 4); d = ImageDraw.Draw(img)
    label = "LEVEL FLIGHT" if t < 1.2 else ("NOSE UP…" if t < 3.6 else ("HANGING ON THE PROPELLERS" if t < 4.2 else ("DOWN, TAIL FIRST" if t < 6.4 else "TOUCHDOWN")))
    text(d, (960, 110), label, 40, AMBER if t >= 1.2 else STEEL)
    if 4.2 < t < 6.4:
        for k in range(3):
            y = 230 + k * 50 + (t * 120) % 50
            arrow(d, (1320, y), (1320, y + 30), STEEL, 3, head=10)
    return img

# S34: what he could see
def s34_sightlines(t, i):
    img = gfx.background(); d = ImageDraw.Draw(img)
    cx, sc = 1080, 19; cy = gfx.stand_cy(GROUND_Y, sc)
    gfx.draw_pogo(img, 90, cx, cy, sc, props_spin=t * 3); d = ImageDraw.Draw(img); ground(d)
    px, py = gfx.pogo_point(gfx.COCKPIT, 90, cx, cy, sc)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    a1 = ease((t - 0.4) / 0.8)
    if a1 > 0:   # forward view: sky
        ld.polygon([(px * SS, py * SS), ((px - 240) * SS, 60 * SS), ((px + 240) * SS, 60 * SS)], fill=STEEL + (int(70 * a1),))
    a2 = ease((t - 2.2) / 0.8)
    if a2 > 0:   # looking down: own aircraft
        ld.polygon([(px * SS, py * SS), ((px - 120) * SS, (py + 330) * SS), ((px + 120) * SS, (py + 330) * SS)], fill=RED + (int(60 * a2),))
    img.paste(layer, (0, 0), layer); d = ImageDraw.Draw(img)
    if a1 > 0.9: text(d, (px, 40), "IN FRONT: SKY", 32, STEEL)
    if a2 > 0.9:
        text(d, (px + 170, py + 260), "BELOW: HIS OWN AIRCRAFT", 30, RED, anchor="lm")
    a3 = ease((t - 4.0) / 1.4)
    if a3 > 0:
        mid = (px - 330, py + 40); end = (px - 520, GROUND_Y - 10)
        e = lerp((px, py), mid, min(1, a3 * 2)) if a3 < 0.5 else lerp(mid, end, (a3 - 0.5) * 2)
        arrow(d, (px - 10, py), e if a3 < 0.5 else mid, GREEN, 5, head=0 if a3 >= 0.5 else 18, dash=16)
        if a3 >= 0.5: arrow(d, mid, e, GREEN, 5, dash=16)
        if a3 > 0.95:
            text(d, (mid[0] - 30, mid[1] - 60), "OVER HIS SHOULDER:", 30, GREEN, anchor="rm")
            text(d, (mid[0] - 30, mid[1] - 22), "THE ONLY VIEW OF THE GROUND", 30, GREEN, anchor="rm")
    r = 9; d.ellipse([(px - r) * SS, (py - r) * SS, (px + r) * SS, (py + r) * SS], fill=AMBER)
    return img

SCENES = {
    "S01_typewriter": (3.0, s01_typewriter, False),
    "S01_typewriter_alpha": (3.0, lambda t, i: s01_typewriter(t, i, True), True),
    "S09_title": (3.0, s09_title, False),
    "S18_ground_behind": (5.5, s18_ground_behind, False),
    "S33_pitch_up": (7.0, s33_pitch_up, False),
    "S34_sightlines": (7.0, s34_sightlines, False),
}

if __name__ == "__main__":
    out = sys.argv[1]; names = sys.argv[2:] or list(SCENES)
    for n in names:
        sec, fn, alpha = SCENES[n]
        ext = "mov" if alpha else "mp4"
        gfx.render(f"{out}/{n}.{ext}", sec, fn, alpha=alpha); print("rendered", n)
