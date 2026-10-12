"""Builds Hangar Physics: Convair XFY-1 Pogo, Parts 1 + 2 (picture), timed to the ElevenLabs voiceover.
Usage: python3 build12.py OUTDIR [chunk_index n_chunks]   (renders frames of that chunk to OUTDIR/v_<i>.mp4)
       python3 build12.py OUTDIR --still T                (one frame at global time T -> OUTDIR/still_T.png)
       python3 build12.py OUTDIR --cues                   (writes cues.json for the audio build)"""
import sys, os, math, json, subprocess, bisect
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import gfx, gfx2
from gfx import SS, W, H, FPS, AMBER, STEEL, OFFWHITE, RED, GREEN, GREY, ease
from gfx2 import T, F, FD, FDB, FSB, FM, FMONO, DIM, e, lin, line, dashed, arrow, circle, layer, fglow, stamp, mix

HERE = os.path.dirname(os.path.abspath(__file__))
SHOT = lambda n: os.path.join(HERE, "footage", "shots", n)
PH = lambda n: os.path.join(HERE, "photos", "cleared", n)

# ---------------------------------------------------------------- voiceover timing
VO_A_OFF, VO_A_END = 1.5, 43.4        # part 1 [0, 43.4) starts at 1.5 s
TITLE_GAP = 3.0
VO_B_OFF = VO_A_OFF + TITLE_GAP       # part 1 [43.4, end) after the title card
P1_LEN, P2_LEN = 217.6, 163.1
VO_C_OFF = VO_B_OFF + P1_LEN + 1.5    # part 2
END = VO_C_OFF + P2_LEN + 4.0
def g1(t): return t + (VO_A_OFF if t < VO_A_END else VO_B_OFF)
def g2(t): return t + VO_C_OFF

