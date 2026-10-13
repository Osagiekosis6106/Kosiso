"""Two test thumbnails for the Pogo video, built from the real public-domain photo (no AI aircraft).
Usage: python3 make_thumbs.py CUTOUT.png GHOST_CUTOUT.png OUTDIR
CUTOUT = photos/cleared/C12 with the sky removed (rembg isnet-general-use)."""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageChops

W, H = 1280, 720
SS = 2                                     # draw at 2x, downscale at the end
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FL = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
AMBER, STEEL, GRAPHITE = (232, 163, 61), (111, 163, 200), (22, 25, 30)
rng = np.random.default_rng(4)

def noise(w, h, octaves=6, seed=0):
    r = np.random.default_rng(seed); acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = 2 ** (o + 2)
        n = Image.fromarray((r.random((max(2, h * s // w), s)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += amp * np.asarray(n, np.float32) / 255; tot += amp; amp *= 0.55
    return acc / tot

def load_cut(path):
    im = Image.open(path).convert("RGBA"); return im.crop(im.getbbox())

def grade_metal(im, warm=(1.0, 1.0, 1.0), contrast=1.15):
    rgb, a = im.convert("RGB"), im.getchannel("A")
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    arr = np.asarray(rgb, np.float32) * np.array(warm, np.float32)
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8)); out.putalpha(a); return out

def side_light(im, color, side="right", strength=0.6):
    """tint the lit side of the metal (multiply-ish gradient)"""
    w, h = im.size; g = np.linspace(0, 1, w, dtype=np.float32)
    if side == "left": g = g[::-1]
    g = (g ** 1.6)[None, :, None] * strength
    arr = np.asarray(im.convert("RGB"), np.float32)
    arr = arr * (1 - g) + (arr * np.array(color, np.float32) / 255 * 1.35) * g
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8)); out.putalpha(im.getchannel("A")); return out

def pad(im, m):
    out = Image.new("RGBA", (im.width + 2 * m, im.height + 2 * m), (0, 0, 0, 0)); out.alpha_composite(im, (m, m)); return out

def rim(alpha, color, dx, dy, width=3, blur=2, gain=1.0):
    """bright edge on the side facing the light: alpha minus itself shifted toward the light"""
    sh = ImageChops.offset(alpha, -dx, -dy)
    e = ImageChops.subtract(alpha, sh).filter(ImageFilter.MaxFilter(width)).filter(ImageFilter.GaussianBlur(blur))
    e = ImageChops.multiply(e, alpha).point(lambda v: min(255, int(v * gain)))
    g = Image.new("RGBA", alpha.size, color + (0,)); g.putalpha(e); return g

def glow(alpha, color, grow, blur, gain=1.0):
    a = alpha.filter(ImageFilter.MaxFilter(grow)).filter(ImageFilter.GaussianBlur(blur))
    a = a.point(lambda v: min(255, int(v * gain)))
    g = Image.new("RGBA", alpha.size, color + (0,)); g.putalpha(a); return g

def condensed_text(txt, height, fill, squeeze=0.74, font=FB, stroke=0):
    f = ImageFont.truetype(font, int(height * 1.32))
    l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    im = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - l, 4 - t), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return im.resize((int(im.width * squeeze), im.height), Image.LANCZOS)

def gradient_fill(mask_im, top, bottom):
    w, h = mask_im.size; t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    arr = (np.array(top, np.float32) * (1 - t) + np.array(bottom, np.float32) * t).repeat(w, 1)
    out = Image.fromarray(arr.astype(np.uint8)); out.putalpha(mask_im.getchannel("A")); return out

def grunge(im, amount=0.18, seed=1):
    n = noise(im.width, im.height, 5, seed); n = (n - n.min()) / (n.max() - n.min())
    a = np.asarray(im.getchannel("A"), np.float32) * (1 - amount * (n > 0.62))
    im = im.copy(); im.putalpha(Image.fromarray(a.astype(np.uint8))); return im

