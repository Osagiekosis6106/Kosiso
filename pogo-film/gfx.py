"""Hangar Physics graphics kit for the Convair Pogo film (B-58 style: graphite + steel blue + amber).
Renders frames with Pillow at 2x and pipes them to ffmpeg (1080p, 30 fps)."""
import math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, SS, FPS = 1920, 1080, 2, 30
GRAPHITE = (22, 25, 30); AMBER = (232, 163, 61); STEEL = (111, 163, 200)
OFFWHITE = (242, 239, 232); RED = (214, 69, 65); GREEN = (96, 186, 120); GREY = (120, 128, 138)
F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(size, path=F_BOLD): return ImageFont.truetype(path, size * SS)

def background():
    """Graphite with a soft vignette, like the B-58 diagrams."""
    img = Image.new("RGB", (W * SS, H * SS), GRAPHITE)
    glow = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(glow).ellipse([W * SS * 0.15, H * SS * 0.05, W * SS * 0.85, H * SS * 0.95], fill=26)
    glow = glow.filter(ImageFilter.GaussianBlur(220 * SS))
    img.paste(Image.new("RGB", img.size, (40, 45, 52)), mask=glow)
    return img

def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

def text(d, xy, s, size, color=OFFWHITE, anchor="mm", path=F_BOLD, spacing=0):
    f = font(size, path)
    x, y = xy[0] * SS, xy[1] * SS
    if spacing:
        total = sum(d.textlength(c, font=f) for c in s) + spacing * SS * (len(s) - 1)
        cx = x - total / 2 if anchor[0] == "m" else x
        for c in s:
            d.text((cx, y), c, font=f, fill=color, anchor="l" + anchor[1]); cx += d.textlength(c, font=f) + spacing * SS
    else:
        d.text((x, y), s, font=f, fill=color, anchor=anchor)

# ---------------------------------------------------------------- Pogo geometry (feet; tail at x=0, nose at +x, level flight)
FUSE = [(1.2, 1.2), (4, 2.0), (12, 2.6), (20, 2.8), (26, 2.6), (30, 2.2), (33, 1.7),
        (33, -1.7), (30, -2.2), (26, -2.6), (20, -2.8), (12, -2.6), (4, -2.0), (1.2, -1.2)]
CANOPY = [(24.0, 2.55), (25.2, 3.7), (27.6, 3.8), (29.4, 2.4)]
FIN_TOP = [(17.5, 2.6), (4.5, 10.8), (1.0, 10.8), (0.6, 1.3)]
FIN_BOT = [(x, -y) for x, y in FIN_TOP]
WING = [(19.5, 0.35), (1.0, 0.35), (1.0, -0.35), (19.5, -0.35)]   # delta wing seen edge-on
SPINNER = [(33, 1.7), (36.5, 0), (33, -1.7)]
WHEELS = [(-0.4, 11.0), (-0.4, -11.0)]                             # castering wheels on struts behind the fin tips
STRUTS = [((1.0, 10.8), (-0.4, 11.0)), ((1.0, -10.8), (-0.4, -11.0))]
WHEEL_R = 0.55
PROPS = (33.8, 34.6, 8.0)                                          # two discs, 16 ft across

