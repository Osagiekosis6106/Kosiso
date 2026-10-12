"""Soundtrack for Parts 1 + 2: processed voiceover + original synthesised score + sound design, ducked and
mastered to YouTube loudness (-14 LUFS integrated, -1.5 dBTP). Usage: python3 audio12.py OUTDIR"""
import sys, os, subprocess, json, math
import numpy as np
import build12 as B

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
VO = [os.path.join(HERE, "audio", f"VO_part{i}.mp3") for i in (1, 2)]
N = int(B.END * SR) + SR
rng = np.random.default_rng(3)

def load(path, extra=""):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-af", extra or "anull", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

VOICE_CHAIN = ("highpass=f=75,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=2.5,"
               "equalizer=f=10000:t=q:w=1:g=1.5,deesser=i=0.35,"
               "acompressor=threshold=0.09:ratio=2.5:attack=8:release=120:makeup=1.5")

def mhz(m): return 440.0 * 2 ** ((m - 69) / 12)
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}
def nm(s):   # "D3" -> midi
    n, o = (s[:-1], int(s[-1])); return 12 * (o + 1) + NOTE[n]
CH = {"Dm": ["D3", "A3", "D4", "F4", "A4"], "Dm9": ["D3", "A3", "E4", "F4", "A4"], "Bb": ["Bb2", "F3", "Bb3", "D4", "F4"],
      "Gm": ["G2", "D3", "G3", "Bb3", "D4"], "A": ["A2", "E3", "A3", "C#4", "E4"], "C": ["C3", "G3", "C4", "E4", "G4"],
      "F": ["F2", "C3", "F3", "A3", "C4"], "Eb": ["Eb3", "Bb3", "Eb4", "G4", "Bb4"], "Asus": ["A2", "E3", "A3", "D4", "E4"]}

def env_adsr(n, a, r):
    e = np.ones(n, dtype=np.float32); ai = min(n, int(a * SR)); ri = min(n, int(r * SR))
    if ai: e[:ai] = np.linspace(0, 1, ai) ** 2
    if ri: e[-ri:] *= np.linspace(1, 0, ri) ** 1.5
    return e

def add(buf, t0, sig):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if j > i: buf[i:j] += sig[: j - i]

def pad_note(f, dur, a=1.6, r=2.2, bright=8):
    n = int((dur + r) * SR); t = np.arange(n) / SR; s = np.zeros(n, dtype=np.float32)
    for det in (-0.004, 0.0, 0.005):
        ff = f * (1 + det); ph = rng.uniform(0, 6.28)
        for h in range(1, bright + 1):
            if ff * h > 6000: break
            s += np.sin(2 * np.pi * ff * h * t + ph * h).astype(np.float32) / (h ** 1.15)
    s *= env_adsr(n, a, r) * (1 + 0.08 * np.sin(2 * np.pi * 0.17 * t)).astype(np.float32)
    return s / 6.0

def pluck(f, dur=1.2, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * bright * np.sin(2 * np.pi * 2 * f * t) + 0.12 * bright * np.sin(2 * np.pi * 3 * f * t))
    return (s * np.exp(-t * 4.2) * np.minimum(1, t * 400)).astype(np.float32)

def thump(dur=0.5, f0=70, f1=40, k=9):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * k)).astype(np.float32)

def boom(dur=3.5):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 28 + 40 * np.exp(-t * 6); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 1.4)
    nz = rng.standard_normal(n) * np.exp(-t * 7) * 0.5
    return (s + lowpass(nz, 900)).astype(np.float32)

def lowpass(x, fc, order=2):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (fr / fc) ** (2 * order)); return np.fft.irfft(X, len(x)).astype(np.float32)

def bandpass(x, lo, hi):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / np.sqrt(1 + (fr / hi) ** 4)) * (1 / np.sqrt(1 + (lo / np.maximum(fr, 1)) ** 4)); return np.fft.irfft(X, len(x)).astype(np.float32)

