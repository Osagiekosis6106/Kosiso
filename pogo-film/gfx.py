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
