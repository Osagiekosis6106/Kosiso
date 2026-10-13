"""Builds the three vertical Shorts (1080x1920) from the finished film + its stems.
Usage: python3 make_shorts.py F13_DIR STT_DIR OUTDIR
F13_DIR holds master_v.mp4 (picture) and audio/{mix_master,voice_only,music_only}.wav."""
import sys, os, io, json, re, subprocess, contextlib
import numpy as np

F13, STT, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
sys.argv = ["x", STT, os.devnull]
with contextlib.redirect_stdout(io.StringIO()):
    import make_srt                      # sentence list with global times: make_srt.segs
SEGS = make_srt.segs
FONTS = "/usr/share/fonts/opentype/inter"
TMP = os.path.join(OUT, "tmp"); os.makedirs(TMP, exist_ok=True)

# piece = (start, end, mode, cx) in film time; mode: tall (4:5 crop) | mid (4:3) | wide (16:9)
# cx can be a pair (start, end) for a crop that follows the aircraft
SHORTS = {
    "Short1_Land_It_Backwards": dict(
        title="HE HAD TO LAND THIS FIGHTER BACKWARDS", hook="LANDING\nBACKWARDS?!", audio="mix",
        pieces=[(4.10, 8.50, "tall", (0.47, 0.80)), (8.50, 10.50, "tall", 0.48), (10.50, 13.70, "tall", 0.49),
                (13.70, 17.60, "tall", 0.50), (17.60, 27.20, "tall", 0.50), (27.20, 33.20, "mid", 0.50),
                (33.20, 39.40, "tall", 0.53), (39.40, 41.80, "tall", 0.50), (41.80, 45.20, "wide", 0.50)]),
    "Short2_Landing_Blind": dict(
        title="HOW DO YOU LAND LOOKING BACKWARDS?", hook="AS HEAVY AS\n4 CARS", audio="stems",
        pieces=[(354.80, 358.15, "tall", 0.50), (358.15, 361.05, "mid", 0.52),
                (295.65, 297.55, "tall", 0.45), (305.30, 309.20, "tall", 0.49),
                (311.95, 322.00, "wide", 0.50), (322.00, 330.60, "mid", 0.50),
                (361.30, 366.20, "mid", 0.80), (366.20, 374.05, "wide", 0.50), (374.05, 377.30, "mid", 0.45)]),
    "Short3_Two_Propellers": dict(
        title="WHY DID THIS FIGHTER NEED TWO PROPELLERS?", hook="WHY TWO\nPROPELLERS?", audio="stems",
        pieces=[(204.00, 211.05, "wide", 0.50), (211.05, 222.10, "mid", 0.50),
                (176.50, 193.10, "mid", 0.50), (196.50, 202.00, "tall", 0.50, 19.00)]),
}
CENTER_Y = 975
LAYOUT = {"tall": (864, 1080, 1080, 1350), "mid": (1440, 1080, 1080, 810), "wide": (1920, 1080, 1080, 608)}

def run(cmd): subprocess.run(cmd, check=True)

def render_piece(i, a, b, mode, cx, path, vsrc=None):
    cw, ch, ow, oh = LAYOUT[mode]
    d = b - a
    if vsrc is not None: a = vsrc
    c0, c1 = (cx, cx) if not isinstance(cx, tuple) else cx
    xexp = f"(iw-{cw})*0+min(max(({c0}+({c1}-{c0})*t/{d})*iw-{cw}/2,0),iw-{cw})"
    y0 = CENTER_Y - oh // 2
    fg = (f"[v]crop={cw}:{ch}:'{xexp}':0,scale={ow}:{oh}:flags=lanczos,"
          f"scale=w='{ow}*(1+0.045*t/{d})':h=-2:eval=frame:flags=bicubic,crop={ow}:{oh}[fg]")
    bg = "[w]scale=-2:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.20:saturation=0.6[bg]"
    flt = (f"[0:v]trim=0:{d},setpts=PTS-STARTPTS,fps=30,split[v][w];{fg};{bg};"
           f"[bg][fg]overlay=(W-w)/2:{y0}:shortest=1,format=yuv420p[o]")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{d + 0.2:.3f}", "-i", os.path.join(F13, "master_v.mp4"), "-filter_complex", flt, "-map", "[o]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-an", path])

def whoosh(sr=48000, dur=0.45, seed=0):
    r = np.random.default_rng(seed); n = int(sr * dur)
    x = r.normal(0, 1, n).astype(np.float32)
    # sweep a one-pole low-pass from dark to bright, rise then fall
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    cut = np.linspace(0.02, 0.35, n)
    y = np.zeros(n, np.float32); s = 0.0
    for k in range(n): s += cut[k] * (x[k] - s); y[k] = s
    return y * env / (np.abs(y).max() + 1e-9) * 0.35