def xf(pts, ang, cx, cy, scale):
    """Rotate (degrees, CCW) about the aircraft's middle, then place on screen (2x pixels)."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        x -= 17; X = x * ca - y * sa; Y = x * sa + y * ca
        out.append(((cx + X * scale) * SS, (cy - Y * scale) * SS))
    return out

def draw_pogo(img, ang=0, cx=960, cy=540, scale=22, props_spin=0.0, fill=STEEL, alpha=110, edge=None):
    edge = edge or tuple(min(255, c + 60) for c in fill)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for poly in (FIN_TOP, FIN_BOT, WING, FUSE, SPINNER):
        p = xf(poly, ang, cx, cy, scale)
        d.polygon(p, fill=fill + (alpha,)); d.line(p + [p[0]], fill=edge + (255,), width=3 * SS)
    c = xf(CANOPY, ang, cx, cy, scale); d.line(c, fill=edge + (255,), width=3 * SS)
    for a_, b_ in STRUTS:
        d.line(xf([a_, b_], ang, cx, cy, scale), fill=edge + (255,), width=3 * SS)
    for wx, wy in WHEELS:
        (px, py), = xf([(wx, wy)], ang, cx, cy, scale); r = WHEEL_R * scale * SS
        d.ellipse([px - r, py - r, px + r, py + r], outline=edge + (255,), width=3 * SS)
    x1, x2, R = PROPS
    for i, x in enumerate((x1, x2)):            # propeller discs edge-on, with a shimmer line
        p = xf([(x, R), (x, -R)], ang, cx, cy, scale)
        d.line(p, fill=AMBER + (200,), width=4 * SS)
        k = math.sin(props_spin * 2 * math.pi + i * math.pi) * R
        q, = xf([(x, k)], ang, cx, cy, scale); r = 0.35 * scale * SS
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=AMBER + (255,))
    img.paste(layer, (0, 0), layer)

def pogo_point(pt, ang, cx, cy, scale):
    (x, y), = xf([pt], ang, cx, cy, scale); return x / SS, y / SS

COCKPIT = (26.5, 2.9)

def stand_cy(ground_y, scale):
    """Screen y of the aircraft's middle so that, standing on its tail (90°), the wheels touch ground_y."""
    return ground_y - (17 - min(w[0] for w in WHEELS) + WHEEL_R) * scale

# ---------------------------------------------------------------- rendering
def render(path, seconds, frame_fn, alpha=False):
    n = int(seconds * FPS)
    if alpha:
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", path]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        im = frame_fn(i / FPS, i).resize((W, H), Image.LANCZOS)
        p.stdin.write(im.convert("RGBA" if alpha else "RGB").tobytes())
    p.stdin.close(); p.wait()

# ---------------------------------------------------------------- v2 look: grid, glow, grain, camera, callouts, real footage
import numpy as np

