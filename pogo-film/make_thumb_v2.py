"""Premium Pogo thumbnail (v2): the user's own Grok image, old text removed, re-lettered in the channel style.
Usage: python3 make_thumb_v2.py BASE.jpg GHOST_CUTOUT.png OUT.jpg"""
import sys, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

BASE, GHOST, OUT = sys.argv[1:4]
W, H, SS = 1280, 720, 2
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FL = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"

# 1. remove the old lettering and label (keep the aircraft untouched)
im = cv2.imread(BASE); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
h, s, v = [hsv[..., i].astype(int) for i in range(3)]
white = (s < 50) & (v > 190); yellow = (h > 12) & (h < 38) & (s > 100) & (v > 150); dark = v < 70
m = np.zeros(im.shape[:2], np.uint8)
reg = np.zeros_like(m); reg[150:560, 15:455] = 1
qm = np.zeros_like(m); qm[290:430, 430:482] = 1
lab = np.zeros_like(m); lab[150:255, 740:1010] = 1
m[((white | yellow) & (reg == 1)) | (yellow & (qm == 1)) | ((white | dark) & (lab == 1) & ~yellow)] = 255
m = cv2.dilate(m, np.ones((11, 11), np.uint8)); m[:, 482:740] = 0
im = cv2.inpaint(im, m, 12, cv2.INPAINT_TELEA)
base = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((W * SS, H * SS), Image.LANCZOS)

# 2. grade: deeper navy shadows, hotter orange highlights, more contrast and clarity
a = np.asarray(base, np.float32) / 255
lum = a @ np.array([0.299, 0.587, 0.114], np.float32)
sh = (1 - lum)[..., None] ** 2; hi = lum[..., None] ** 2
a = a * (1 - 0.18 * sh) + sh * 0.18 * np.array([0.05, 0.10, 0.22]) + hi * 0.10 * np.array([1.0, 0.55, 0.15])
a = np.clip((a - 0.5) * 1.12 + 0.5, 0, 1)
base = Image.fromarray((a * 255).astype(np.uint8))
base = Image.blend(base, base.filter(ImageFilter.UnsharpMask(6, 70, 2)), 0.8).convert("RGBA")
w, h_ = base.size

# 3. dark navy gradient behind the headline (also hides the inpainted area)
g = np.zeros((h_, w), np.float32); x = np.linspace(0, 1, w)[None, :]
g[:] = np.clip(1 - x / 0.50, 0, 1) ** 1.1 * 235
ov = Image.new("RGBA", (w, h_), (6, 12, 26, 0)); ov.putalpha(Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(30)))
base.alpha_composite(ov)