def riser(dur=2.6):
    n = int(dur * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n).astype(np.float32)
    out = np.zeros(n, dtype=np.float32); seg = SR // 10
    for i in range(0, n, seg):
        k = i / n; out[i:i + seg] = bandpass(nz[i:i + seg], 300 + 3000 * k, 800 + 7000 * k)
    sw = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * 0.25
    return ((out + sw) * (t / dur) ** 2.2).astype(np.float32)

def whoosh(dur=0.45):
    n = int(dur * SR); t = np.arange(n) / SR
    s = bandpass(rng.standard_normal(n).astype(np.float32), 400, 3500)
    return (s * np.sin(np.pi * t / dur) ** 2).astype(np.float32)

def click(dur=0.03, lo=1500, hi=6000):
    n = int(dur * SR); t = np.arange(n) / SR
    return (bandpass(rng.standard_normal(n).astype(np.float32), lo, hi) * np.exp(-t * 180)).astype(np.float32)

def keyclack():
    a = click(0.035, 1200, 5000); b = thump(0.06, 180, 120, 60) * 0.4
    m = np.zeros(max(len(a), len(b)), dtype=np.float32); m[:len(a)] += a; m[:len(b)] += b; return m

def shutter():
    s = np.zeros(int(0.18 * SR), dtype=np.float32)
    s[:len(click(0.03, 800, 6000))] += click(0.03, 800, 6000)
    c2 = click(0.04, 600, 4000); s[int(0.07 * SR):int(0.07 * SR) + len(c2)] += c2 * 0.8
    return s

def prop_roar(dur):
    """Turboprop: two contra-rotating 3-blade props (blade-pass ~ 80 Hz, slight beat) + turbine whine + air noise."""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n, dtype=np.float32)
    for fb, ph in ((79.0, 0.0), (81.5, 1.3)):
        for h in range(1, 14):
            s += (np.sin(2 * np.pi * fb * h * t + ph * h) / h ** 1.05).astype(np.float32)
    s *= (1 + 0.15 * np.sin(2 * np.pi * 2.5 * t)).astype(np.float32)
    nz = lowpass(rng.standard_normal(n).astype(np.float32), 1100) * 2.2
    whine = (0.06 * np.sin(2 * np.pi * (2650 + 15 * np.sin(2 * np.pi * 0.3 * t)) * t)).astype(np.float32)
    return lowpass(s * 0.18 + nz * 0.5, 2500) + whine

def reverb(x, secs=2.8, wet=0.3):
    n = int(secs * SR); t = np.arange(n) / SR
    ir = rng.standard_normal(n).astype(np.float32) * np.exp(-t * 6.5 / secs)
    ir = lowpass(ir, 4500); ir /= np.sqrt(np.sum(ir ** 2))
    Lb = 1 << 20; nf = 1 << (Lb + n - 1).bit_length(); IR = np.fft.rfft(ir, nf)
    y = np.zeros(len(x) + nf, dtype=np.float32)
    for i in range(0, len(x), Lb):
        blk = np.fft.irfft(np.fft.rfft(x[i:i + Lb], nf) * IR, nf).astype(np.float32)
        y[i:i + nf] += blk
    return x * (1 - wet) + y[: len(x)] * wet * 1.6