def grid_background(t=0.0):
    """Graphite blueprint: fine grid, major lines every 5 cells, vignette. Drifts slowly with t."""
    img = background(); d = ImageDraw.Draw(img, "RGBA")
    off = (t * 6) % 40
    for k in range(-1, W // 40 + 2):
        x = (k * 40 - off) * SS; major = (k + int((t * 6) // 40)) % 5 == 0
        d.line([(x, 0), (x, H * SS)], fill=STEEL + (34 if major else 14,), width=SS)
    for k in range(H // 40 + 2):
        y = k * 40 * SS; d.line([(0, y), (W * SS, y)], fill=STEEL + (34 if k % 5 == 0 else 14,), width=SS)
    return img

def glow(img, layer, radius=10, strength=1.0):
    """Paste an RGBA line layer with a soft bloom under it."""
    if strength > 0:
        b = layer.filter(ImageFilter.GaussianBlur(radius * SS))
        if strength != 1.0:
            a = b.getchannel("A").point(lambda v: int(min(255, v * strength))); b.putalpha(a)
        img.paste(b, (0, 0), b)
    img.paste(layer, (0, 0), layer)

def finish(img, i, grain=7, vignette=True):
    """Downscale to 1080p, add film grain and a dark vignette (call last; returns a 1x RGB image)."""
    im = img.convert("RGB").resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    if grain:
        rng = np.random.default_rng(i); a += rng.integers(-grain, grain + 1, (H, W, 1), dtype=np.int16)
    if vignette:
        a = (a * _VIG).astype(np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

_yy, _xx = np.mgrid[0:H, 0:W]
_VIG = (1 - 0.20 * (((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) ** 1.6).clip(0.7, 1)[..., None]

def camera(img, zoom=1.0, cx=None, cy=None):
    """Zoom an SS-sized frame about (cx, cy) in 1x screen pixels; keeps the frame filled."""
    if zoom == 1.0: return img
    cx = W / 2 if cx is None else cx; cy = H / 2 if cy is None else cy
    w, h = W / zoom, H / zoom
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return img.crop((int(x0 * SS), int(y0 * SS), int((x0 + w) * SS), int((y0 + h) * SS))).resize((W * SS, H * SS), Image.BICUBIC)

def callout(img, anchor, label_xy, lines, color=AMBER, k=1.0, size=28, sub=None):
    """Dot on the anchor, leader line drawn on over k (0..1), then a label that slides and fades in."""
    if k <= 0: return
    d = ImageDraw.Draw(img, "RGBA")
    ax, ay = anchor; lx, ly = label_xy
    a = ease(k / 0.5); r = 7 * SS
    d.ellipse([ax * SS - r, ay * SS - r, ax * SS + r, ay * SS + r], fill=color + (int(255 * a),))
    d.ellipse([ax * SS - 2.4 * r, ay * SS - 2.4 * r, ax * SS + 2.4 * r, ay * SS + 2.4 * r], outline=color + (int(140 * a),), width=2 * SS)
    e = ease((k - 0.15) / 0.45)
    if e > 0:
        ex, ey = ax + (lx - ax) * e, ay + (ly - ay) * e
        d.line([(ax * SS, ay * SS), (ex * SS, ey * SS)], fill=color + (230,), width=3 * SS)
    f = ease((k - 0.55) / 0.45)
    if f > 0:
        right = lx >= ax; sl = (1 - f) * 30 * (1 if right else -1)
        tx = lx + (14 if right else -14) + sl; anchor_ = "ls" if right else "rs"
        fnt = font(size); y = ly - 6
        for n, s in enumerate(lines):
            d.text((tx * SS, (y + n * (size + 8)) * SS), s, font=fnt, fill=color + (int(255 * f),), anchor=anchor_)
        if sub:
            d.text((tx * SS, (y + len(lines) * (size + 8)) * SS), sub, font=font(int(size * 0.72)), fill=OFFWHITE + (int(200 * f),), anchor=anchor_)

def prop_disc(img, center, rx, ry, color=AMBER, spin=0.0):
    """A blurred spinning propeller disc seen at an angle (ellipse), with a faint blade sweep."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    cx, cy = center[0] * SS, center[1] * SS
    d.ellipse([cx - rx * SS, cy - ry * SS, cx + rx * SS, cy + ry * SS], fill=color + (40,), outline=color + (150,), width=2 * SS)
    for b in range(3):
        a = spin * 2 * math.pi + b * 2 * math.pi / 3
        d.line([(cx, cy), (cx + math.cos(a) * rx * SS, cy + math.sin(a) * ry * SS)], fill=color + (90,), width=5 * SS)
    img.paste(layer.filter(ImageFilter.GaussianBlur(2 * SS)), (0, 0), layer.filter(ImageFilter.GaussianBlur(2 * SS)))

class Footage:
    """Sequential frame reader for an archival clip: crops 4:3 film to 16:9, scales to 1080p, light grade.
    frame(n) returns frame n as a 2x (SS) RGB image; asking for the same or a later frame is cheap."""
    def __init__(self, path, start=0.0, crop_y=0.5, contrast=1.08):
        vf = (f"fps={FPS},crop=iw:iw*9/16:0:(ih-iw*9/16)*{crop_y},scale={W}:{H}:flags=lanczos,"
              f"eq=contrast={contrast}:brightness=-0.02,format=rgb24")
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-i", path, "-vf", vf,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.n = -1; self.last = None
    def frame(self, n):
        while self.n < n:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            self.last = Image.frombytes("RGB", (W, H), buf); self.n += 1
        return self.last.resize((W * SS, H * SS), Image.BICUBIC)

def render1x(path, seconds, frame_fn):
    """Like render(), but frame_fn returns a finished 1x RGB frame (from finish())."""
    n = int(seconds * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame_fn(i / FPS, i).tobytes())
    p.stdin.close(); p.wait()