def read_wav(p, a, d):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(d), "-i", p, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def build_audio(spec, pieces, path):
    sr = 48000; tot = sum(b - a for a, b, *_ in pieces); N = int(tot * sr) + sr
    out = np.zeros((N, 2), np.float32); t = 0.0; cuts = []
    src = os.path.join(F13, "audio", "mix_master.wav" if spec["audio"] == "mix" else "voice_only.wav")
    for k, (a, b, *_ ) in enumerate(pieces):
        seg = read_wav(src, a, b - a); f = min(len(seg), int(0.03 * sr))
        seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(t * sr); out[i:i + len(seg)] += seg
        if k and abs(a - pieces[k - 1][1]) > 0.05: cuts.append(t)
        t += b - a
    if spec["audio"] != "mix":
        mus = read_wav(os.path.join(F13, "audio", "music_only.wav"), pieces[0][0], tot + 1)
        voice_env = np.convolve(np.abs(out[:, 0]), np.ones(4800) / 4800, "same")
        duck = 1 - 0.55 * np.clip(voice_env / (voice_env.max() * 0.15 + 1e-9), 0, 1)
        m = min(len(mus), len(out)); out[:m] += mus[:m] * 1.4 * duck[:m, None]
    w = whoosh()
    for c in cuts:
        i = int((c - 0.22) * sr); out[i:i + len(w)] += w[:, None] * np.array([0.9, 1.0])
    fade = int(0.6 * sr); out[int(tot * sr) - fade:int(tot * sr)] *= np.linspace(1, 0, fade)[:, None]
    out = out[:int(tot * sr)]
    pre = path + ".pre.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "2", "-i", "-", pre], input=out.tobytes(), check=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", path])
    return tot

def ass_time(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

def build_ass(spec, pieces, tot, path):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Inter Display Black,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,4,3,8,70,70,170,1
Style: Hook,Inter Display Black,118,&H003DA3E8,&H003DA3E8,&H00000000,&HA0000000,0,0,0,0,100,100,2,0,1,7,5,5,60,60,0,1
Style: Cap,Inter Display Black,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,1,0,1,6,3,2,90,90,430,1
Style: CTA,Inter Display Black,46,&H00161 91E,&H00FFFFFF,&H003DA3E8,&H003DA3E8,0,0,0,0,100,100,1,0,3,14,0,8,120,120,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""".replace("&H00161 91E", "&H001E1916")
    ev = []
    title = spec["title"]
    ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(tot)},Title,,0,0,0,,{{\\fad(150,0)}}{title}")
    hook = spec["hook"].replace("\n", "\\N")
    ev.append(f"Dialogue: 3,{ass_time(0)},{ass_time(2.6)},Hook,,0,0,0,,{{\\pos(540,{CENTER_Y})\\fscx60\\fscy60\\t(0,180,\\fscx105\\fscy105)\\t(180,300,\\fscx100\\fscy100)\\fad(0,250)}}{hook}")
    # captions: 2-3 word chunks timed by character share within each sentence
    t0 = 0.0
    for a, b, *_ in pieces:
        for s, sa, sb in SEGS:
            if sb <= a or sa >= b: continue
            sa2, sb2 = max(sa, a), min(sb, b)
            words = s.upper().replace("…", "...").split(); chunks = []
            cur = []
            for w in words:
                cur.append(w)
                if len(cur) == 3 or w.endswith((",", ".", "?", "!", "...")) or len(" ".join(cur)) > 14:
                    chunks.append(" ".join(cur)); cur = []
            if cur: chunks.append(" ".join(cur))
            totc = sum(len(c) for c in chunks); tt = sa2
            for c in chunks:
                dd = (sb2 - sa2) * len(c) / totc
                st, en = t0 + (tt - a), t0 + (tt - a) + dd
                if st > 2.4 or en > 2.6:        # leave the hook alone for its first 2.6 s
                    st = max(st, 2.6 if st < 2.6 else st)
                    ev.append(f"Dialogue: 2,{ass_time(st)},{ass_time(en)},Cap,,0,0,0,,{{\\fad(40,0)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{c}")
                tt += dd
        t0 += b - a
    ev.append(f"Dialogue: 4,{ass_time(tot - 3.2)},{ass_time(tot)},CTA,,0,0,0,,{{\\fad(200,0)}}FULL STORY: TAP THE VIDEO LINK BELOW")
    open(path, "w").write(head + "\n".join(ev) + "\n")

for name, spec in SHORTS.items():
    if os.environ.get("ONLY") and name not in os.environ["ONLY"].split(","): continue
    print("==", name, flush=True)
    pieces = spec["pieces"]; parts = []
    for i, (a, b, mode, cx, *vs) in enumerate(pieces):
        vsrc = vs[0] if vs else None
        key = f"{a}_{b}_{mode}_{cx}_{vsrc}".replace(" ", "").replace("(", "").replace(")", "").replace(",", "-")
        p = os.path.join(TMP, f"{name}_{i:02d}_{key}.mp4")
        if not (os.path.exists(p) and os.path.getsize(p) > 0): render_piece(i, a, b, mode, cx, p, vsrc)
        parts.append(p)
    lst = os.path.join(TMP, f"{name}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    vid = os.path.join(TMP, f"{name}_v.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    aud = os.path.join(TMP, f"{name}.wav"); tot = build_audio(spec, pieces, aud)
    ass = os.path.join(TMP, f"{name}.ass"); build_ass(spec, pieces, tot, ass)
    run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-filter_complex",
         f"[0:v]subtitles='{ass}':fontsdir={FONTS},fade=t=out:st={tot - 0.5}:d=0.5[v]", "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "16M", "-bufsize", "32M", "-profile:v", "high",
         "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
         os.path.join(OUT, f"Pogo_{name}.mp4")])
    print("   ", round(tot, 1), "s", flush=True)