def shadowed(layer, off=(6, 8), blur=10, op=200):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.putalpha(layer.getchannel("A").point(lambda v: v * op // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); return sh, off

def film_finish(img, grain=6, vignette=0.35):
    arr = np.asarray(img.convert("RGB"), np.float32)
    yy, xx = np.mgrid[0:img.height, 0:img.width]
    v = 1 - vignette * (((xx - img.width / 2) / (img.width / 2)) ** 2 + ((yy - img.height / 2) / (img.height / 2)) ** 2) ** 1.4
    arr = arr * v.clip(0.35, 1)[..., None] + rng.normal(0, grain, arr.shape)
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

# ------------------------------------------------------------------ A: channel style
def thumb_a(cut, ghost, out):
    w, h = W * SS, H * SS
    # sky: navy storm (left) -> fiery orange/gold (right), cloud texture
    n1, n2 = noise(w // 4, h // 4, 7, 11), noise(w // 4, h // 4, 7, 23)
    x = np.linspace(0, 1, w // 4, dtype=np.float32)[None, :]; y = np.linspace(0, 1, h // 4, dtype=np.float32)[:, None]
    heat = np.clip((x - 0.30) * 1.9 + (n1 - 0.5) * 1.3 - (y - 0.55) * 0.25, 0, 1) ** 1.25
    cloud = np.clip((n2 - 0.38) * 2.4, 0, 1)
    navy_d, navy_l = np.array([6, 12, 28]), np.array([38, 62, 98])
    fire_d, fire_l = np.array([120, 30, 6]), np.array([255, 178, 60])
    navy = navy_d * (1 - cloud[..., None]) + navy_l * cloud[..., None]
    fire = fire_d * (1 - cloud[..., None]) + fire_l * cloud[..., None]
    sky = navy * (1 - heat[..., None]) + fire * heat[..., None]
    sun = np.exp(-(((x - 0.80) / 0.16) ** 2 + ((y - 0.80) / 0.20) ** 2))[..., None] * np.array([255, 210, 120])
    sky = (sky + sun * 0.9).clip(0, 255)
    img = Image.fromarray(sky.astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3)).convert("RGBA")

    # ghost: second real Pogo photo, faded steel-blue, top left (like the ghost bomber in the channel thumbnails)
    gh = ghost.resize((int(ghost.width * 330 * SS / ghost.height), 330 * SS), Image.LANCZOS)
    gh = Image.fromarray((np.asarray(gh.convert("RGB"), np.float32) * np.array([0.45, 0.58, 0.75])).astype(np.uint8)); ga = ghost.resize(gh.size).getchannel("A")
    gh.putalpha(ga.point(lambda v: v * 120 // 255)); gh = gh.filter(ImageFilter.GaussianBlur(1.5))
    img.alpha_composite(gh, (60 * SS, 10 * SS))

    # hero Pogo (real photo), warm side light from the sunset, orange rim glow
    s = 700 * SS / cut.height; p = cut.resize((int(cut.width * s), int(cut.height * s)), Image.LANCZOS)
    p = grade_metal(p, (1.0, 0.99, 0.97), 1.25); p = side_light(p, (255, 170, 80), "right", 0.40)
    M = 60 * SS; p = pad(p, M)
    px, py = 700 * SS - M, 18 * SS - M
    img.alpha_composite(glow(p.getchannel("A"), (255, 120, 20), 9, 26, 1.6), (px, py))
    img.alpha_composite(glow(p.getchannel("A"), (255, 200, 90), 3, 4, 1.4), (px, py))
    img.alpha_composite(p, (px, py))
    img.alpha_composite(rim(p.getchannel("A"), (255, 190, 90), 7 * SS, -3 * SS, 3, 2, 2.2), (px, py))

    # headline: LANDS (white) / BACKWARDS? (gold gradient), grunge, drop shadow
    t1 = grunge(condensed_text("LANDS", 150 * SS, (255, 255, 255)), 0.12, 3)
    t2 = condensed_text("BACKWARDS?", 150 * SS, (255, 255, 255))
    t2 = grunge(gradient_fill(t2, (255, 222, 90), (238, 140, 18)), 0.12, 5)
    k = min(1.0, 640 * SS / t2.width); t1 = t1.resize((int(t1.width * k), int(t1.height * k))); t2 = t2.resize((int(t2.width * k), int(t2.height * k)))
    for t, (tx, ty) in ((t1, (48 * SS, 330 * SS)), (t2, (48 * SS, 330 * SS + t1.height - 6 * SS))):
        sh, off = shadowed(t, (8 * SS, 10 * SS), 12 * SS, 230); img.alpha_composite(sh, (tx + off[0], ty + off[1])); img.alpha_composite(t, (tx, ty))

    # label + curved arrow to the canopy
    d = ImageDraw.Draw(img)
    lab = condensed_text("HE CAN'T SEE THE GROUND", 30 * SS, (255, 255, 255), 0.86, FL)
    lx, ly = 215 * SS, 112 * SS
    sh, off = shadowed(lab, (3 * SS, 4 * SS), 5 * SS, 230); img.alpha_composite(sh, (lx + off[0], ly + off[1])); img.alpha_composite(lab, (lx, ly))
    canopy = (px + M + int(0.19 * (p.width - 2 * M)), py + M + int(0.33 * (p.height - 2 * M)))
    a0 = (lx + lab.width + 8 * SS, ly + lab.height // 2 + 4 * SS)
    ctrl = (canopy[0] - 20 * SS, a0[1] - 10 * SS)
    pts = [((1 - t) ** 2 * a0[0] + 2 * (1 - t) * t * ctrl[0] + t * t * (canopy[0] - 6 * SS), (1 - t) ** 2 * a0[1] + 2 * (1 - t) * t * ctrl[1] + t * t * canopy[1]) for t in np.linspace(0, 1, 40)]
    for wdt, col in ((10 * SS, (0, 0, 0, 120)), (5 * SS, (255, 255, 255, 255))):
        d.line(pts, fill=col, width=wdt, joint="curve")
    ex, ey = pts[-1]; px0, py0 = pts[-4]; ang = math.atan2(ey - py0, ex - px0)
    head = [(ex + 22 * SS * math.cos(ang), ey + 22 * SS * math.sin(ang)),
            (ex + 14 * SS * math.cos(ang + 2.3), ey + 14 * SS * math.sin(ang + 2.3)),
            (ex + 14 * SS * math.cos(ang - 2.3), ey + 14 * SS * math.sin(ang - 2.3))]
    d.polygon(head, fill=(255, 255, 255))
    film_finish(img.resize((W, H), Image.LANCZOS), 5, 0.30).save(out, quality=95)

# ------------------------------------------------------------------ B: premium studio (Airspeed idea, done better)
def thumb_b(cut, out):
    w, h = W * SS, H * SS
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :]; y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    base = np.array(GRAPHITE, np.float32)[None, None, :] * (0.22 + 0.35 * (1 - y))[..., None] * np.ones((1, w, 1), np.float32)
    key = np.exp(-(((x - 0.50) / 0.20) ** 2 + ((y - 0.35) / 0.55) ** 2))[..., None] * np.array(AMBER) * 0.22 + np.exp(-(((x - 0.10) / 0.14) ** 2 + ((y - 0.05) / 0.28) ** 2))[..., None] * np.array(AMBER) * 0.55
    rimg = np.exp(-(((x - 0.88) / 0.16) ** 2 + ((y - 0.30) / 0.40) ** 2))[..., None] * np.array(STEEL) * 0.40
    cone = np.clip(1 - np.abs(x - 0.52) / (0.06 + 0.30 * y), 0, 1) ** 1.5
    beam = (cone * (1.1 - y))[..., None] * np.array([235, 200, 150]) * 0.24
    haze = (noise(w // 4, h // 4, 5, 7) - 0.5)
    haze = np.asarray(Image.fromarray(((haze + 0.5) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32)[..., None] / 255 * 26
    bg = base + key + rimg + beam + haze
    floor_y = int(0.88 * h)
    fl = np.zeros_like(bg); fl[floor_y:] = 1
    bg = bg * (1 - fl * 0.35)
    img = Image.fromarray(bg.clip(0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img); d.line([(0, floor_y), (w, floor_y)], fill=AMBER + (28,), width=1 * SS)

    s = 640 * SS / cut.height; p = cut.resize((int(cut.width * s), int(cut.height * s)), Image.LANCZOS)
    p = grade_metal(p, (1.0, 1.0, 1.02), 1.3)
    p = side_light(p, AMBER, "left", 0.45); p = side_light(p, STEEL, "right", 0.40)
    M = 60 * SS; p = pad(p, M)
    px = (w - p.width) // 2 + 30 * SS; py = floor_y - p.height + M - 4 * SS
    # mirror reflection on the glossy floor
    refl = p.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(3 * SS))
    fade = np.linspace(0.55, 0, refl.height, dtype=np.float32)[:, None] ** 1.3
    ra = (np.asarray(refl.getchannel("A"), np.float32) * fade).astype(np.uint8); refl.putalpha(Image.fromarray(ra))
    img.alpha_composite(refl, (px, floor_y - M + 8 * SS))
    # contact glow under the hovering aircraft (prop-wash light pool)
    pool = Image.new("L", (w, h), 0); ImageDraw.Draw(pool).ellipse([px + p.width * 0.15, floor_y - 16 * SS, px + p.width * 0.85, floor_y + 40 * SS], fill=120)
    pool = pool.filter(ImageFilter.GaussianBlur(30 * SS)); pl = Image.new("RGBA", (w, h), AMBER + (0,)); pl.putalpha(pool); img.alpha_composite(pl)
    img.alpha_composite(glow(p.getchannel("A"), STEEL, 3, 40, 0.55), (px, py))
    img.alpha_composite(p, (px, py))
    # foreground haze over the floor
    hz = Image.new("RGBA", (w, h), (40, 44, 52, 0)); ha = np.zeros((h, w), np.float32)
    ha[int(0.70 * h):] = np.linspace(0, 70, h - int(0.70 * h))[:, None]; hz.putalpha(Image.fromarray(ha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(20)))
    img.alpha_composite(hz)
    film_finish(img.resize((W, H), Image.LANCZOS), 4, 0.42).save(out, quality=95)

if __name__ == "__main__":
    cut, ghost, od = load_cut(sys.argv[1]), load_cut(sys.argv[2]), sys.argv[3]
    os.makedirs(od, exist_ok=True)
    thumb_a(cut, ghost, os.path.join(od, "Pogo_Thumbnail_A_channel_style.jpg"))
    thumb_b(cut, os.path.join(od, "Pogo_Thumbnail_B_premium_studio.jpg"))
