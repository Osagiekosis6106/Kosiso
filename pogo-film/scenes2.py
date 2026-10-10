"""Preview 2 scenes (v2 look: real film + blueprint overlays, grid, glow, grain, camera moves).
Usage: python3 scenes2.py OUTDIR [scene ...]"""
import sys, math, os
from PIL import Image, ImageDraw
import gfx
from gfx import SS, W, H, AMBER, STEEL, OFFWHITE, RED, GREEN, GREY, GRAPHITE, ease, text
from scenes import arrow, lerp, GROUND_Y, ground

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT = lambda n: os.path.join(HERE, "footage", "shots", n)

def tint(img, k, color=(18, 26, 36), amount=0.5):
    """Darken and cool a frozen film frame so overlays read clearly (k = 0..1)."""
    if k <= 0: return img
    return Image.blend(img, Image.new("RGB", img.size, color), amount * k)

# ---------------------------------------------------------------- S01 hook: typewriter date on black, hard cut to the real Pogo hanging on its propellers
_D = {}
def v2_s01_hook(t, i):
    if t < 2.4:
        img = Image.new("RGB", (W * SS, H * SS), (8, 8, 10)); d = ImageDraw.Draw(img)
        s = "NOVEMBER 1954"; n = min(len(s), int(max(0, t - 0.3) / 0.1))
        shown = s[:n] + ("_" if int(t * 2.5) % 2 == 0 else " ")
        flick = 0.85 + 0.15 * math.sin(i * 1.7) ** 2
        text(d, (960, 540), shown, 64, tuple(int(c * flick) for c in AMBER), path=gfx.F_MONO)
        return gfx.finish(img, i, grain=9)
    if "D" not in _D: _D["D"] = gfx.Footage(SHOT("D_lowangle_hanging.mp4"), crop_y=0.45)
    k = (t - 2.4) / 3.1
    img = _D["D"].frame(int((t - 2.4) * gfx.FPS))
    img = gfx.camera(img, 1.0 + 0.10 * ease(k), 1150, 430)
    return gfx.finish(img, i, grain=6)

# ---------------------------------------------------------------- S34: real film plays, freezes, zooms in, X-ray sight lines drawn over the real aircraft
F_CANOPY = (952, 681); F_NOSE = (939, 575); F_BASE_Y = 839; F_WING = (832, 1053)   # 1080p positions in shot F (crop_y 0.5)
Z, ZC = 2.0, (950, 700)
_F = {}

def zoom_pt(p, z):
    w, h = W / z, H / z
    x0 = min(max(ZC[0] - w / 2, 0), W - w); y0 = min(max(ZC[1] - h / 2, 0), H - h)
    return ((p[0] - x0) * z, (p[1] - y0) * z)

def corners(d, box, k, color=AMBER, L=34):
    x0, y0, x1, y1 = box; a = int(255 * ease(k / 0.4)); L = L * ease(k / 0.6)
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([(x * SS, y * SS), ((x + sx * L) * SS, y * SS)], fill=color + (a,), width=3 * SS)
        d.line([(x * SS, y * SS), (x * SS, (y + sy * L) * SS)], fill=color + (a,), width=3 * SS)