# ---------------------------------------------------------------- score
def score():
    pads = np.zeros(N, dtype=np.float32); arp = np.zeros(N, dtype=np.float32); low = np.zeros(N, dtype=np.float32)
    perc = np.zeros(N, dtype=np.float32); fx = np.zeros(N, dtype=np.float32)
    g1, g2 = B.g1, B.g2
    def prog(t0, t1, chords, bar, gain=1.0, bright=7):
        t = t0; i = 0
        while t < t1 - 0.5:
            d = min(bar, t1 - t)
            for m in CH[chords[i % len(chords)]]:
                add(pads, t, pad_note(mhz(nm(m)), d, a=min(1.6, d * 0.4), r=2.2, bright=bright) * gain)
            t += bar; i += 1
    def arpeggio(t0, t1, chords, bar, bpm, gain=1.0, octave=12, bright=1.0):
        step = 60 / bpm / 2; t = t0; i = 0
        while t < t1:
            ch = CH[chords[int((t - t0) // bar) % len(chords)]]
            notes = [nm(m) + octave for m in ch[1:]]
            pat = [0, 1, 2, 3, 2, 1, 3, 2]
            add(arp, t, pluck(mhz(notes[pat[i % 8] % len(notes)]), 1.2, bright) * gain * (1.0 if i % 2 == 0 else 0.7))
            t += step; i += 1
    def heartbeat(t0, t1, bpm0, bpm1, gain=1.0):
        t = t0
        while t < t1:
            k = (t - t0) / max(1e-6, t1 - t0); bpm = bpm0 + (bpm1 - bpm0) * k
            add(perc, t, thump(0.45, 75, 42, 10) * gain); add(perc, t + 0.22, thump(0.4, 68, 40, 12) * gain * 0.65)
            t += 60 / bpm
    def ticks(t0, t1, bpm, gain=1.0):
        t = t0; i = 0
        while t < t1:
            add(perc, t, click(0.02, 3000, 9000) * gain * (1.0 if i % 4 == 0 else 0.5)); t += 60 / bpm / 2; i += 1
    def drone(t0, t1, gain=1.0, f=mhz(nm("D2"))):
        n = int((t1 - t0) * SR); t = np.arange(n) / SR
        s = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f / 2 * t) + 0.25 * np.sin(2 * np.pi * f * 1.5 * t)) * env_adsr(n, 2.5, 3.0)
        add(low, t0, (s * gain).astype(np.float32))

    # cold open + tension
    drone(0.0, 46.0, 0.9)
    prog(4.0, 44.9, ["Dm9", "Dm9", "Bb", "Dm9"], 10.0, 0.55, 5)
    heartbeat(9.0, 42.8, 66, 80, 0.55)
    add(fx, 44.95 - 2.6, riser(2.6) * 0.5)
    add(fx, 44.95, boom(4.0) * 1.0)
    prog(44.95, 48.6, ["Dm"], 4.0, 1.0, 9)
    # questions / one problem
    t_sea = g1(59.8); t_req = g1(92.5); t_tech = g1(130.4)
    prog(48.4, t_sea, ["Dm", "Bb", "Gm", "A"], 4.0, 0.55, 6)
    drone(48.4, t_sea + 1, 0.4, mhz(nm("A1")))
    # WWII history: low march pulse
    prog(t_sea, t_req, ["Dm", "C", "Bb", "A"], 5.0, 0.5, 6)
    t = t_sea + 0.5
    while t < t_req - 1:
        add(perc, t, thump(0.5, 95, 55, 9) * 0.35); t += 60 / 84
    # requirement / the catch
    prog(t_req, t_tech, ["Gm", "Dm", "Bb", "Asus", "A"], 6.0, 0.5, 6)
    ticks(g1(113.8), t_tech, 80, 0.25)
    drone(g1(113.8), t_tech + 1, 0.45)
    # design + physics: arpeggio drive
    t_end1 = B.VO_C_OFF - 1.5
    prog(t_tech, t_end1 + 1.0, ["Dm", "Bb", "F", "C"], 5.0, 0.42, 6)
    arpeggio(t_tech + 0.2, t_end1 - 0.5, ["Dm", "Bb", "F", "C"], 5.0, 96, 0.30)
    ticks(g1(152.2), t_end1 - 0.5, 96, 0.22)
    heartbeat(g1(172.1), t_end1 - 0.5, 72, 88, 0.35)
    add(fx, t_end1 - 1.5, riser(1.6) * 0.3)
    add(fx, B.VO_C_OFF - 0.1, boom(3.0) * 0.55)
    # Part 2: hangar mystery
    t_col = g2(29.0); t_fly = g2(52.75); t_land = g2(72.2); t_nov = g2(137.8); t_tail = g2(160.0)
    prog(B.VO_C_OFF - 1.5, t_col, ["Gm", "Dm", "Eb", "Dm"], 6.0, 0.48, 6)
    for k, tt in enumerate(np.arange(B.VO_C_OFF + 1, t_col - 1, 3.0)):
        add(arp, tt, pluck(mhz(nm(["D5", "A4", "F5", "E5"][k % 4])), 2.0, 0.6) * 0.22)
    # Coleman
    prog(t_col, t_fly, ["F", "C", "Dm", "Bb"], 6.0, 0.5, 6)
    # free flight
    prog(t_fly, t_land, ["F", "C", "Bb", "F"], 5.0, 0.45, 7)
    arpeggio(t_fly + 0.1, t_land - 0.3, ["F", "C", "Bb", "F"], 5.0, 104, 0.30, 12, 1.2)
    # landing tension
    prog(t_land, t_nov, ["Dm9", "Bb", "Dm9", "Gm"], 8.0, 0.45, 5)
    drone(t_land, t_nov + 1, 0.8)
    heartbeat(t_land + 1.5, t_nov - 1.0, 70, 104, 0.6)
    ticks(g2(98.4), t_nov - 1.0, 104, 0.25)
    add(fx, t_nov - 2.6, riser(2.6) * 0.5)
    add(fx, t_nov, boom(4.0) * 0.9)
    # triumph
    prog(t_nov, t_tail + 1, ["F", "C", "Dm", "Bb"], 5.5, 0.6, 9)
    arpeggio(t_nov + 0.3, t_tail, ["F", "C", "Dm", "Bb"], 5.5, 100, 0.32, 12, 1.3)
    # resolve
    prog(t_tail, B.END, ["Bb", "Dm9"], 4.0, 0.5, 6)
    drone(t_tail, B.END, 0.5)
    bed = reverb(pads * 0.5 + arp * 0.9, 3.2, 0.38) + lowpass(low, 220) * 0.6 + reverb(perc, 1.6, 0.2) * 0.9
    # level the bed so every section sits at a similar loudness (hits in fx stay on top)
    hop = SR // 10; w = 30
    r = np.sqrt(np.convolve(bed[::hop] ** 2 if False else (bed ** 2)[::hop], np.ones(w) / w, "same")) + 1e-5
    target = np.median(r[r > np.percentile(r, 20)])
    g = np.clip(target / r, 0.35, 2.0)
    g = np.convolve(g, np.ones(20) / 20, "same")
    bed = bed * np.interp(np.arange(len(bed)) / hop, np.arange(len(g)), g).astype(np.float32)
    return bed + reverb(fx, 2.5, 0.3) * 0.9

# ---------------------------------------------------------------- sound design
def sfx():
    s = np.zeros(N, dtype=np.float32)
    S = B.build_timeline()
    starts = [t for t, _ in S] + [B.END]
    flying = {"D_lowangle_hanging.mp4": 0.9, "A_hover_high.mp4": 0.8, "B_descent_touchdown.mp4": 0.8, "C_hover_descent2.mp4": 0.8,
              "G_takeoff1.mp4": 1.0, "H_takeoff2.mp4": 1.0, "F_standing_wide.mp4": 0.35, "I_cameraman.mp4": 0.45, "E_on_ground_crew.mp4": 0.25}
    for i, (t0, shot) in enumerate(S):
        t1 = starts[i + 1]
        name = getattr(shot, "name", None)
        if name in flying:
            d = t1 - t0 + 0.4; r = prop_roar(d) * env_adsr(int(d * SR), 0.25, 0.4) * flying[name]
            add(s, t0 - 0.1, r * 0.55)
        if type(shot).__name__ == "Gfx" and t0 > 3:
            add(s, t0 - 0.2, whoosh(0.45) * 0.35)
    # cold open: engine fades up under the typewriter, peaks at the cut to film
    d = 4.6; r = prop_roar(d) * (np.linspace(0, 1, int(d * SR)) ** 2.0); add(s, 0.0, r * 0.75)
    # typewriter keys
    for k in range(len("NOVEMBER 1954")): add(s, 0.35 + 0.1 * k, keyclack() * 0.5)
    for t0, t_off, text in ((B.g1(100.05), 0.2, "1951"), (B.g2(7.5), 0.2, "SPRING 1954"), (B.g2(52.75), 0.1, "1 AUGUST 1954"), (B.g2(137.8), 0.1, "2 NOVEMBER 1954")):
        for k in range(len(text)): add(s, t0 + t_off + 0.09 * k, keyclack() * 0.45)
    add(s, B.g2(85.8) + 1.2, shutter() * 0.9)
    for t in (B.g1(31.7) + 3.95, B.g1(25.7) + 4.9, B.g2(142.6) + 7.0, B.g1(197.55) + 13.6):
        add(s, t, thump(0.5, 120, 60, 10) * 0.6)
    add(s, B.g1(25.7) + 1.5, boom(1.5) * 0.6)
    add(s, B.g2(115.65) + 1.6, boom(1.5) * 0.5)
    return s

# ---------------------------------------------------------------- mix
def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    p1 = load(VO[0], VOICE_CHAIN); p2 = load(VO[1], VOICE_CHAIN)
    voice = np.zeros(N, dtype=np.float32)
    cut = int(B.VO_A_END * SR)
    add(voice, B.VO_A_OFF, p1[:cut]); add(voice, B.VO_B_OFF + B.VO_A_END, p1[cut:]); add(voice, B.VO_C_OFF, p2)
    # duck envelope from the voice (attack 60 ms, release 500 ms)
    hop = SR // 100
    rms = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, "same"))[::hop]
    act = (rms > 0.012).astype(np.float32)
    envd = np.zeros_like(act); v = 0.0
    for i, a in enumerate(act):
        v = v + (a - v) * (0.35 if a > v else 0.02); envd[i] = v
    duck = np.interp(np.arange(N) / hop, np.arange(len(envd)), envd).astype(np.float32)
    music = score(); fxs = sfx()
    mg = 1.0 - 0.65 * duck            # about -9 dB more under speech
    fg = 1.0 - 0.5 * duck
    voice_lvl = 1.0 / max(1e-6, np.percentile(np.abs(voice[voice != 0]), 99.5))
    mix = voice * voice_lvl * 0.5 + music * mg * 0.5 + fxs * fg * 0.26
    # music/fx widened with a 12 ms offset between channels; voice stays centred
    side = music * mg * 0.5 + fxs * fg * 0.26; vc = voice * voice_lvl * 0.5
    dl = int(0.012 * SR); sideR = np.concatenate([np.zeros(dl, dtype=np.float32), side[:-dl]])
    stereo = np.stack([vc + side, vc + sideR], 1)[: int(B.END * SR)]
    pre = os.path.join(out, "mix_pre.wav")
    pcm = np.clip(stereo, -1, 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", pre], input=pcm.astype(np.float32).tobytes(), check=True)
    # two-pass loudnorm to YouTube's -14 LUFS / -1.5 dBTP
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", af, "-ar", "48000", os.path.join(out, "mix_master.wav")], check=True)
    # stems for reference
    for nm_, sig in (("music_only", music * 0.5), ("voice_only", voice * voice_lvl * 0.5)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", os.path.join(out, nm_ + ".wav")],
                       input=np.clip(sig[: int(B.END * SR)], -1, 1).astype(np.float32).tobytes(), check=True)
    print("measured", m["input_i"], "LUFS ->", "-14 target")

if __name__ == "__main__":
    main()
