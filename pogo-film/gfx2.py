"""Hangar Physics v3 graphics: shared drawing helpers and the animated scenes for the Pogo film.
All scenes draw at 2x (SS) on the graphite blueprint grid and return an RGB image of size (W*SS, H*SS)."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import gfx
from gfx import SS, W, H, AMBER, STEEL, OFFWHITE, RED, GREEN, GREY, GRAPHITE, ease

FD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FDB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FSB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FM = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
FMONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
WHITE = (255, 255, 255)
DIM = (150, 160, 172)


@lru_cache(maxsize=256)
def F(path, size):
    return ImageFont.truetype(path, int(size))


def e(t, a, b):
    """0..1 eased progress of t between a and b."""
    if b <= a: return 1.0 if t >= a else 0.0
    return ease((t - a) / (b - a))


def lin(t, a, b):
    if b <= a: return 1.0 if t >= a else 0.0
    return max(0.0, min(1.0, (t - a) / (b - a)))


def mix(c1, c2, k): return tuple(int(c1[i] + (c2[i] - c1[i]) * k) for i in range(3))


def T(d, xy, s, size, col=OFFWHITE, a=1.0, anchor="mm", font=FD, sc=SS, spacing=0):
    """Text at 1x coords (scaled by sc) with alpha."""
    if a <= 0: return
    f = F(font, size * sc)
    x, y = xy[0] * sc, xy[1] * sc
    fill = tuple(col[:3]) + (int(255 * max(0, min(1, a))),)
    if spacing:
        total = sum(d.textlength(c, font=f) for c in s) + spacing * sc * (len(s) - 1)
        cx = x - total / 2 if anchor[0] == "m" else (x - total if anchor[0] == "r" else x)
        for c in s:
            d.text((cx, y), c, font=f, fill=fill, anchor="l" + anchor[1]); cx += d.textlength(c, font=f) + spacing * sc
    else:
        d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def tw(d, s, size, font=FD, sc=SS):
    return d.textlength(s, font=F(font, size * sc)) / sc


def line(d, pts, col, w=3, a=1.0, sc=SS):
    d.line([(x * sc, y * sc) for x, y in pts], fill=tuple(col[:3]) + (int(255 * a),), width=max(1, int(w * sc)), joint="curve")


def dashed(d, pts, col, w=3, a=1.0, dash=14, gap=10, k=1.0, sc=SS):
    """Dashed polyline drawn on up to fraction k of its length."""
    segs = []; total = 0
    for p, q in zip(pts, pts[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1]); segs.append((p, q, L)); total += L
    lim = total * k; pos = 0; on = True; run = 0
    for p, q, L in segs:
        s = 0
        while s < L and pos < lim:
            step = min((dash if on else gap) - run, L - s, lim - pos)
            if on:
                a0 = s / L; a1 = (s + step) / L
                line(d, [(p[0] + (q[0] - p[0]) * a0, p[1] + (q[1] - p[1]) * a0), (p[0] + (q[0] - p[0]) * a1, p[1] + (q[1] - p[1]) * a1)], col, w, a, sc)
            s += step; pos += step; run += step
            if run >= (dash if on else gap): on = not on; run = 0


def arrow(d, a_, b_, col, w=4, head=18, a=1.0, sc=SS, dash=False):
    if dash: dashed(d, [a_, b_], col, w, a, sc=sc)
    else: line(d, [a_, b_], col, w, a, sc)
    ang = math.atan2(b_[1] - a_[1], b_[0] - a_[0])
    p1 = (b_[0] - head * math.cos(ang - 0.42), b_[1] - head * math.sin(ang - 0.42))
    p2 = (b_[0] - head * math.cos(ang + 0.42), b_[1] - head * math.sin(ang + 0.42))
    d.polygon([(b_[0] * sc, b_[1] * sc), (p1[0] * sc, p1[1] * sc), (p2[0] * sc, p2[1] * sc)], fill=tuple(col[:3]) + (int(255 * a),))


def circle(d, c, r, col=None, fill=None, w=3, a=1.0, sc=SS):
    x, y = c
    d.ellipse([(x - r) * sc, (y - r) * sc, (x + r) * sc, (y + r) * sc],
              outline=(tuple(col[:3]) + (int(255 * a),)) if col else None,
              fill=(tuple(fill[:3]) + (int(fill[3] * a) if len(fill) > 3 else int(255 * a),)) if fill else None,
              width=max(1, int(w * sc)))


def arc_arrow(d, c, r, a0, a1, col, w=4, a=1.0, head=16, sc=SS):
    """Arc from angle a0 to a1 (degrees, screen coords, 0 = right, positive = clockwise on screen)."""
    n = 40; pts = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n); pts.append((c[0] + r * math.cos(t), c[1] + r * math.sin(t)))
    line(d, pts, col, w, a, sc)
    arrow(d, pts[-3], pts[-1], col, w, head, a, sc)


def layer(): return Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))


def fglow(img, lay, r=10, s=1.0):
    """Paste lay with a soft bloom, blurred at quarter resolution for speed."""
    w, h = lay.size
    sm = lay.resize((w // 4, h // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1, r * SS / 4)))
    if s != 1.0:
        al = sm.getchannel("A").point(lambda v: int(min(255, v * s))); sm.putalpha(al)
    big = sm.resize((w, h), Image.BILINEAR)
    img.paste(big, (0, 0), big); img.paste(lay, (0, 0), lay)


_BG = {}
def bg(kind="grid"):
    if kind not in _BG:
        if kind == "grid": _BG[kind] = gfx.grid_background(0)
        elif kind == "black": _BG[kind] = Image.new("RGB", (W * SS, H * SS), (8, 9, 11))
        else: _BG[kind] = gfx.background()
    return _BG[kind].copy()


def heading(d, s, a=1.0, y=96, col=AMBER, size=40):
    T(d, (960, y), s, size, col, a, spacing=4)


def stamp(d, xy, s, col=RED, a=1.0, size=44, rot=0):
    """Rubber-stamp style boxed label."""
    if a <= 0: return
    w_ = tw(d, s, size, FDB) + 40; h_ = size + 26
    x, y = xy
    line(d, [(x - w_ / 2, y - h_ / 2), (x + w_ / 2, y - h_ / 2), (x + w_ / 2, y + h_ / 2), (x - w_ / 2, y + h_ / 2), (x - w_ / 2, y - h_ / 2)], col, 5, a)
    T(d, (x, y + 2), s, size, col, a, font=FDB)


# ---------------------------------------------------------------- aircraft drawings
def pogo(lay, ang, cx, cy, sc, spin=0.0, fill=STEEL, alpha=110, edge=None):
    gfx.draw_pogo(lay, ang, cx, cy, sc, props_spin=spin, fill=fill, alpha=alpha, edge=edge)


def P(pt, ang, cx, cy, sc): return gfx.pogo_point(pt, ang, cx, cy, sc)


GROUND = 900
def ground(d, a=1.0, y=GROUND, x0=160, x1=1760, label=None):
    c = tuple(int(v) for v in GREY)
    line(d, [(x0, y), (x1, y)], c, 3, a)
    for x in range(x0, x1, 40): line(d, [(x, y), (x - 16, y + 16)], c, 2, a * 0.8)
    if label: T(d, (x1 - 10, y + 40), label, 22, GREY, a, anchor="rm", font=FSB)


def rot(pts, ang, cx, cy, s):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s) for x, y in pts]


# Rear (or front) view of the Pogo: wings along x, fins along y (feet; y down on screen = bottom fin).
R_FUS = 2.8; R_SPAN = 13.8; R_FIN = 11.0
def rear(lay, cx, cy, s, roll=0.0, col=STEEL, alpha=110, wheels=True, wheel_hl=0.0, props=0, spin=0.0,
         prop_dirs=(1, -1), pod_hl=0.0, draw_k=1.0):
    d = ImageDraw.Draw(lay)
    edge = tuple(min(255, c + 60) for c in col)
    k = draw_k
    wing = [(R_FUS * 0.8, -0.45), (R_FUS + (R_SPAN - R_FUS) * k, -0.25), (R_FUS + (R_SPAN - R_FUS) * k, 0.25), (R_FUS * 0.8, 0.45)]
    fin = [(-0.5, R_FUS * 0.8), (-0.28, R_FUS + (R_FIN - R_FUS) * k), (0.28, R_FUS + (R_FIN - R_FUS) * k), (0.5, R_FUS * 0.8)]
    polys = [wing, [(-x, y) for x, y in wing], fin, [(x, -y) for x, y in fin]]
    for p in polys:
        q = rot(p, roll, cx, cy, s); q2 = [(x * SS, y * SS) for x, y in q]
        d.polygon(q2, fill=col + (alpha,)); d.line(q2 + [q2[0]], fill=edge + (255,), width=3 * SS)
    # wingtip pods
    if k > 0.98:
        for sx in (-1, 1):
            c = rot([(sx * R_SPAN, 0)], roll, cx, cy, s)[0]
            hl = pod_hl if sx == -1 else 0
            circle(d, c, 0.75 * s, mix(edge, AMBER, hl), fill=col + (alpha,), w=3)
    # fuselage
    c = rot([(0, 0)], roll, cx, cy, s)[0]
    circle(d, c, R_FUS * s, edge, fill=col + (alpha + 30,), w=3)
    circle(d, c, R_FUS * 0.45 * s, edge, w=2, a=0.7)
    if wheels and k > 0.98:
        tips = [(R_SPAN, 0.0), (-R_SPAN, 0.0), (0.0, R_FIN), (0.0, -R_FIN)]
        for tx, ty in tips:
            off = (0, 1.0) if ty == 0 else (0, 0.9 * (1 if ty > 0 else -1))
            # wheels hang toward the ground (screen down) at the tips: strut then wheel
            base = rot([(tx, ty)], roll, cx, cy, s)[0]
            wpos = rot([(tx, ty + 1.2 if ty >= 0 else ty - 1.2)], roll, cx, cy, s)[0] if ty != 0 else rot([(tx, ty + 1.3)], roll, cx, cy, s)[0]
            colw = mix(edge, AMBER, wheel_hl)
            line(d, [base, wpos], colw, 3)
            circle(d, wpos, 0.55 * s, colw, fill=(colw + (200,)) if wheel_hl > 0.3 else None, w=3)
            if wheel_hl > 0:
                circle(d, wpos, (0.55 + 1.6 * wheel_hl) * s, AMBER, w=2, a=0.6 * wheel_hl)
    if props:
        for i in range(props):
            dirn = prop_dirs[i]
            r = 8.0 * s * (1 - 0.06 * i)
            col_p = AMBER
            circle(d, c, r, col_p, w=2, a=0.35, fill=col_p + (22,))
            for b in range(3):
                a_ = spin * dirn * 2 * math.pi + b * 2 * math.pi / 3 + i * 0.5
                bl = [(c[0] + math.cos(a_ + o) * r * f, c[1] + math.sin(a_ + o) * r * f) for o, f in ((-0.07, 0.2), (-0.03, 1.0), (0.03, 1.0), (0.07, 0.2))]
                d.polygon([(x * SS, y * SS) for x, y in bl], fill=col_p + (170 if i == 0 else 120,))


def rear_ground_cy(ground_y, s, roll=0.0):
    """cy so the lowest wheel touches ground_y when standing (fin down)."""
    return ground_y - (R_FIN + 1.2 + 0.55) * s


CAR = [(-2.3, 0), (-2.3, -0.75), (-1.6, -0.85), (-1.0, -1.35), (0.7, -1.35), (1.3, -0.85), (2.3, -0.7), (2.3, 0)]
CARRIER = [(-12, 0), (12, 0), (13.5, -1.4), (-12.5, -1.4)]
ISLAND = [(3, -1.4), (5, -1.4), (5, -3.6), (3.6, -3.6), (3.6, -4.6), (3.3, -4.6), (3.3, -1.4)]
SHIP = [(-10, 0), (9, 0), (11, -2.2), (-10.5, -2.0)]
SHIP_SUP = [(-8.5, -2.0), (-4.5, -2.0), (-4.5, -4.2), (-8.5, -4.2)]


def poly(d, pts, cx, cy, s, col, a=1.0, fill_a=60, w=3):
    q = [((cx + x * s) * SS, (cy + y * s) * SS) for x, y in pts]
    d.polygon(q, fill=col + (int(fill_a * a),)); d.line(q + [q[0]], fill=col + (int(255 * a),), width=w * SS)


def waves(d, y, t, a=1.0, x0=0, x1=1920, col=STEEL):
    pts = [(x, y + 6 * math.sin(x / 60 + t * 2)) for x in range(x0, x1 + 1, 12)]
    line(d, pts, col, 3, a * 0.8)
    pts = [(x, y + 26 + 5 * math.sin(x / 45 - t * 1.6)) for x in range(x0, x1 + 1, 12)]
    line(d, pts, col, 2, a * 0.4)


# ================================================================ scenes  (tl = local time, D = duration)
def sc_typewriter(text, sub=None):
    def f(tl, D):
        img = bg("black"); d = ImageDraw.Draw(img, "RGBA")
        n = min(len(text), int(max(0, tl - 0.35) / 0.1))
        cur = "_" if (int(tl * 2.6) % 2 == 0 or n < len(text)) else " "
        flick = 0.88 + 0.12 * math.sin(tl * 37) ** 2
        T(d, (960, 520), text[:n] + cur, 66, mix((0, 0, 0), AMBER, flick), 1.0, font=FMONO)
        if sub: T(d, (960, 600), sub, 26, DIM, e(tl, 0.35 + len(text) * 0.1, 0.35 + len(text) * 0.1 + 0.6), font=FSB, spacing=3)
        return img
    return f


def sc_title(tl, D):
    img = bg("grid"); lay = layer()
    pogo(lay, 90, 1450, 560, 13, spin=tl * 3, fill=STEEL, alpha=int(40 * e(tl, 0, 1)))
    img.paste(lay, (0, 0), lay)
    d = ImageDraw.Draw(img, "RGBA")
    a = e(tl, 0.0, 0.6)
    T(d, (960, 490), "HANGAR PHYSICS", 104, OFFWHITE, a, font=FDB, spacing=16)
    w = 600 * e(tl, 0.3, 1.1)
    line(d, [(960 - w, 568), (960 + w, 568)], AMBER, 3)
    T(d, (960, 626), "Every strange aircraft is the answer to a problem.", 32, AMBER, e(tl, 0.8, 1.5), font=FSB)
    return img


def sc_name_overlay(tl, D):
    """Big name card drawn over film (returns RGBA overlay at SS)."""
    lay = layer(); d = ImageDraw.Draw(lay, "RGBA")
    a = e(tl, 0.15, 0.7) * (1 - e(tl, D - 0.35, D))
    sl = (1 - e(tl, 0.15, 0.8)) * 40
    d.rectangle([0, 700 * SS, W * SS, H * SS], fill=(10, 12, 15, int(150 * a)))
    line(d, [(110 - sl, 790), (118 - sl, 790)], AMBER, 8, a)
    line(d, [(110, 760), (110, 960)], AMBER, 6, a)
    T(d, (140 - sl, 820), "CONVAIR XFY-1", 40, AMBER, a, anchor="ls", font=FSB, spacing=6)
    T(d, (136 - sl, 940), "POGO", 132, OFFWHITE, a, anchor="ls", font=FDB, spacing=10)
    T(d, (1800, 940), "U.S. NAVY  ·  1954", 26, DIM, a, anchor="rs", font=FSB, spacing=4)
    return lay


def sc_danger(tl, D):
    """Too fast: slams onto its tail. Drift: tips over."""
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    sc = 15; land = gfx.stand_cy(GROUND, sc); cx = 960
    ground(d)
    lay = layer(); shake = 0; tilt = 90
    if tl < 3.4:
        k = lin(tl, 0.3, 1.5) ** 2
        cy = 330 + (land - 330) * k
        if tl > 1.5: shake = 10 * math.exp(-(tl - 1.5) * 5) * math.sin(tl * 60)
        pogo(lay, 90, cx + shake, cy, sc, spin=tl * 4)
        fglow(img, lay, 8, 0.8); d = ImageDraw.Draw(img, "RGBA")
        if tl < 1.5:
            for i in range(3):
                y = cy - 220 - i * 46
                arrow(d, (cx + 210, y), (cx + 210, y + 32), RED, 4, 12, 0.8)
        T(d, (960, 120), "COME DOWN TOO FAST…", 46, RED, e(tl, 0.2, 0.6))
        if tl > 1.5:
            fl = math.exp(-(tl - 1.5) * 4)
            circle(d, (cx, GROUND), 40 + 260 * (1 - fl), RED, w=4, a=fl)
            T(d, (960, 190), "…IT SLAMS ONTO ITS TAIL", 40, OFFWHITE, e(tl, 1.55, 1.9))
    else:
        t2 = tl - 3.4
        drift = 180 * e(t2, 0.2, 2.0)
        tilt = 90 - 26 * e(t2, 1.2, 2.4)
        cy = land - 30 + 30 * e(t2, 0.0, 1.0)
        pogo(lay, tilt, cx - 120 + drift, cy, sc, spin=tl * 4)
        fglow(img, lay, 8, 0.8); d = ImageDraw.Draw(img, "RGBA")
        arrow(d, (cx - 380, cy - 140), (cx - 240 + drift * 0.6, cy - 140), AMBER, 5, 18, e(t2, 0.1, 0.5))
        T(d, (960, 120), "DRIFT SIDEWAYS…", 46, AMBER, e(t2, 0.0, 0.4))
        T(d, (960, 190), "…AND IT CAN TIP OVER", 40, OFFWHITE, e(t2, 1.2, 1.6))
        if t2 > 1.4: stamp(d, (1500, 520), "TIP-OVER", RED, e(t2, 1.5, 1.8), 40)
    return img


def sc_text_card(lines, sub=None):
    def f(tl, D):
        img = bg("grid"); lay = layer()
        pogo(lay, 90, 960, 560, 15, spin=tl * 2, fill=STEEL, alpha=25)
        img.paste(lay, (0, 0), lay); d = ImageDraw.Draw(img, "RGBA")
        img.paste(Image.new("RGB", img.size, (10, 12, 15)), (0, 0), Image.new("L", img.size, 120))
        d = ImageDraw.Draw(img, "RGBA")
        for i, s in enumerate(lines):
            T(d, (960, 520 + i * 110 - (len(lines) - 1) * 55), s, 96, OFFWHITE, e(tl, 0.1 + i * 0.25, 0.6 + i * 0.25), font=FDB, spacing=6)
        w = 300 * e(tl, 0.4, 1.0)
        line(d, [(960 - w, 600 + (len(lines) - 1) * 55), (960 + w, 600 + (len(lines) - 1) * 55)], AMBER, 4)
        if sub: T(d, (960, 680), sub, 30, AMBER, e(tl, 0.8, 1.3), font=FSB)
        return img
    return f


def sc_runway_carrier(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    heading(d, "1940s FIGHTERS NEEDED…", e(tl, 0, 0.4))
    # runway (left)
    a1 = e(tl, 0.2, 0.7)
    d.polygon([(250 * SS, 760 * SS), (830 * SS, 760 * SS), (700 * SS, 420 * SS), (380 * SS, 420 * SS)], fill=(60, 66, 74, int(200 * a1)))
    for i in range(7):
        y0 = 440 + i * 46; y1 = y0 + 24
        xw = 6 + i * 1.5
        d.rectangle([(540 - xw) * SS, y0 * SS, (540 + xw) * SS, y1 * SS], fill=OFFWHITE + (int(200 * a1),))
    T(d, (540, 820), "A RUNWAY", 44, OFFWHITE, a1, font=FDB)
    T(d, (960, 600), "OR", 40, DIM, e(tl, 0.9, 1.3), font=FSB)
    # carriers (right): one bright, two ghosts appear then dim
    a2 = e(tl, 1.2, 1.8)
    poly(d, CARRIER, 1380, 700, 18, STEEL, a2, 80); poly(d, ISLAND, 1380, 700, 18, STEEL, a2, 80)
    waves(d, 712, tl, a2, 1080, 1700)
    T(d, (1380, 820), "AN AIRCRAFT CARRIER", 44, OFFWHITE, a2, font=FDB)
    a3 = e(tl, 3.0, 3.6)
    T(d, (1380, 480), "EXPENSIVE", 36, AMBER, a3, font=FSB, spacing=3)
    T(d, (1380, 530), "AND FEW", 36, AMBER, e(tl, 3.6, 4.2), font=FSB, spacing=3)
    return img


def sc_no_runway(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    words = [("NO RUNWAY", 0.0), ("NO CATAPULT", 0.96), ("NO CARRIER", 1.83)]
    shift = -170 * e(tl, 2.8, 3.4)
    for i, (w_, t0) in enumerate(words):
        y = 360 + i * 120 + shift * (1 if True else 0)
        a = e(tl, t0, t0 + 0.25) * (1 - 0.65 * e(tl, 2.8, 3.4))
        T(d, (960, y), w_, 78, OFFWHITE, a, font=FDB, spacing=4)
        k = e(tl, t0 + 0.3, t0 + 0.55)
        if k > 0:
            ww = tw(d, w_, 78, FDB) + 4 * len(w_) + 30
            line(d, [(960 - ww / 2, y), (960 - ww / 2 + ww * k, y)], RED, 7, a + 0.3)
    a = e(tl, 3.0, 3.6)
    if a > 0:
        sx, sy, s = 960, 800, 34
        poly(d, SHIP, sx, sy, s, STEEL, a, 70); poly(d, SHIP_SUP, sx, sy, s, STEEL, a, 70)
        line(d, [(sx - 1 * s, sy - 2.1 * s), (sx - 1 * s, sy - 6 * s)], STEEL, 3, a)
        line(d, [(sx + 5 * s, sy - 2.15 * s), (sx + 5 * s, sy - 5.2 * s)], STEEL, 3, a)
        waves(d, sy + 6, tl, a)
        k = e(tl, 3.5, 4.2)
        px0, px1 = sx - 10.2 * s, sx - 8.7 * s
        d.rectangle([px0 * SS, (sy - 4.6 * s) * SS, px1 * SS, (sy - 4.2 * s) * SS], fill=AMBER + (int(255 * k),))
        circle(d, ((px0 + px1) / 2, sy - 4.4 * s), 40 + 30 * math.sin(tl * 5), AMBER, w=3, a=0.6 * k)
        T(d, ((px0 + px1) / 2 + 30, sy - 5.6 * s), "JUST A SMALL PLATFORM", 36, AMBER, k, anchor="lm", font=FDB)
    return img


def sc_ship_vertical(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    sx, sy, s = 1060, 860, 40
    poly(d, SHIP, sx, sy, s, STEEL, 1, 70); poly(d, SHIP_SUP, sx, sy, s, STEEL, 1, 70)
    waves(d, sy + 6, tl, 1)
    pad_x = sx - 9.4 * s; pad_y = sy - 4.4 * s
    d.rectangle([(pad_x - 34) * SS, (pad_y - 6) * SS, (pad_x + 34) * SS, (pad_y + 4) * SS], fill=AMBER + (255,))
    # pogo goes up then down
    sc = 9; base = pad_y - (17 + 0.4 + 0.55) * sc
    up = e(tl, 0.8, 3.0) * (1 - e(tl, 3.8, 6.4))
    cy = base - 380 * up
    lay = layer(); pogo(lay, 90, pad_x, cy, sc, spin=tl * 5); fglow(img, lay, 8, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    if 0.8 < tl < 3.6:
        arrow(d, (pad_x + 140, base + 40), (pad_x + 140, base - 300), STEEL, 5, 20, e(tl, 0.8, 1.2))
        T(d, (pad_x + 180, base - 200), "TAKE OFF STRAIGHT UP", 38, STEEL, e(tl, 0.9, 1.3), anchor="lm")
    if tl > 3.6:
        arrow(d, (pad_x + 140, base - 300), (pad_x + 140, base + 40), AMBER, 5, 20, e(tl, 3.6, 4.0))
        T(d, (pad_x + 180, base - 160), "LAND STRAIGHT BACK DOWN", 38, AMBER, e(tl, 3.7, 4.1), anchor="lm")
    heading(d, "THE NAVY'S REQUIREMENT", e(tl, 0, 0.4), col=DIM, size=30)
    return img


def sc_catch(tl, D):
    """Takes off pointing at the sky -> lands pointing at the sky -> pilot at the top -> ground behind him."""
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    cx, sc = 1120, 20; cy = gfx.stand_cy(GROUND, sc)
    ground(d)
    lay = layer(); pogo(lay, 90, cx, cy, sc, spin=tl * 3); fglow(img, lay, 8, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    nx, ny = P((36.5, 0), 90, cx, cy, sc)
    a1 = e(tl, 0.1, 0.6) * (1 - 0.7 * e(tl, 5.2, 5.8))
    arrow(d, (nx, ny - 20), (nx, ny - 20 - 150 * e(tl, 0.1, 0.8)), STEEL, 5, 20, a1)
    T(d, (nx + 40, ny - 110), "TAKES OFF POINTING AT THE SKY", 34, STEEL, a1, anchor="lm")
    a2 = e(tl, 2.4, 2.9) * (1 - 0.7 * e(tl, 5.2, 5.8))
    T(d, (nx + 40, ny - 60), "LANDS POINTING AT THE SKY", 34, AMBER, a2, anchor="lm")
    if a2 > 0:
        tx, ty = P((-0.4, 0), 90, cx, cy, sc)
        for i in range(3):
            y = ty - 140 + i * 36 + (tl * 40) % 36
            arrow(d, (cx + 260, y), (cx + 260, y + 24), AMBER, 4, 12, a2 * 0.8)
    px, py = P(gfx.COCKPIT, 90, cx, cy, sc)
    k = min(1, max(0, (tl - 5.35) / 0.9))
    if k > 0:
        lay2 = layer(); gfx.callout(lay2, (px, py), (px - 260, py - 120), ["THE PILOT: AT THE VERY TOP"], AMBER, k, 32)
        img.paste(lay2, (0, 0), lay2); d = ImageDraw.Draw(img, "RGBA")
    k2 = e(tl, 8.5, 10.0)
    if k2 > 0:
        pts = [(px - 15 + (-430 - 15) * u - 0 * u, py + 30 + (GROUND - 40 - py) * (u ** 1.6)) for u in [i / 30 for i in range(31)]]
        pts = [(px - 20 - 460 * math.sin(u * math.pi / 2), py + 20 + (GROUND - 30 - py) * (u ** 1.8)) for u in [i / 40 for i in range(41)]]
        lay3 = layer(); d3 = ImageDraw.Draw(lay3)
        dashed(d3, pts, AMBER, 5, 1.0, k=k2); fglow(img, lay3, 8)
        d = ImageDraw.Draw(img, "RGBA")
        if k2 > 0.97:
            arrow(d, pts[-3], pts[-1], AMBER, 5, 20)
            T(d, (pts[-1][0] - 20, pts[-1][1] - 290), "THE GROUND:", 40, AMBER, e(tl, 10.0, 10.4), anchor="lm", font=FDB)
            T(d, (pts[-1][0] - 20, pts[-1][1] - 245), "BEHIND HIS BACK", 40, AMBER, e(tl, 10.0, 10.4), anchor="lm", font=FDB)
    return img


def sc_rear_cross(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    cx, cy, s = 960, 545, 30
    k = e(tl, 0.0, 1.2)
    hl = e(tl, 5.3, 5.8) * (0.75 + 0.25 * math.sin(tl * 6))
    lay = layer(); rear(lay, cx, cy, s, draw_k=max(0.02, k), wheel_hl=hl); fglow(img, lay, 9, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    a1 = e(tl, 1.2, 1.6) * (1 - e(tl, 2.9, 3.3))
    T(d, (960, 96), "SEEN FROM BEHIND: A CROSS", 40, AMBER, a1, spacing=3)
    a2 = e(tl, 3.1, 3.5)
    T(d, (960, 96), "NO CONVENTIONAL LANDING GEAR", 40, AMBER, a2, spacing=3)
    if hl > 0:
        T(d, (960, 1010), "JUST FOUR SMALL WHEELS — ON THE TIPS OF THE WINGS AND FINS", 32, OFFWHITE, e(tl, 5.5, 5.9), font=FSB)
    return img


def sc_engine(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    cx, cy, sc = 930, 560, 34
    lay = layer(); pogo(lay, 0, cx, cy, sc, spin=tl * 3, alpha=70); fglow(img, lay, 6, 0.5)
    d = ImageDraw.Draw(img, "RGBA")
    # X-ray internals: two turbine sections side by side (shown stacked), one gearbox, prop shaft
    lay2 = layer(); d2 = ImageDraw.Draw(lay2)
    a = e(tl, 0.2, 0.9); pulse = 0.75 + 0.25 * math.sin(tl * 5)
    for i, off in enumerate((0.75, -0.75)):
        ai = a * e(tl, 1.8 + 0.3 * i, 2.4 + 0.3 * i) if i else a
        x0, y0 = P((18.5, off + 0.55), 0, cx, cy, sc); x1, y1 = P((28.5, off - 0.55), 0, cx, cy, sc)
        d2.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=10 * SS, fill=AMBER + (int(110 * ai * pulse),), outline=AMBER + (int(255 * ai),), width=3 * SS)
        for k in range(6):
            xx = x0 + (x1 - x0) * (k + 1) / 7
            line(d2, [(xx, y0 + 6), (xx, y1 - 6)], AMBER, 2, ai * 0.6)
    ag = e(tl, 3.6, 4.2)
    gx0, gy0 = P((29.0, 1.35), 0, cx, cy, sc); gx1, gy1 = P((32.2, -1.35), 0, cx, cy, sc)
    d2.rounded_rectangle([gx0 * SS, gy0 * SS, gx1 * SS, gy1 * SS], radius=12 * SS, fill=RED + (int(120 * ag * pulse),), outline=RED + (int(255 * ag),), width=3 * SS)
    sx0, sy0 = P((32.2, 0), 0, cx, cy, sc); sx1, sy1 = P((34.6, 0), 0, cx, cy, sc)
    line(d2, [(sx0, sy0), (sx1, sy1)], AMBER, 6, ag)
    fglow(img, lay2, 10, 1.0); d = ImageDraw.Draw(img, "RGBA")
    ex, ey = P((23.5, 2.5), 0, cx, cy, sc)
    lay3 = layer()
    gfx.callout(lay3, (ex, ey - 30), (ex - 220, 250), ["ALLISON T40"], AMBER, min(1, tl / 1.0), 36)
    gfx.callout(lay3, P((23.5, -1.3), 0, cx, cy, sc), (ex - 120, 880), ["REALLY TWO TURBINE ENGINES"], AMBER, max(0, min(1, (tl - 2.0) / 0.9)), 30)
    gfx.callout(lay3, P((30.6, 1.35), 0, cx, cy, sc), (1050, 330), ["DRIVING ONE GEARBOX"], RED, max(0, min(1, (tl - 3.9) / 0.9)), 30)
    img.paste(lay3, (0, 0), lay3); d = ImageDraw.Draw(img, "RGBA")
    a4 = e(tl, 6.6, 7.2)
    T(d, (1500, 820), "≈ 5,850", 86, OFFWHITE, a4, font=FDB)
    T(d, (1500, 890), "HORSEPOWER", 30, AMBER, a4, font=FSB, spacing=6)
    return img


def sc_props_front(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    cx, cy, s = 960, 560, 46
    lay = layer(); rear(lay, cx, cy, s * 0.62, wheels=False, alpha=60, props=0); img.paste(lay, (0, 0), lay)
    lay = layer(); d2 = ImageDraw.Draw(lay)
    sp = tl * 0.9
    for i, (dirn, col) in enumerate(((1, AMBER), (-1, STEEL))):
        r = 8 * s * (1 - 0.05 * i)
        for b in range(3):
            a_ = sp * dirn * 2 * math.pi + b * 2 * math.pi / 3 + i * 0.6
            bl = [(cx + math.cos(a_ + o) * r * f, cy + math.sin(a_ + o) * r * f) for o, f in ((-0.09, 0.18), (-0.035, 1.0), (0.035, 1.0), (0.09, 0.18))]
            d2.polygon([(x * SS, y * SS) for x, y in bl], fill=col + (200,), outline=col + (255,))
    circle(d2, (cx, cy), 1.4 * s, OFFWHITE, fill=(60, 66, 74, 255), w=3)
    fglow(img, lay, 8, 0.8); d = ImageDraw.Draw(img, "RGBA")
    a = e(tl, 0.3, 0.8)
    arc_arrow(d, (cx, cy), 8 * s + 40, -60, -10, AMBER, 5, a)
    arc_arrow(d, (cx, cy), 8 * s + 40, 190, 240, STEEL, 5, a)
    T(d, (cx + 8 * s + 70, cy - 300), "CLOCKWISE", 30, AMBER, a, anchor="lm", font=FSB)
    T(d, (cx - 8 * s - 70, cy - 300), "ANTICLOCKWISE", 30, STEEL, a, anchor="rm", font=FSB)
    a2 = e(tl, 1.0, 1.6)
    line(d, [(cx - 8 * s, cy + 8 * s + 60), (cx + 8 * s, cy + 8 * s + 60)], OFFWHITE, 3, a2)
    for xx in (cx - 8 * s, cx + 8 * s): line(d, [(xx, cy + 8 * s + 46), (xx, cy + 8 * s + 74)], OFFWHITE, 3, a2)
    T(d, (cx, cy + 8 * s + 100), "16 FT  ·  ABOUT 5 M  ·  3 BLADES EACH", 30, OFFWHITE, a2, font=FSB, spacing=2)
    return img


def sc_thrust(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    sc = 14; land = gfx.stand_cy(GROUND, sc); cx = 1000
    ground(d)
    # vertical motion: hover, climb at 12.0, sink at 14.7, throttle wiggle 16.8+
    y = land - 160
    y -= 140 * e(tl, 12.1, 14.4) - 140 * e(tl, 14.8, 16.7)
    if tl > 16.9: y += 50 * math.sin((tl - 16.9) * 2.2)
    thrust = 1.0 + 0.45 * e(tl, 12.0, 12.6) - 0.75 * e(tl, 14.7, 15.2) + 0.3 * e(tl, 16.7, 17.2)
    if tl > 16.9: thrust += 0.28 * math.cos((tl - 16.9) * 2.2)
    lay = layer(); pogo(lay, 90, cx, y, sc, spin=tl * 5); fglow(img, lay, 8, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    nx, ny = P((36.5, 0), 90, cx, y, sc); tx, ty = P((-0.4, 0), 90, cx, y, sc)
    a = e(tl, 0.2, 0.8); L = 170
    arrow(d, (cx + 230, (ny + ty) / 2), (cx + 230, (ny + ty) / 2 - L * thrust), STEEL, 7, 26, a)
    T(d, (cx + 270, (ny + ty) / 2 - L * thrust + 10), "THRUST", 34, STEEL, a, anchor="lm", font=FDB)
    arrow(d, (cx - 230, (ny + ty) / 2), (cx - 230, (ny + ty) / 2 + L), AMBER, 7, 26, a)
    T(d, (cx - 270, (ny + ty) / 2 + L - 10), "WEIGHT", 34, AMBER, a, anchor="rm", font=FDB)
    aw = e(tl, 5.9, 6.4) * (1 - e(tl, 11.6, 12.0))
    T(d, (420, 300), "MAX TAKEOFF WEIGHT", 28, DIM, aw, anchor="mm", font=FSB, spacing=3)
    T(d, (420, 370), "≈ 16,000 LB", 64, OFFWHITE, aw, font=FDB)
    T(d, (420, 440), "OVER 7 TONNES", 34, AMBER, aw, font=FSB, spacing=2)
    T(d, (960, 110), "TO HOVER:  THRUST  >  WEIGHT", 42, OFFWHITE, e(tl, 0.6, 1.1) * (1 - e(tl, 11.6, 12.0)), spacing=2)
    T(d, (960, 110), "MORE THRUST THAN WEIGHT → IT CLIMBS", 42, STEEL, e(tl, 12.0, 12.4) * (1 - e(tl, 14.5, 14.8)), spacing=1)
    T(d, (960, 110), "LESS → IT SINKS", 42, AMBER, e(tl, 14.7, 15.1) * (1 - e(tl, 16.5, 16.8)), spacing=1)
    at = e(tl, 16.8, 17.3)
    if at > 0:
        T(d, (960, 110), "THE THROTTLE CONTROLS THE CLIMB AND THE SINK", 40, OFFWHITE, at, spacing=1)
        bx, by = 360, 600
        d.rounded_rectangle([(bx - 30) * SS, (by - 170) * SS, (bx + 30) * SS, (by + 170) * SS], radius=20 * SS, outline=DIM + (int(255 * at),), width=3 * SS)
        hy = by - 140 * (thrust - 1.0) / 0.5
        d.rounded_rectangle([(bx - 60) * SS, (hy - 18) * SS, (bx + 60) * SS, (hy + 18) * SS], radius=12 * SS, fill=AMBER + (int(255 * at),))
        T(d, (bx, by + 220), "THROTTLE", 26, AMBER, at, font=FSB, spacing=4)
    return img


def sc_torque(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    cx, cy, s = 960, 560, 26
    if tl < 9.1:
        roll = -40 * lin(tl, 1.2, 9.1) ** 1.6
        props = 1; dirs = (1,)
        col = mix(STEEL, RED, e(tl, 1.5, 3.0))
    elif tl < 16.7:
        roll = 0; props = 2; dirs = (1, -1); col = mix(STEEL, GREEN, e(tl, 11.2, 11.8))
    else:
        roll = -((tl - 16.7) ** 2) * 260; props = 1; dirs = (1,); col = RED
    lay = layer(); rear(lay, cx, cy, s, roll=roll, col=col, wheels=False, props=props, spin=tl * 1.5, prop_dirs=dirs + (0,))
    fglow(img, lay, 9, 0.8); d = ImageDraw.Draw(img, "RGBA")
    if tl < 9.1:
        a = e(tl, 0.2, 0.7)
        arc_arrow(d, (cx, cy), 8 * s + 50, -70, -20, AMBER, 6, a)
        T(d, (cx + 8 * s + 80, cy - 320), "PROPELLER SPINS THIS WAY", 30, AMBER, a, anchor="lm", font=FSB)
        a2 = e(tl, 1.8, 2.4)
        arc_arrow(d, (cx, cy), 8 * s + 50, 160, 110, RED, 6, a2)
        T(d, (cx - 8 * s - 80, cy + 320), "AIRFRAME TWISTS THE OTHER WAY", 30, RED, a2, anchor="rm", font=FSB)
        T(d, (960, 100), "NEWTON'S THIRD LAW", 52, OFFWHITE, e(tl, 7.2, 7.6), font=FDB, spacing=4)
        T(d, (960, 160), "EVERY ACTION HAS AN EQUAL AND OPPOSITE REACTION", 26, DIM, e(tl, 7.5, 8.0), font=FSB, spacing=2)
    elif tl < 16.7:
        a = e(tl, 9.2, 9.7)
        T(d, (960, 100), "SO THE POGO HAS TWO", 48, OFFWHITE, a * (1 - e(tl, 11.0, 11.3)), font=FDB, spacing=3)
        a2 = e(tl, 11.2, 11.6)
        arc_arrow(d, (cx, cy), 8 * s + 50, -70, -20, AMBER, 6, a2)
        arc_arrow(d, (cx, cy), 8 * s + 50, 250, 200, STEEL, 6, a2)
        T(d, (cx + 8 * s + 80, cy - 320), "CLOCKWISE", 30, AMBER, a2, anchor="lm", font=FSB)
        T(d, (cx - 8 * s - 80, cy - 320), "ANTICLOCKWISE", 30, STEEL, a2, anchor="rm", font=FSB)
        T(d, (960, 100), "THE TWIST CANCELS OUT", 48, GREEN, e(tl, 13.0, 13.5), font=FDB, spacing=3)
        stamp(d, (960, 1000), "STABLE", GREEN, e(tl, 13.6, 14.0), 36)
    else:
        T(d, (960, 100), "WITHOUT IT…", 52, RED, e(tl, 16.8, 17.2), font=FDB, spacing=4)
        T(d, (960, 1000), "…IT WOULD SPIN ON ITS TAIL LIKE A TOP", 36, OFFWHITE, e(tl, 17.6, 18.0), font=FSB)
    return img


def sc_seat(tl, D):
    """Cutaway of the upright cockpit: pilot on his back, seat tilts ~45 degrees toward the panel."""
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    # nose pointing up: draw a big vertical fuselage section
    lay = layer(); d2 = ImageDraw.Draw(lay)
    fx = 960
    body = [(fx - 230, 1080), (fx - 250, 520), (fx - 200, 260), (fx - 80, 90), (fx + 80, 90), (fx + 200, 260), (fx + 250, 520), (fx + 230, 1080)]
    d2.polygon([(x * SS, y * SS) for x, y in body], fill=STEEL + (45,), outline=STEEL + (255,), width=3 * SS)
    canopy = [(fx + 245, 640), (fx + 330, 600), (fx + 340, 420), (fx + 230, 330)]
    line(d2, canopy, STEEL, 3, 1)
    # instrument panel (toward the nose = up)
    d2.rounded_rectangle([(fx - 40) * SS, 330 * SS, (fx + 220) * SS, 356 * SS], radius=8 * SS, fill=AMBER + (200,))
    T(d2, (fx - 60, 343), "INSTRUMENT PANEL", 24, AMBER, 1, anchor="rm", font=FSB)
    # seat pivot + pilot. Level-flight seat frame: x = forward (toward the nose), y = up (toward the canopy).
    # Nose up: forward -> screen up, up -> screen right, so he lies on his back facing the sky.
    th = 45 * e(tl, 0.8, 2.6)
    piv = (fx - 60, 760)
    def R(pts):
        sp = [(piv[0] + y, piv[1] - x) for x, y in pts]
        return rot([(x - piv[0], y - piv[1]) for x, y in sp], -th, piv[0], piv[1], 1)
    seat = R([(0, -14), (150, -14), (150, 10), (0, 10)]); back = R([(-24, 0), (0, 0), (0, 250), (-24, 250)])
    d2.polygon([(x * SS, y * SS) for x, y in seat], fill=DIM + (210,)); d2.polygon([(x * SS, y * SS) for x, y in back], fill=DIM + (210,))
    head = R([(40, 290)])[0]; circle(d2, head, 40, OFFWHITE, fill=(80, 88, 98, 255), w=3)
    line(d2, R([(30, 245), (30, 40)]), OFFWHITE, 18, 1)
    line(d2, R([(30, 40), (170, 60), (230, -40)]), OFFWHITE, 15, 1)
    line(d2, R([(30, 200), (130, 170), (190, 200)]), OFFWHITE, 11, 1)
    eye = R([(60, 300)])[0]; look = R([(260, 300)])[0]
    dashed(d2, [eye, look], STEEL, 3, 0.8)
    fglow(img, lay, 6, 0.6); d = ImageDraw.Draw(img, "RGBA")
    a = e(tl, 0.8, 1.2)
    arc_arrow(d, piv, 340, -5, -5 - 45 * e(tl, 0.8, 2.6) - 0.01, AMBER, 5, a)
    T(d, (430, 560), "SEAT TILTS", 40, AMBER, a, font=FDB)
    T(d, (430, 615), "ABOUT 45°", 52, OFFWHITE, a, font=FDB)
    T(d, (430, 670), "TOWARD THE PANEL", 26, AMBER, a, font=FSB, spacing=2)
    T(d, (1500, 900), "THE GROUND:", 30, RED, e(tl, 3.0, 3.4), font=FSB, spacing=2)
    T(d, (1500, 945), "STILL BEHIND HIM", 30, RED, e(tl, 3.0, 3.4), font=FSB, spacing=2)
    arrow(d, (1500, 980), (1500, 1060), RED, 4, 16, e(tl, 3.0, 3.4))
    return img


def sc_transition(tl, D):
    """Vertical climb -> pushes the nose over -> level flight."""
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    k = e(tl, 0.0, D - 0.3)
    ang = 90 - 90 * k
    cx = 500 + 900 * k; cy = 700 - 300 * math.sin(k * math.pi / 2)
    pts = [(500 + 900 * u, 700 - 300 * math.sin(u * math.pi / 2)) for u in [i / 40 * k for i in range(41)]]
    dashed(d, pts, STEEL, 3, 0.8)
    lay = layer(); pogo(lay, ang, cx, cy, 12, spin=tl * 6); fglow(img, lay, 8, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    T(d, (960, 110), "NOSE OVER → FLIES LIKE A NORMAL PLANE", 40, OFFWHITE, e(tl, 0.2, 0.6), spacing=1)
    return img


STEPS = ["LEVEL FLIGHT", "SLOW DOWN", "NOSE UP", "HANG ON THE PROPELLERS"]
def sc_pitch(cues=(0.0, 0.3, 1.9, 5.3)):
    def f(tl, D):
        img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
        rot_ = 90 * e(tl, cues[2], cues[3])
        cx = 860 + 100 * e(tl, 0, cues[3]); cy = 540
        lay = layer(); pogo(lay, rot_, cx, cy, 15, spin=tl * 4); fglow(img, lay, 9, 0.9)
        d = ImageDraw.Draw(img, "RGBA")
        step = sum(1 for c in cues if tl >= c) - 1
        s = STEPS[max(0, step)]
        T(d, (960, 110), s, 46, AMBER if step else STEEL, 1.0, spacing=3)
        for k in range(4):
            x = 960 - 1.5 * 36 + k * 36
            circle(d, (x, 168), 7, fill=(AMBER + (255,)) if k <= step else (GREY + (130,)), w=1)
        if 0.3 < tl < cues[2] + 0.5:
            for i in range(3):
                xx = cx - 420 - i * 60 - (tl * 160) % 60
                line(d, [(xx, cy), (xx + 36, cy)], STEEL, 3, 0.6)
        return img
    return f


def sc_altimeter(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    s = 24; cx = 820; cy = rear_ground_cy(GROUND, s) - 120
    ground(d)
    hl = e(tl, 0.3, 0.9) * (0.7 + 0.3 * math.sin(tl * 7))
    lay = layer(); rear(lay, cx, cy, s, pod_hl=hl, props=0); fglow(img, lay, 9, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    pod = (cx - R_SPAN * s, cy)
    for i in range(4):
        ph = ((tl * 0.9 + i / 4) % 1.0)
        yy = pod[1] + 30 + ph * (GROUND - pod[1] - 30)
        w_ = 30 + ph * 110
        a = (1 - ph) * e(tl, 0.6, 1.0)
        d.arc([(pod[0] - w_) * SS, (yy - 18) * SS, (pod[0] + w_) * SS, (yy + 18) * SS], 20, 160, fill=AMBER + (int(255 * a),), width=3 * SS)
    lay2 = layer(); gfx.callout(lay2, pod, (pod[0] - 40, 230), ["RADAR ALTIMETER", "IN THE WINGTIP"], AMBER, min(1, tl / 1.0), 30)
    img.paste(lay2, (0, 0), lay2); d = ImageDraw.Draw(img, "RGBA")
    # three warning lights (no colours claimed: neutral white)
    ap = e(tl, 1.6, 2.2); dim = 1 - 0.75 * e(tl, 5.5, 6.0)
    bx, by = 1500, 520
    d.rounded_rectangle([(bx - 170) * SS, (by - 110) * SS, (bx + 170) * SS, (by + 110) * SS], radius=18 * SS, fill=(18, 20, 24, int(230 * ap)), outline=DIM + (int(255 * ap),), width=3 * SS)
    for i in range(3):
        on = ap * dim * (0.55 + 0.45 * (math.sin(tl * 4 - i * 1.3) > 0))
        circle(d, (bx - 100 + i * 100, by - 10), 32, DIM, fill=(255, 250, 235, int(255 * on)), w=3, a=ap)
    T(d, (bx, by + 160), "3 WARNING LIGHTS", 32, OFFWHITE, ap, font=FDB, spacing=2)
    T(d, (960, 1000), "BUT THE LIGHTS COULDN'T DO THE LANDING FOR HIM", 34, RED, e(tl, 5.6, 6.0), font=FSB)
    return img


def sc_rear_danger(tl, D):
    """Too fast -> narrow stance & drift -> gusts on the big wing and fins (rear view)."""
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    s = 22; land = rear_ground_cy(GROUND, s); cx = 960
    ground(d)
    roll = 0; col = STEEL; hl = 0
    if tl < 5.4:
        k = lin(tl, 0.3, 1.6) ** 2; cy = 320 + (land - 320) * k
        if tl > 1.6: roll = 8 * math.exp(-(tl - 1.6) * 3) * math.sin((tl - 1.6) * 14); col = RED
        title, tcol = "TOO FAST: THE IMPACT CAN DAMAGE IT, OR TIP IT OVER", RED
    elif tl < 9.7:
        t2 = tl - 5.4; cy = land - 70; cx = 960 + 150 * math.sin(t2 * 1.3); roll = 6 * math.sin(t2 * 1.3 + 0.6)
        hl = e(t2, 0.8, 1.3); title, tcol = "DRIFT SIDEWAYS: A NARROW STANCE, LITTLE ROOM FOR ERROR", AMBER
    else:
        t2 = tl - 9.7; cy = land - 70; g = math.sin(t2 * 2.3) * 0.6 + math.sin(t2 * 5.1) * 0.4
        roll = 9 * g; cx = 960 + 40 * g; title, tcol = "AND ANY GUST PUSHES ON THAT BIG WING AND THOSE TALL FINS", STEEL
    lay = layer(); rear(lay, cx, cy, s, roll=roll, col=col, wheel_hl=hl, props=1, spin=tl * 2); fglow(img, lay, 9, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    T(d, (960, 100), title, 34, tcol, 1.0, font=FSB, spacing=1)
    if tl >= 5.4 and tl < 9.7:
        y = GROUND + 50; x0 = cx - 1.0 * s * 0 - 40; x1 = cx + 40
        line(d, [(cx - 60, y), (cx + 60, y)], AMBER, 3, hl); T(d, (cx, y + 36), "WHEEL STANCE", 24, AMBER, hl, font=FSB, spacing=2)
    if tl >= 9.7:
        for i in range(6):
            yy = 260 + i * 110; ph = (tl * 1.4 + i * 0.37) % 1.0
            x0 = 120 + ph * 500; a = math.sin(ph * math.pi) * e(tl, 9.8, 10.3)
            arrow(d, (x0, yy), (x0 + 150, yy), STEEL, 4, 16, a)
        T(d, (240, 980), "GUSTS", 30, STEEL, e(tl, 10.0, 10.4), font=FDB, spacing=6)
    if tl < 5.4 and tl > 1.6:
        fl = math.exp(-(tl - 1.6) * 3)
        circle(d, (cx, GROUND), 60 + 260 * (1 - fl), RED, w=4, a=fl)
    return img


def sc_four_cars(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    lay = layer(); pogo(lay, 0, 520, 520, 13, spin=tl * 2, alpha=110); fglow(img, lay, 8, 0.7)
    d = ImageDraw.Draw(img, "RGBA")
    T(d, (520, 700), "XFY-1 POGO", 34, OFFWHITE, e(tl, 0.1, 0.5), font=FDB, spacing=3)
    T(d, (960, 520), "=", 90, AMBER, e(tl, 0.4, 0.8), font=FDB)
    for i in range(4):
        a = e(tl, 0.6 + i * 0.28, 0.9 + i * 0.28)
        x = 1180 + (i % 2) * 330; y = 470 + (i // 2) * 150
        poly(d, CAR, x, y, 60, STEEL, a, 80)
        circle(d, (x - 1.35 * 60, y), 20, STEEL, fill=(30, 34, 40, 255), w=3, a=a); circle(d, (x + 1.35 * 60, y), 20, STEEL, fill=(30, 34, 40, 255), w=3, a=a)
    T(d, (1345, 700), "4 CARS", 40, AMBER, e(tl, 1.8, 2.2), font=FDB, spacing=3)
    T(d, (960, 110), "AS HEAVY AS FOUR CARS — LANDED BACKWARDS, BY EYE", 36, OFFWHITE, e(tl, 0.2, 0.6), font=FSB, spacing=1)
    return img


def sc_full_cycle(tl, D):
    img = bg("grid"); d = ImageDraw.Draw(img, "RGBA")
    ground(d)
    # path: up from A, arc over to level, cruise, pull up to vertical, slide back down at B
    Ax, Bx, top = 360, 1560, 300
    path = []
    for u in [i / 30 for i in range(31)]: path.append((Ax, GROUND - 40 - (GROUND - 40 - 520) * u, 90))
    for u in [i / 30 for i in range(1, 31)]:
        a = u * math.pi / 2; path.append((Ax + 200 * (1 - math.cos(a)), 520 - 220 * math.sin(a), 90 - 90 * u))
    for u in [i / 30 for i in range(1, 31)]: path.append((Ax + 200 + (Bx - Ax - 400) * u, top, 0))
    for u in [i / 30 for i in range(1, 31)]:
        a = u * math.pi / 2; path.append((Bx - 200 + 200 * math.sin(a), top + 220 * (1 - math.cos(a)), 90 * u))
    for u in [i / 30 for i in range(1, 31)]: path.append((Bx, 520 + (GROUND - 40 - 520) * u, 90))
    k = e(tl, 0.1, 6.8); n = max(2, int(k * (len(path) - 1)) + 1)
    lay = layer(); d2 = ImageDraw.Draw(lay)
    dashed(d2, [(x, y) for x, y, _ in path[:n]], AMBER, 4, 1.0)
    x, y, ang = path[n - 1]
    fglow(img, lay, 8, 0.9)
    lay = layer(); pogo(lay, ang, x, y, 6, spin=tl * 6); fglow(img, lay, 6, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    labels = [(0.2, (Ax - 30, 700), "STRAIGHT UP", "rm"), (1.9, (700, top - 60), "OVER INTO LEVEL FLIGHT", "mm"),
              (3.9, (Bx + 40, 420), "BACK UP TO VERTICAL", "lm"), (5.4, (Bx + 40, 720), "DOWN, BACKWARDS,", "lm"), (5.4, (Bx + 40, 765), "ONTO ITS TAIL", "lm")]
    for t0, xy, s, anc in labels: T(d, xy, s, 32, OFFWHITE, e(tl, t0, t0 + 0.4), anchor=anc, font=FDB)
    T(d, (960, 100), "2 NOVEMBER 1954 · THE FULL CYCLE", 40, AMBER, e(tl, 0, 0.4), spacing=3)
    stamp(d, (960, 560), "FIRST EVER", AMBER, e(tl, 7.0, 7.3), 46)
    return img