def v2_s34_xray(t, i):
    if "F" not in _F: _F["F"] = gfx.Footage(SHOT("F_standing_wide.mp4"), start=1.0, crop_y=0.5)
    FREEZE = 1.6
    img = _F["F"].frame(int(min(t, FREEZE) * gfx.FPS))
    zk = ease((t - FREEZE - 0.15) / 1.3); z = 1 + (Z - 1) * zk
    img = gfx.camera(img, z, *ZC) if z > 1.001 else img
    img = tint(img, ease((t - FREEZE) / 1.0), amount=0.55)
    if FREEZE <= t < FREEZE + 0.12:                      # shutter flash on the freeze
        img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.35)
    if t > FREEZE + 0.2:
        S = lambda p: zoom_pt(p, z)
        canopy = S(F_CANOPY); nose = S(F_NOSE); base = S((F_CANOPY[0], F_BASE_Y))
        wl = S((F_WING[0], F_BASE_Y)); wr = S((F_WING[1], F_BASE_Y))
        d = ImageDraw.Draw(img, "RGBA")
        if t > 3.0: corners(d, (wl[0] - 30, nose[1] - 40, wr[0] + 30, base[1] + 14), t - 3.0)
        if t > 3.0: text(d, (wl[0] - 30, base[1] + 46), "XFY-1 · STANDING ON ITS TAIL", 22, AMBER, anchor="lm")
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        a1 = ease((t - 4.4) / 0.9)
        if a1 > 0:                                      # in front of him: sky
            top = 40; spread = 330 * a1
            ld.polygon([(canopy[0] * SS, canopy[1] * SS), ((canopy[0] - spread) * SS, top * SS), ((canopy[0] + spread) * SS, top * SS)],
                       fill=STEEL + (int(70 * a1),), outline=STEEL + (int(220 * a1),))
        a2 = ease((t - 6.0) / 0.9)
        if a2 > 0:                                      # below him: his own aircraft
            ld.polygon([(canopy[0] * SS, canopy[1] * SS), ((canopy[0] - 120) * SS, base[1] * SS), ((canopy[0] + 120) * SS, base[1] * SS)],
                       fill=RED + (int(85 * a2),), outline=RED + (int(230 * a2),))
        gfx.glow(img, layer, radius=8, strength=0.8)
        d = ImageDraw.Draw(img, "RGBA")
        if a1 > 0.9: text(d, (canopy[0], 70), "IN FRONT OF HIM: SKY", 32, STEEL)
        if a2 > 0.9: gfx.callout(img, (canopy[0] + 60, (canopy[1] + base[1]) / 2), (canopy[0] + 300, (canopy[1] + base[1]) / 2 + 10),
                                 ["BELOW HIM: HIS OWN AIRCRAFT"], RED, k=min(1, (t - 6.8) / 0.8), size=28)
        a3 = ease((t - 7.7) / 1.2)
        if a3 > 0:                                      # over his shoulder, curving back down to the ground
            pts = [(canopy[0] - 30 - 520 * math.sin(u * math.pi / 2), canopy[1] - 140 * math.sin(u * math.pi) + (base[1] + 30 - canopy[1]) * u ** 2)
                   for u in [k / 40 for k in range(int(40 * a3) + 1)]]
            gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
            for n in range(0, len(pts) - 1, 2):
                gd.line([(pts[n][0] * SS, pts[n][1] * SS), (pts[n + 1][0] * SS, pts[n + 1][1] * SS)], fill=GREEN + (255,), width=5 * SS)
            gfx.glow(img, gl, radius=8)
            d = ImageDraw.Draw(img, "RGBA")
            if a3 > 0.97:
                arrow(d, pts[-3], pts[-1], GREEN, 5, head=20)
                text(d, (70, 250), "OVER HIS SHOULDER:", 30, GREEN, anchor="lm")
                text(d, (70, 288), "THE ONLY VIEW OF THE GROUND", 30, GREEN, anchor="lm")
        if t > 3.6: gfx.callout(img, canopy, (canopy[0] + 260, canopy[1] - 120), ["PILOT"], AMBER, k=min(1, (t - 3.6) / 0.9), size=30)
    return gfx.finish(img, i, grain=6)

# ---------------------------------------------------------------- S33 v2: blueprint pitch-up to the tail-first landing
STEPS = ["LEVEL FLIGHT", "NOSE UP", "HANGING ON THE PROPELLERS", "DOWN, TAIL FIRST", "TOUCHDOWN"]

def v2_s33_pitch(t, i):
    img = gfx.grid_background(t)
    rot = 90 * ease((t - 1.0) / 2.6)
    sc = 16; top = 500; land = gfx.stand_cy(GROUND_Y, sc)
    sink = ease((t - 4.0) / 2.4)
    cx, cy = 960 - 140 * (1 - ease((t - 0.2) / 3.4)), top + (land - top) * sink
    g = ease((t - 3.2) / 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    if g > 0: ground(d, g)
    if t > 4.0:                                          # descent trail
        for y in range(int(top), int(cy), 26):
            d.line([((cx - 230) * SS, y * SS), ((cx - 230) * SS, (y + 12) * SS)], fill=STEEL + (110,), width=3 * SS)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gfx.draw_pogo(layer, rot, cx, cy, sc, props_spin=t * 4)
    gfx.glow(img, layer, radius=9, strength=0.9)
    d = ImageDraw.Draw(img, "RGBA")
    step = 0 if t < 1.2 else 1 if t < 3.6 else 2 if t < 4.2 else 3 if t < 6.4 else 4
    since = t - [0, 1.2, 3.6, 4.2, 6.4][step]
    s = STEPS[step]; n = min(len(s), int(since / 0.03) + 1)
    text(d, (960, 108), s[:n], 42, AMBER if step else STEEL)
    for k in range(len(STEPS)):                          # step dots
        x = 960 - 2 * 34 + k * 34; r = 7 * SS
        d.ellipse([x * SS - r, 160 * SS - r, x * SS + r, 160 * SS + r], fill=(AMBER + (255,)) if k <= step else (GREY + (120,)))
    if 4.2 < t < 6.4:                                    # thrust just under weight: sinking slowly
        tx, ty = cx + 230, cy
        arrow(d, (tx, ty - 10), (tx, ty - 120), STEEL, 4, head=16); text(d, (tx + 18, ty - 100), "THRUST", 22, STEEL, anchor="lm")
        arrow(d, (tx, ty + 10), (tx, ty + 132), AMBER, 4, head=16); text(d, (tx + 18, ty + 110), "WEIGHT", 22, AMBER, anchor="lm")
    z = 1.0 + 0.05 * ease(t / 7.0)
    return gfx.finish(gfx.camera(img, z, 960, 560), i, grain=5)

SCENES = {
    "V2_S01_hook": (5.2, v2_s01_hook),
    "V2_S34_xray": (11.0, v2_s34_xray),
    "V2_S33_pitch": (7.5, v2_s33_pitch),
}

if __name__ == "__main__":
    out = sys.argv[1]; names = sys.argv[2:] or list(SCENES)
    for nme in names:
        sec, fn = SCENES[nme]
        gfx.render1x(f"{out}/{nme}.mp4", sec, fn); print("rendered", nme)