# 4. ghost Pogo (real photo) top left, like the ghost aircraft in the channel thumbnails
gc = Image.open(GHOST).convert("RGBA"); gc = gc.crop(gc.getbbox())
gc = gc.resize((int(gc.width * 190 * SS / gc.height), 190 * SS), Image.LANCZOS)
garr = (np.asarray(gc.convert("RGB"), np.float32) * np.array([0.55, 0.68, 0.85])).astype(np.uint8)
gh = Image.fromarray(garr).convert("RGBA"); gh.putalpha(gc.getchannel("A").point(lambda q: q * 110 // 255))
base.alpha_composite(gh.filter(ImageFilter.GaussianBlur(1.2)), (38 * SS, 14 * SS))

def condensed(txt, height, fill, squeeze=0.78, font=FB):
    f = ImageFont.truetype(font, int(height * 1.32)); l, t, r, b = f.getbbox(txt)
    t_ = Image.new("RGBA", (r - l + 12, b - t + 12), (0, 0, 0, 0))
    ImageDraw.Draw(t_).text((6 - l, 6 - t), txt, font=f, fill=fill)
    return t_.resize((int(t_.width * squeeze), t_.height), Image.LANCZOS)

def gold(t_):
    hh = t_.height; y = np.linspace(0, 1, hh, dtype=np.float32)[:, None, None]
    top, mid, bot = np.array([255, 236, 140.]), np.array([255, 196, 50.]), np.array([214, 112, 10.])
    col = np.where(y < 0.5, top * (1 - y * 2) + mid * (y * 2), mid * (2 - y * 2) + bot * (y * 2 - 1))
    arr = np.repeat(col, t_.width, 1).astype(np.uint8); out = Image.fromarray(arr).convert("RGBA"); out.putalpha(t_.getchannel("A")); return out

def place(t_, xy, glow=None):
    P = 50 * SS                                   # room for the soft shadow/glow so it never clips into a box
    big = Image.new("RGBA", (t_.width + 2 * P, t_.height + 2 * P), (0, 0, 0, 0)); big.alpha_composite(t_, (P, P))
    t_, xy = big, (xy[0] - P, xy[1] - P)
    al = t_.getchannel("A")
    stroke = Image.new("RGBA", t_.size, (8, 10, 16, 0)); stroke.putalpha(al.filter(ImageFilter.MaxFilter(9)))
    shadow = Image.new("RGBA", t_.size, (0, 0, 0, 0)); shadow.putalpha(al.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(14)).point(lambda q: q * 230 // 255))
    if glow:
        gl = Image.new("RGBA", t_.size, glow + (0,)); gl.putalpha(al.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(26)).point(lambda q: q * 150 // 255))
        base.alpha_composite(gl, xy)
    base.alpha_composite(shadow, (xy[0] + 10 * SS, xy[1] + 12 * SS))
    base.alpha_composite(stroke, xy); base.alpha_composite(t_, xy)

# 5. headline: LANDS (white) / BACKWARDS? (gold), bigger than the competitors'
t1 = condensed("LANDS", 240 * SS, (250, 250, 248), 0.74)
t2 = gold(condensed("BACKWARDS?", 150 * SS, (255, 255, 255)))
k = 470 * SS / t2.width; t2 = t2.resize((int(t2.width * k), int(t2.height * k)), Image.LANCZOS)
k1 = 470 * SS / t1.width; t1 = t1.resize((int(t1.width * k1), int(t1.height * k1)), Image.LANCZOS)
x0 = 34 * SS; y0 = 168 * SS
place(t1, (x0, y0)); place(t2, (x0, y0 + t1.height - 6 * SS), glow=(255, 140, 20))

# 6. label + arrow to the cockpit
lab = condensed("HE CAN'T SEE", 30 * SS, (255, 255, 255), 0.9, FL); lab2 = condensed("THE GROUND", 30 * SS, (255, 210, 90), 0.9, FL)
lx, ly = 790 * SS, 138 * SS
place(lab, (lx, ly)); place(lab2, (lx, ly + lab.height))
d = ImageDraw.Draw(base)
a0 = (lx - 8 * SS, ly + lab.height); tip = (738 * SS, 172 * SS); c = (a0[0] - 10 * SS, a0[1] + 40 * SS)
pts = [((1 - t) ** 2 * a0[0] + 2 * (1 - t) * t * c[0] + t * t * tip[0], (1 - t) ** 2 * a0[1] + 2 * (1 - t) * t * c[1] + t * t * tip[1]) for t in np.linspace(0, 1, 40)]
for wd, col in ((11 * SS, (0, 0, 0, 150)), (5 * SS, (255, 255, 255, 255))): d.line(pts, fill=col, width=wd, joint="curve")
ex, ey = pts[-1]; px, py = pts[-5]; ang = math.atan2(ey - py, ex - px)
d.polygon([(ex + 20 * SS * math.cos(ang), ey + 20 * SS * math.sin(ang)), (ex + 13 * SS * math.cos(ang + 2.3), ey + 13 * SS * math.sin(ang + 2.3)),
           (ex + 13 * SS * math.cos(ang - 2.3), ey + 13 * SS * math.sin(ang - 2.3))], fill=(255, 255, 255))

# 7. finish: vignette + fine grain
out = base.convert("RGB").resize((W, H), Image.LANCZOS)
arr = np.asarray(out, np.float32); yy, xx = np.mgrid[0:H, 0:W]
vig = 1 - 0.28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.5
arr = arr * vig.clip(0.55, 1)[..., None] + np.random.default_rng(3).normal(0, 3.5, arr.shape)
Image.fromarray(arr.clip(0, 255).astype(np.uint8)).save(OUT, quality=95)