# ---------------------------------------------------------------- finishing
_yy, _xx = np.mgrid[0:H, 0:W]
_VIG = (1 - 0.22 * (((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) ** 1.5).clip(0.68, 1).astype(np.float32)[..., None]
_rng = np.random.default_rng(7)
_GRAIN = [_rng.integers(-7, 8, (H, W, 1), dtype=np.int16) for _ in range(12)]

def finish(im1, fi, grain=1.0):
    a = np.asarray(im1, dtype=np.float32) * _VIG
    if grain: a = a + _GRAIN[fi % 12] * grain
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def down(img_ss): return img_ss.convert("RGB").resize((W, H), Image.LANCZOS)

def comp_overlay(base1, lay_ss):
    ov = lay_ss.resize((W, H), Image.LANCZOS)
    base1 = base1.convert("RGB"); base1.paste(ov, (0, 0), ov); return base1

# ---------------------------------------------------------------- overlays (drawn at SS on an RGBA layer)
def lower_third(title, sub=None, t_in=0.25, t_out=None):
    def f(d, tl, D, Pmap):
        a = e(tl, t_in, t_in + 0.45) * (1 - e(tl, (t_out or D) - 0.35, (t_out or D)))
        if a <= 0: return
        sl = (1 - e(tl, t_in, t_in + 0.6)) * 30
        wb = max(gfx2.tw(d, title, 34, FDB) + 2 * len(title), gfx2.tw(d, sub or "", 22, FSB) + 2 * len(sub or "")) + 70
        d.rounded_rectangle([70 * SS, 896 * SS, (118 + wb) * SS, (912 + (100 if sub else 66)) * SS], radius=10 * SS, fill=(8, 10, 13, int(150 * a)))
        d.rectangle([92 * SS, 912 * SS, 98 * SS, (912 + (86 if sub else 52) * e(tl, t_in, t_in + 0.4)) * SS], fill=AMBER + (int(255 * a),))
        T(d, (118 - sl, 948), title, 34, OFFWHITE, a, anchor="ls", font=FDB, spacing=2)
        if sub: T(d, (118 - sl, 990), sub, 22, (190, 196, 204), a, anchor="ls", font=FSB, spacing=2)
    return f

def source_tag(s):
    def f(d, tl, D, Pmap):
        a = 0.62 * e(tl, 0.2, 0.7) * (1 - e(tl, D - 0.3, D))
        T(d, (1832, 1036), s, 17, OFFWHITE, a, anchor="rs", font=FSB, spacing=2)
    return f

def typewriter(text, sub=None, xy=(110, 150), t0=0.2, size=50):
    def f(d, tl, D, Pmap):
        n = min(len(text), int(max(0, tl - t0) / 0.09))
        if tl < t0: return
        a = 1 - e(tl, D - 0.35, D)
        cur = "_" if (n < len(text) or int(tl * 2.6) % 2 == 0) else ""
        tw_ = gfx2.tw(d, text[:n] + "_", size, FMONO)
        d.rectangle([(xy[0] - 18) * SS, (xy[1] - size * 0.85) * SS, (xy[0] + tw_ + 18) * SS, (xy[1] + size * 0.45) * SS], fill=(8, 9, 11, int(170 * a)))
        T(d, xy, text[:n] + cur, size, AMBER, a, anchor="ls", font=FMONO)
        if sub:
            ta = t0 + len(text) * 0.09; a2 = a * e(tl, ta, ta + 0.5)
            sw = gfx2.tw(d, sub, 26, FSB) + 3 * len(sub)
            d.rectangle([(xy[0] - 18) * SS, (xy[1] + 22) * SS, (xy[0] + sw + 18) * SS, (xy[1] + 64) * SS], fill=(8, 9, 11, int(170 * a2)))
            T(d, (xy[0], xy[1] + 52), sub, 26, OFFWHITE, a2, anchor="ls", font=FSB, spacing=3)
    return f

def big_question(s1, s2=None, t0=0.2):
    def f(d, tl, D, Pmap):
        a = e(tl, t0, t0 + 0.5) * (1 - e(tl, D - 0.3, D))
        d.rectangle([0, 400 * SS, W * SS, 700 * SS], fill=(8, 10, 13, int(120 * a)))
        T(d, (960, 510), s1, 60, OFFWHITE, a, font=FDB, spacing=2)
        if s2: T(d, (960, 590), s2, 60, AMBER, a * e(tl, t0 + 0.3, t0 + 0.8), font=FDB, spacing=2)
    return f

def callouts(items):
    """items: (t0, (nx, ny) image point, (lx, ly) screen label pos, [lines], color)"""
    def f(d, tl, D, Pmap, lay=None):
        for it in items:
            t0, pt, lab, lines, col = it[:5]; t1 = it[5] if len(it) > 5 else 99
            k = (tl - t0) / 0.9
            if k <= 0 or tl > t1: continue
            k *= (1 - e(tl, D - 0.3, D)) * (1 - e(tl, t1 - 0.25, t1))
            ax = Pmap(*pt)[0]; right = lab[0] >= ax
            wmax = max(gfx2.tw(d, l_, 30) for l_ in lines) + 30
            x0 = lab[0] + (0 if right else -wmax - 14); y0 = lab[1] - 44
            d.rounded_rectangle([x0 * SS, y0 * SS, (x0 + wmax + 14) * SS, (y0 + 30 + 38 * len(lines)) * SS], radius=10 * SS, fill=(10, 12, 15, int(200 * min(1, max(0, (k - 0.5) * 2)))))
            gfx.callout(f.lay, Pmap(*pt), lab, lines, col, min(1, k), 30)
    f.needs_layer = True
    return f

def highlight_boxes(items):
    """items: (t0, (x0,y0,x1,y1) image-normalised)"""
    def f(d, tl, D, Pmap):
        for t0, (x0, y0, x1, y1) in items:
            k = e(tl, t0, t0 + 0.6)
            if k <= 0: continue
            a = 1 - e(tl, D - 0.3, D)
            p0 = Pmap(x0, y0); p1 = Pmap(x1, y1)
            d.rectangle([p0[0] * SS, p0[1] * SS, (p0[0] + (p1[0] - p0[0]) * k) * SS, p1[1] * SS], fill=AMBER + (int(80 * a),))
            d.rectangle([p0[0] * SS, (p1[1] + 2) * SS, (p0[0] + (p1[0] - p0[0]) * k) * SS, (p1[1] + 6) * SS], fill=AMBER + (int(255 * a),))
    return f

def red_stamp(s, t0, xy=(1460, 860)):
    def f(d, tl, D, Pmap):
        stamp(d, xy, s, RED, e(tl, t0, t0 + 0.2) * (1 - e(tl, D - 0.3, D)), 40)
    return f

def text_lines(items, size=40):
    """items: (t0, (x,y), text, color, anchor)"""
    def f(d, tl, D, Pmap):
        for t0, xy, s, col, anc in items:
            a = e(tl, t0, t0 + 0.4) * (1 - e(tl, D - 0.3, D))
            w_ = gfx2.tw(d, s, size, FDB) + 2 * len(s)
            x0 = xy[0] - w_ / 2 if anc[0] == "m" else (xy[0] if anc[0] == "l" else xy[0] - w_)
            d.rounded_rectangle([(x0 - 26) * SS, (xy[1] - size * 0.85) * SS, (x0 + w_ + 26) * SS, (xy[1] + size * 0.85) * SS], radius=12 * SS, fill=(8, 10, 13, int(160 * a)))
            T(d, xy, s, size, col, a, anchor=anc, font=FDB, spacing=2)
    return f

def dark_band(y0=0, y1=1080, a_=0.5):
    def f(d, tl, D, Pmap):
        d.rectangle([0, y0 * SS, W * SS, y1 * SS], fill=(8, 10, 13, int(255 * a_)))
    return f

def trophy(t0=0.3):
    def f(d, tl, D, Pmap):
        a = e(tl, t0, t0 + 0.5) * (1 - e(tl, D - 0.3, D))
        if a <= 0: return
        cx, cy = 1640, 470
        cup = [(cx - 90, cy - 120), (cx + 90, cy - 120), (cx + 70, cy - 20), (cx + 25, cy + 30), (cx + 25, cy + 80), (cx + 70, cy + 110), (cx - 70, cy + 110), (cx - 25, cy + 80), (cx - 25, cy + 30), (cx - 70, cy - 20)]
        d.polygon([(x * SS, y * SS) for x, y in cup], fill=AMBER + (int(230 * a),))
        for sx in (-1, 1):
            d.arc([(cx + sx * 90 - 45) * SS, (cy - 110) * SS, (cx + sx * 90 + 45) * SS, (cy - 30) * SS], 270 if sx > 0 else 90, 90 if sx > 0 else 270, fill=AMBER + (int(230 * a),), width=10 * SS)
        d.rectangle([(cx - 110) * SS, (cy + 110) * SS, (cx + 110) * SS, (cy + 140) * SS], fill=AMBER + (int(230 * a),))
        T(d, (cx, cy + 210), "HARMON TROPHY", 50, OFFWHITE, a, font=FDB, spacing=4)
        T(d, (cx, cy + 262), "ONE OF AVIATION'S HIGHEST AWARDS", 24, AMBER, a, font=FSB, spacing=2)
    return f

# ---------------------------------------------------------------- shot types
def keyinterp(keys, tl):
    """keys: [(t, z, cx, cy), ...] -> eased interpolation."""
    if tl <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if tl <= t1:
            k = ease((tl - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(x + (y - x) * k for x, y in zip(a, b))
    return keys[-1][1:]

_PHOTOS = {}
def load_photo(path, bw, crop):
    key = (path, bw, crop)
    if key not in _PHOTOS:
        im = Image.open(path).convert("RGB")
        if crop:
            w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        if bw:
            g = ImageOps.autocontrast(im.convert("L"), cutoff=0.5)
            im = Image.merge("RGB", [g.point(lambda v: min(255, int(v * 1.02 + 4))), g, g.point(lambda v: int(v * 0.96))])
        _PHOTOS[key] = im
    return _PHOTOS[key]

class Shot:
    xin = 0.0
    def __init__(self, overlays=(), xin=0.0, tint=0.0, grain=1.0):
        self.overlays = list(overlays); self.xin = xin; self.tint = tint; self.grain = grain
    def apply_overlays(self, base1, tl, D, Pmap):
        if not self.overlays: return base1
        lay = layer(); d = ImageDraw.Draw(lay, "RGBA")
        for o in self.overlays:
            if getattr(o, "needs_layer", False):
                o.lay = lay; o(d, tl, D, Pmap); d = ImageDraw.Draw(lay, "RGBA")
            else: o(d, tl, D, Pmap)
        return comp_overlay(base1, lay)
    def close(self): pass

class Photo(Shot):
    def __init__(self, path, keys, mode="cover", bw=False, crop=None, **kw):
        super().__init__(**kw); self.path, self.keys, self.mode, self.bw, self.crop = path, keys, mode, bw, crop
        self._bg = None
    def render(self, tl, D, fi):
        im = load_photo(self.path, self.bw, self.crop); iw, ih = im.size
        z, cx, cy = keyinterp(self.keys, tl)
        if self.mode == "cover":
            s = max(W / iw, H / ih) * z
            vw, vh = W / s, H / s
            x0 = min(max(cx * iw - vw / 2, 0), iw - vw); y0 = min(max(cy * ih - vh / 2, 0), ih - vh)
            out = im.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC)
            Pmap = lambda nx, ny: ((nx * iw - x0) * s, (ny * ih - y0) * s)
        else:
            if self._bg is None:
                s0 = max(W / iw, H / ih) * 1.1
                b = im.transform((W, H), Image.AFFINE, (1 / s0, 0, (iw - W / s0) / 2, 0, 1 / s0, (ih - H / s0) / 2), resample=Image.BILINEAR)
                b = b.filter(ImageFilter.GaussianBlur(28))
                self._bg = Image.blend(b, Image.new("RGB", (W, H), (12, 14, 18)), 0.62)
            s = min(940 / ih, 1600 / iw) * z
            x0 = cx * iw - (W / 2) / s; y0 = cy * ih - (H / 2) / s
            rgba = im.convert("RGBA")
            fg = rgba.transform((W, H), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0), resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
            out = self._bg.copy()
            # shadow + border from the card's screen rectangle
            rx0, ry0 = (0 - x0) * s, (0 - y0) * s; rx1, ry1 = (iw - x0) * s, (ih - y0) * s
            sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([rx0 + 14, ry0 + 18, rx1 + 14, ry1 + 18], fill=170)
            out.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
            out.paste(fg, (0, 0), fg)
            ImageDraw.Draw(out).rectangle([rx0 - 1, ry0 - 1, rx1 + 1, ry1 + 1], outline=(235, 232, 225), width=3)
            Pmap = lambda nx, ny: ((nx * iw - x0) * s, (ny * ih - y0) * s)
        if self.tint: out = Image.blend(out, Image.new("RGB", (W, H), (10, 12, 16)), self.tint)
        return self.apply_overlays(out, tl, D, Pmap)

class Film(Shot):
    """mode 'fill': crop to 16:9 and fill; 'framed': 4:3 picture at 1200x900 over a blurred copy of itself."""
    def __init__(self, name, src_in=0.0, speed=1.0, mode="fill", crop_y=0.5, keys=((0, 1.0, .5, .5),),
                 freeze=None, sar=None, bw=True, contrast=1.08, **kw):
        super().__init__(**kw)
        self.name, self.src_in, self.speed, self.mode, self.crop_y, self.keys = name, src_in, speed, mode, crop_y, keys
        self.freeze, self.bw, self.contrast = freeze, bw, contrast
        self.p = None; self.n = -1; self.last = None; self.t_open = None
    def _open(self, tl):
        path = SHOT(self.name)
        w, h = [int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip().split(",")[:2]]
        pre = "scale=654:480," if (w, h) == (720, 480) else ""
        if self.mode == "fill":
            vf = f"{pre}crop=iw:iw*9/16:0:(ih-iw*9/16)*{self.crop_y},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5"
            self.size = (W, H)
        else:
            vf = f"{pre}scale=1200:900:flags=lanczos,unsharp=5:5:0.4"
            self.size = (1200, 900)
        grade = f"eq=contrast={self.contrast}:brightness=-0.015" + (":saturation=0" if self.bw else ":saturation=0.85")
        start = self.src_in + tl * self.speed
        vf = f"setpts=(PTS-STARTPTS)/{self.speed},fps={FPS},{vf},{grade},format=rgb24"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-vf", vf, "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.n = -1; self.t_open = tl; self.last = None
    def frame(self, tl):
        if self.freeze is not None: tl = min(tl, self.freeze)
        if self.p is None or tl < (self.t_open or 0) - 1e-6: self._open(tl)
        want = int(round((tl - self.t_open) * FPS))
        nb = self.size[0] * self.size[1] * 3
        while self.n < want:
            buf = self.p.stdout.read(nb)
            if len(buf) < nb: break
            self.last = Image.frombytes("RGB", self.size, buf); self.n += 1
        if self.last is None: self.last = Image.new("RGB", self.size, (0, 0, 0))
        return self.last
    def render(self, tl, D, fi):
        fr = self.frame(tl)
        z, cx, cy = keyinterp(self.keys, tl)
        if self.mode == "fill":
            vw, vh = W / z, H / z
            x0 = min(max(cx * W - vw / 2, 0), W - vw); y0 = min(max(cy * H - vh / 2, 0), H - vh)
            out = fr.transform((W, H), Image.AFFINE, (1 / z, 0, x0, 0, 1 / z, y0), resample=Image.BICUBIC) if z != 1.0 else fr.copy()
            Pmap = lambda nx, ny: ((nx * W - x0) * z, (ny * H - y0) * z)
        else:
            bgim = fr.resize((W, int(W * 0.75)), Image.BILINEAR).crop((0, (int(W * .75) - H) // 2, W, (int(W * .75) - H) // 2 + H)).filter(ImageFilter.GaussianBlur(24))
            out = Image.blend(bgim, Image.new("RGB", (W, H), (10, 12, 15)), 0.6)
            fw, fh = int(1200 * z), int(900 * z)
            pic = fr.resize((fw, fh), Image.BICUBIC) if z != 1 else fr
            ox, oy = (W - fw) // 2, (H - fh) // 2
            sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rectangle([ox + 14, oy + 18, ox + fw + 14, oy + fh + 18], fill=170)
            out.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
            pic_c = pic.crop((max(0, -ox), max(0, -oy), max(0, -ox) + min(fw, W), max(0, -oy) + min(fh, H)))
            out.paste(pic_c, (max(0, ox), max(0, oy)))
            Pmap = lambda nx, ny: (ox + nx * fw, oy + ny * fh)
        if self.tint: out = Image.blend(out, Image.new("RGB", (W, H), (10, 12, 16)), self.tint)
        if self.freeze is not None and self.freeze <= tl < self.freeze + 0.1:
            out = Image.blend(out, Image.new("RGB", (W, H), (255, 255, 255)), 0.4)
        return self.apply_overlays(out, tl, D, Pmap)
    def close(self):
        if self.p: self.p.kill(); self.p = None

class Gfx(Shot):
    def __init__(self, fn, **kw):
        super().__init__(**kw); self.fn = fn
    def render(self, tl, D, fi):
        out = down(self.fn(tl, D))
        return self.apply_overlays(out, tl, D, lambda x, y: (x * W, y * H))

class FilmPlus(Film):
    """Film with an SS overlay function fn(tl, D) -> RGBA layer (used for the name card)."""
    def __init__(self, name, ovfn, **kw):
        super().__init__(name, **kw); self.ovfn = ovfn
    def render(self, tl, D, fi):
        base = super().render(tl, D, fi)
        return comp_overlay(base, self.ovfn(tl, D))

# ---------------------------------------------------------------- X-ray of the real Pogo (shot F): cones over the frozen frame
def fy(y): return y * 1.101 - 54.3     # old preview (square-pixel) y -> corrected 4:3 y
XR_CANOPY = (952, fy(681)); XR_NOSE = (939, fy(575)); XR_BASE = fy(839)
XR_Z, XR_ZC = 2.0, (950, 715)

def xray_overlay(cues):
    fz, c_sky, c_red, c_grn = cues
    def f(d, tl, D, Pmap):
        if tl < fz + 0.2: return
        def S(p): return Pmap(p[0] / W, p[1] / H)
        canopy = S(XR_CANOPY); nose = S(XR_NOSE); base = S((XR_CANOPY[0], XR_BASE))
        a0 = e(tl, fz + 1.0, fz + 1.5)
        d.rounded_rectangle([(canopy[0] - 350) * SS, (base[1] + 28) * SS, (canopy[0] + 60) * SS, (base[1] + 72) * SS], radius=8 * SS, fill=(8, 10, 13, int(170 * a0)))
        T(d, (canopy[0] - 330, base[1] + 50), "XFY-1 · STANDING ON ITS TAIL", 22, AMBER, a0, anchor="lm", font=FSB, spacing=2)
        lay = f.lay; dl = ImageDraw.Draw(lay)
        a1 = e(tl, c_sky, c_sky + 0.8)
        if a1 > 0:
            sp = 330 * a1
            dl.polygon([(canopy[0] * SS, canopy[1] * SS), ((canopy[0] - sp) * SS, 40 * SS), ((canopy[0] + sp) * SS, 40 * SS)], fill=STEEL + (int(70 * a1),), outline=STEEL + (int(220 * a1),))
            T(dl, (canopy[0], 74), "IN FRONT OF HIM: SKY", 32, STEEL, e(tl, c_sky + 0.5, c_sky + 0.9), font=FDB, spacing=2)
        a2 = e(tl, c_red, c_red + 0.8)
        if a2 > 0:
            dl.polygon([(canopy[0] * SS, canopy[1] * SS), ((canopy[0] - 120) * SS, base[1] * SS), ((canopy[0] + 120) * SS, base[1] * SS)], fill=RED + (int(85 * a2),), outline=RED + (int(230 * a2),))
            gfx.callout(lay, (canopy[0] + 60, (canopy[1] + base[1]) / 2), (canopy[0] + 300, (canopy[1] + base[1]) / 2 + 10), ["BELOW HIM: HIS OWN AIRCRAFT"], RED, min(1, (tl - c_red - 0.5) / 0.8) if tl > c_red + 0.5 else 0, 28)
        a3 = e(tl, c_grn, c_grn + 1.4)
        if a3 > 0:
            pts = [(canopy[0] - 30 - 520 * math.sin(u * math.pi / 2), canopy[1] - 140 * math.sin(u * math.pi) + (base[1] + 30 - canopy[1]) * u ** 2) for u in [k / 40 for k in range(41)]]
            dashed(dl, pts, GREEN, 6, 1.0, k=a3)
            if a3 > 0.97:
                arrow(dl, pts[-3], pts[-1], GREEN, 6, 22)
                T(dl, (70, 250), "OVER HIS SHOULDER:", 32, GREEN, e(tl, c_grn + 1.3, c_grn + 1.7), anchor="lm", font=FDB)
                T(dl, (70, 292), "THE ONLY VIEW OF THE GROUND", 32, GREEN, e(tl, c_grn + 1.3, c_grn + 1.7), anchor="lm", font=FDB)
        if tl > fz + 1.6: gfx.callout(lay, canopy, (canopy[0] + 260, canopy[1] - 120), ["PILOT"], AMBER, min(1, (tl - fz - 1.6) / 0.8), 30)
    f.needs_layer = True
    return f

def three_questions(cues):
    def f(d, tl, D, Pmap):
        d.rectangle([0, 0, W * SS, H * SS], fill=(8, 10, 13, int(120 * e(tl, 0, 0.6))))
        T(d, (960, 230), "HE HAD TO JUDGE THREE THINGS AT ONCE", 34, DIM, e(tl, 0.3, 0.8) * (1 - e(tl, D - 0.3, D)), font=FSB, spacing=3)
        qs = ["HOW HIGH AM I?", "HOW FAST AM I SINKING?", "AM I DRIFTING SIDEWAYS?"]
        for i, (q, c) in enumerate(zip(qs, cues)):
            a = e(tl, c, c + 0.35) * (1 - e(tl, D - 0.3, D))
            y = 420 + i * 150
            T(d, (560, y), f"{i + 1}", 80, AMBER, a, font=FDB)
            T(d, (640, y), q, 64, OFFWHITE, a, anchor="lm", font=FDB)
    return f

# ---------------------------------------------------------------- the timeline
NAVY = "U.S. NAVY FILM · NATIONAL ARCHIVES"
def build_timeline():
    S = []   # (global_start, shot)
    def add(t, shot): S.append((t, shot))
    # --- cold open
    add(0.0, Gfx(gfx2.sc_typewriter("NOVEMBER 1954")))
    add(g1(2.62), Film("D_lowangle_hanging.mp4", speed=0.55, keys=((0, 1.0, .5, .45), (5.0, 1.12, .58, .4)), overlays=[source_tag(NAVY)]))
    add(g1(7.0), Film("A_hover_high.mp4", src_in=1.0, speed=0.7, keys=((0, 1.05, .5, .5), (2.2, 1.12, .5, .45))))
    add(g1(9.0), Film("B_descent_touchdown.mp4", src_in=0.5, speed=0.8, keys=((0, 1.0, .5, .5), (3.3, 1.08, .5, .55))))
    add(g1(12.2), Photo(PH("C16_Richie_pilot_by_Pogo_1955_noknown.jpg"), ((0, 1.0, .5, .78), (4.0, 1.25, .48, .35)), mode="cover", bw=True))
    add(g1(16.1), Film("C_hover_descent2.mp4", speed=0.72, keys=((0, 1.0, .5, .5), (8.7, 1.1, .5, .5)), overlays=[lower_third("LANDING TAIL-FIRST", "CONVAIR XFY-1 · 1954")]))
    add(g1(25.7), Gfx(gfx2.sc_danger))
    add(g1(31.7), Photo(PH("xfv1/X01_XFV1_standing_crew_Edwards_USN_PD.jpg"), ((0, 1.0, .5, .5), (6.2, 1.12, .5, .42)), mode="card",
                        overlays=[lower_third("LOCKHEED XFV-1", "THE RIVAL"), red_stamp("NEVER ONCE", 3.95)]))
    add(g1(37.9), Film("G_takeoff1.mp4", src_in=6.0, speed=1.0, keys=((0, 1.0, .5, .5),)))
    add(g1(40.3), FilmPlus("F_standing_wide.mp4", gfx2.sc_name_overlay, src_in=0.5, speed=0.8, keys=((0, 1.0, .5, .5), (4.6, 1.1, .5, .52))))
    add(VO_A_OFF + VO_A_END + 0.05, Gfx(gfx2.sc_title))
    # --- the questions
    add(g1(43.6), Photo(PH("C12_hover_from_below_Pogo2_unknown_PD.jpg"), ((0, 1.0, .5, .45), (4.4, 1.15, .5, .4)), mode="cover", bw=True))
    add(g1(48.0), Photo(PH("C01_level_flight_over_SanDiego_USN_PD.jpg"), ((0, 1.35, .42, .42), (4.0, 1.45, .45, .4)), mode="cover", bw=True, xin=0.4))
    add(g1(52.0), Gfx(gfx2.sc_text_card(["ONE PROBLEM."])))
    add(g1(54.7), Film("E_on_ground_crew.mp4", src_in=1.0, speed=0.85, keys=((0, 1.0, .5, .5), (5.1, 1.08, .5, .5)), tint=0.15))
    # --- WWII
    add(g1(59.8), Film("L_ships_at_anchor_aerial.mp4", src_in=0.0, mode="framed", overlays=[source_tag("1941–42 · NATIONAL ARCHIVES")]))
    add(g1(61.75), Film("K_convoy_route_map_Halifax_Iceland.mp4", src_in=6.0, mode="framed", overlays=[lower_third("ALLIED CONVOY ROUTE", "HALIFAX · ICELAND · BRITAIN"), source_tag("OSS FILM · NATIONAL ARCHIVES")]))
    add(g1(68.85), Film("M_docks_merchant_ships.mp4", src_in=2.0, mode="framed"))
    add(g1(73.6), Gfx(gfx2.sc_runway_carrier))
    add(g1(80.0), Film("J_F3D_carrier_deck.mp4", src_in=3.0, speed=0.9, keys=((0, 1.0, .5, .5), (3.4, 1.06, .5, .5)), overlays=[lower_third("AFTER THE WAR", "U.S. NAVY")]))
    add(g1(83.4), Film("L_ships_at_anchor_aerial.mp4", src_in=10.0, mode="framed", overlays=[big_question("WHAT IF ANY SHIP", "COULD CARRY ITS OWN FIGHTER?", 0.2)]))
    add(g1(86.75), Gfx(gfx2.sc_no_runway))
    add(g1(92.5), Gfx(gfx2.sc_ship_vertical))
    add(g1(100.05), Photo(PH("C06_in_production_hangar_SDASM_0074978_PD.jpg"), ((0, 1.0, .5, .4), (4.6, 1.15, .5, .35)), mode="cover", bw=True,
                          overlays=[typewriter("1951", "THE NAVY ORDERS PROTOTYPES: CONVAIR AND LOCKHEED", (110, 170), 0.2, 64)]))
    add(g1(104.65), Photo("photos/DoD_newsreel_release_38-54_17Mar1954.jpg" if False else os.path.join(HERE, "photos", "DoD_newsreel_release_38-54_17Mar1954.jpg"),
                          ((0, 1.6, .5, .3), (1.4, 2.3, .48, .43), (3.0, 2.3, .48, .43)), mode="card",
                          overlays=[highlight_boxes([(0.4, (0.32, 0.225, 0.61, 0.25)), (1.5, (0.085, 0.398, 0.82, 0.445))]), source_tag("DEPARTMENT OF DEFENSE · 17 MARCH 1954")]))
    add(g1(107.65), Gfx(split_screen))
    add(g1(110.7), Photo(PH("C03_Convair_test_pilot_c1954_USN_PD.jpg"), ((0, 1.0, .5, .8), (3.1, 1.2, .55, .3)), mode="cover", bw=True))
    add(g1(113.8), Gfx(gfx2.sc_catch))
    add(g1(126.9), Film("F_standing_wide.mp4", src_in=7.0, speed=0.75, keys=((0, 1.0, .5, .5), (3.5, 1.1, .5, .45)), tint=0.25))
    add(g1(130.4), Photo(PH("C05_colour_takeoff_SDASM_0074616_PD.jpg"), ((0, 1.0, .5, .55), (2.8, 1.15, .5, .5)), mode="cover", bw=True))
    add(g1(133.2), Photo(PH("C15_NAVAER_standard_characteristics_May1952_SDASM_PD.jpg"),
                         ((0, 2.3, .22, .75), (1.8, 2.3, .22, .75), (2.4, 2.1, .2, .3), (3.2, 2.1, .2, .3), (3.9, 2.6, .215, .53), (5.8, 2.8, .215, .53)), mode="card",
                         overlays=[callouts([(0.15, (.20, .735), (1250, 300), ["SHORT, FAT FUSELAGE"], AMBER, 2.0),
                                             (2.4, (.14, .24), (1250, 300), ["DELTA WING"], AMBER, 3.3),
                                             (4.0, (.215, .462), (1250, 300), ["FINS ABOVE AND BELOW"], AMBER, 99)]),
                                   source_tag("NAVAER STANDARD AIRCRAFT CHARACTERISTICS · MAY 1952")]))
    add(g1(139.0), Gfx(gfx2.sc_rear_cross))
    add(g1(148.45), Film("E_on_ground_crew.mp4", src_in=4.0, speed=0.8, keys=((0, 1.0, .5, .5), (3.8, 1.1, .5, .45)), overlays=[text_lines([(2.3, (960, 1000), "IT STOOD.", OFFWHITE, "mm")], 52)]))
    add(g1(152.2), Gfx(gfx2.sc_engine))
    add(g1(161.9), Photo(PH("C15_NAVAER_standard_characteristics_May1952_SDASM_PD.jpg"), ((0, 2.6, .22, .55), (4.0, 3.1, .23, .57)), mode="card",
                         overlays=[highlight_boxes([(0.6, (0.205, 0.597, 0.34, 0.613))])]))
    add(g1(166.0), Gfx(gfx2.sc_props_front))
    add(g1(170.45), Film("A_hover_high.mp4", src_in=3.0, speed=0.7, keys=((0, 1.05, .5, .5), (1.7, 1.1, .5, .5))))
    add(g1(172.1), Gfx(gfx2.sc_thrust))
    add(g1(192.1), Film("C_hover_descent2.mp4", src_in=1.5, speed=0.85, keys=((0, 1.0, .5, .5), (5.5, 1.15, .5, .45)), overlays=[lower_third("BALANCING ON ITS TAIL", "EVERY SECOND")]))
    add(g1(197.55), Gfx(gfx2.sc_torque))
    # --- Part 2
    add(g2(-1.5) + 0.0, Film("H_takeoff2.mp4", src_in=2.0, speed=1.0, keys=((0, 1.0, .5, .55), (5.0, 1.08, .5, .5))))
    add(g2(3.5), Film("B_descent_touchdown.mp4", src_in=0.0, speed=0.6, keys=((0, 1.0, .5, .5), (4.0, 1.12, .5, .55)), tint=0.25))
    add(g2(7.5), Photo(PH("C11_tethered_hangar_MoffettFld_NAN8-54_USN_PD.jpg"), ((0, 0.95, .5, .5), (11.7, 1.25, .5, .45)), mode="card", crop=(0, 0, 1, 0.62),
                       overlays=[typewriter("SPRING 1954", "HANGAR ONE · MOFFETT FIELD, CALIFORNIA", (110, 150), 0.2, 50),
                                 text_lines([(5.5, (1640, 900), "BUILT FOR A NAVY AIRSHIP", AMBER, "mm")], 28)]))
    add(g2(19.2), Photo(PH("C11_tethered_hangar_MoffettFld_NAN8-54_USN_PD.jpg"), ((0, 1.4, .5, .45), (9.8, 1.7, .55, .62)), mode="card", crop=(0, 0, 1, 0.62),
                        overlays=[callouts([(0.4, (.48, .14), (1250, 230), ["TIED TO CABLES"], AMBER), (1.6, (.85, .97), (1350, 900), ["FOR SAFETY"], AMBER)])]))
    add(g2(29.0), Photo(PH("C07_Coleman_portrait_SDASM_000419_PD.jpg"), ((0, 1.0, .5, .45), (5.2, 1.18, .5, .35)), mode="card", bw=True,
                        overlays=[lower_third("JAMES \"SKEETS\" COLEMAN", "CONVAIR TEST PILOT", 0.6)]))
    add(g2(34.2), Photo(PH("C09_Coleman_cockpit_ladder_SDASM_000414_PD.jpg"), ((0, 1.0, .5, .75), (6.3, 1.25, .5, .3)), mode="card", bw=True,
                        overlays=[text_lines([(3.2, (1690, 950), "TWO STOREYS UP", AMBER, "mm")], 34)]))
    add(g2(40.5), Photo(PH("C10_Coleman_cockpit_close_SDASM_000411_PD.jpg"), ((0, 1.05, .5, .45), (3.4, 1.2, .5, .4)), mode="card", bw=True, xin=0.3))
    add(g2(43.9), Gfx(gfx2.sc_seat))
    add(g2(48.5), Photo(PH("C14_Coleman_cockpit_SDASM_000429_PD.jpg"), ((0, 1.0, .5, .5), (4.3, 1.15, .5, .4)), mode="card", bw=True))
    add(g2(52.75), Film("G_takeoff1.mp4", src_in=0.0, speed=1.0, keys=((0, 1.0, .5, .55), (9.1, 1.1, .5, .5)),
                        overlays=[typewriter("1 AUGUST 1954", "FIRST FREE FLIGHT · THE CABLES COME OFF", (110, 150), 0.1, 50)]))
    add(g2(61.9), Film("H_takeoff2.mp4", src_in=8.0, speed=1.0, keys=((0, 1.0, .5, .5), (4.9, 1.08, .5, .45))))
    add(g2(66.8), Gfx(gfx2.sc_transition))
    add(g2(69.5), Photo(PH("C01_level_flight_over_SanDiego_USN_PD.jpg"), ((0, 1.35, .40, .45), (2.7, 1.5, .45, .42)), mode="cover", bw=True,
                        overlays=[lower_third("LEVEL FLIGHT", "OVER SAN DIEGO")]))
    add(g2(72.2), Photo(PH("C12_hover_from_below_Pogo2_unknown_PD.jpg"), ((0, 1.2, .5, .4), (1.9, 1.35, .5, .38)), mode="cover", bw=True, tint=0.2,
                        overlays=[text_lines([(0.2, (960, 980), "LANDING WAS THE PROBLEM.", OFFWHITE, "mm")], 52)]))
    add(g2(74.1), Gfx(gfx2.sc_pitch((0.0, 0.1, 1.9, 5.3))))
    add(g2(81.85), Film("B_descent_touchdown.mp4", src_in=1.5, speed=0.75, keys=((0, 1.0, .5, .5), (4.0, 1.1, .5, .55)), overlays=[lower_third("TAIL-FIRST", "")]))
    add(g2(85.8), Film("F_standing_wide.mp4", src_in=1.0, speed=1.0, freeze=1.2, keys=((0, 1.0, .5, .5), (1.35, 1.0, XR_ZC[0] / W, XR_ZC[1] / H), (2.6, XR_Z, XR_ZC[0] / W, XR_ZC[1] / H)),
                       overlays=[xray_overlay((1.2, 2.7, 4.9, 7.5))]))
    add(g2(98.4), Film("C_hover_descent2.mp4", src_in=0.0, speed=0.8, keys=((0, 1.0, .5, .5), (8.9, 1.12, .5, .5)), overlays=[three_questions((3.4, 4.8, 6.45))]))
    add(g2(107.3), Gfx(gfx2.sc_altimeter))
    add(g2(115.65), Gfx(gfx2.sc_rear_danger))
    add(g2(131.25), Photo(PH("C14_Coleman_cockpit_SDASM_000429_PD.jpg"), ((0, 1.2, .5, .35), (3.3, 1.35, .5, .3)), mode="card", bw=True,
                          overlays=[text_lines([(0.4, (1690, 930), "BACKWARDS. BY EYE.", OFFWHITE, "mm")], 34)]))
    add(g2(134.55), Gfx(gfx2.sc_four_cars))
    add(g2(137.8), Photo(PH("C02_BrownField_takeoff_Nov1954_TBM_USN_PD.jpg"), ((0, 1.0, .5, .5), (4.8, 1.15, .52, .45)), mode="cover", bw=True,
                         overlays=[typewriter("2 NOVEMBER 1954", "BROWN FIELD, NEAR SAN DIEGO", (110, 150), 0.1, 50)]))
    add(g2(142.6), Gfx(gfx2.sc_full_cycle))
    add(g2(150.45), Film("I_cameraman.mp4", src_in=0.0, speed=0.9, keys=((0, 1.0, .5, .5), (3.4, 1.08, .5, .5)), overlays=[source_tag(NAVY)]))
    add(g2(153.85), Photo(PH("C08_Coleman_by_FY-1_SDASM_000423_PD.jpg"), ((0, 1.0, .5, .5), (4.5, 1.1, .5, .45)), mode="card", bw=True, overlays=[trophy(0.3)]))
    add(g2(158.3), Film("D_lowangle_hanging.mp4", src_in=0.5, speed=0.6, keys=((0, 1.0, .5, .45), (1.8, 1.08, .55, .42))))
    add(g2(160.05), Photo(PH("C07_Coleman_portrait_SDASM_000419_PD.jpg"), ((0, 1.15, .5, .4), (7.0, 1.35, .5, .33)), mode="card", bw=True))
    S.sort(key=lambda x: x[0])
    return S

def split_screen(tl, D):
    """Pogo (left) and XFV-1 (right) standing on their tails."""
    img = Image.new("RGB", (W * SS, H * SS), (12, 14, 18)); d = ImageDraw.Draw(img, "RGBA")
    for i, (path, lab, crop) in enumerate(((PH("C03_Convair_test_pilot_c1954_USN_PD.jpg"), "CONVAIR XFY-1", (0.25, 0.0, 1.0, 0.85)),
                                           (PH("xfv1/X01_XFV1_standing_crew_Edwards_USN_PD.jpg"), "LOCKHEED XFV-1", (0.05, 0.05, 0.95, 0.9)))):
        im = load_photo(path, True, crop)
        z = 1.0 + 0.06 * tl / D
        tw_, th_ = int(W * SS / 2 * z), int(H * SS * z)
        r = max(tw_ / im.width, th_ / im.height)
        im2 = im.resize((int(im.width * r), int(im.height * r)), Image.BICUBIC)
        x0 = (im2.width - W * SS // 2) // 2; y0 = (im2.height - H * SS) // 2
        img.paste(im2.crop((x0, y0, x0 + W * SS // 2, y0 + H * SS)), (i * W * SS // 2, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 820 * SS, W * SS, H * SS], fill=(8, 10, 13, 170))
    d.rectangle([(960 - 3) * SS, 0, (960 + 3) * SS, H * SS], fill=AMBER + (255,))
    T(d, (480, 880), "CONVAIR XFY-1", 40, OFFWHITE, e(tl, 0.1, 0.5), font=FDB, spacing=3)
    T(d, (1440, 880), "LOCKHEED XFV-1", 40, OFFWHITE, e(tl, 0.1, 0.5), font=FDB, spacing=3)
    T(d, (960, 990), "THE SAME BASIC IDEA: A FIGHTER THAT SITS ON ITS TAIL", 34, AMBER, e(tl, 0.5, 1.0), font=FSB, spacing=2)
    return img

# ---------------------------------------------------------------- render
def render_range(S, f0, f1, out):
    starts = [s for s, _ in S]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-tune", "film", "-pix_fmt", "yuv420p", "-g", "60", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last_i = None
    for fi in range(f0, f1):
        t = fi / FPS
        i = max(0, bisect.bisect_right(starts, t) - 1)
        st, shot = S[i]; D = (S[i + 1][0] if i + 1 < len(S) else END) - st
        img = shot.render(t - st, D, fi)
        if shot.xin and t - st < shot.xin and i > 0:
            pst, pshot = S[i - 1]
            pimg = pshot.render(t - pst, st - pst, fi)
            img = Image.blend(pimg, img, ease((t - st) / shot.xin))
        if i != last_i:
            for j in range(0, max(0, i - 1)): S[j][1].close()
        last_i = i
        img = finish(img, fi)
        if t < 0.0: pass
        if t > END - 2.0: img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (t - (END - 2.0)) / 2.0))
        p.stdin.write(img.tobytes())
        if fi % 150 == 0: print(f"  frame {fi} / {f1}", flush=True)
    p.stdin.close(); p.wait()
    for _, s in S: s.close()

def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    S = build_timeline()
    N = int(END * FPS)
    if "--still" in sys.argv:
        for ts in sys.argv[sys.argv.index("--still") + 1:]:
            t = float(ts); starts = [s for s, _ in S]; i = max(0, bisect.bisect_right(starts, t) - 1)
            st, shot = S[i]; D = (S[i + 1][0] if i + 1 < len(S) else END) - st
            finish(shot.render(t - st, D, int(t * FPS)), 0).save(f"{out}/still_{t:07.2f}.png"); shot.close()
        return
    if "--cues" in sys.argv:
        json.dump({"END": END, "VO": [[VO_A_OFF, 0, VO_A_END], [VO_B_OFF, VO_A_END, P1_LEN], [VO_C_OFF, 0, P2_LEN]],
                   "shots": [[round(s, 3), type(x).__name__, getattr(x, "name", getattr(x, "path", getattr(getattr(x, "fn", None), "__name__", "")))] for s, x in S]},
                  open(f"{out}/cues.json", "w"), indent=1)
        return
    k, n = int(sys.argv[2]), int(sys.argv[3])
    # split on shot boundaries closest to equal frame counts
    bounds = [0] + [int(N * j / n) for j in range(1, n)] + [N]
    render_range(S, bounds[k], bounds[k + 1], f"{out}/v_{k:02d}.mp4")

if __name__ == "__main__":
    main()
