"""Builds the YouTube subtitle file (SRT) from the script text + the voiceover word timings.
Usage: python3 make_srt.py STT_DIR OUT.srt"""
import sys, json, re, difflib
import build12 as B

STT, OUT = sys.argv[1], sys.argv[2]
md = open(B.os.path.join(B.HERE, "..", "convair-pogo.md")).read()
script = md.split("## FINAL SCRIPT (v8")[1].split("\n", 1)[1].split("\n### History")[0]
p3_text = script[script.index("And remember the rival"):script.index("subscribe to Hangar Physics.") + len("subscribe to Hangar Physics.")]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.?!…])\s+(?=[A-Z\"“])", " ".join(text.split())) if s.strip()]

def align_words(sents, words):
    """sentence start/end from the recognised words (difflib on normalised tokens)"""
    toks, owner = [], []
    for i, s in enumerate(sents):
        for w in s.replace("—", " ").replace("-", " ").split():
            if norm(w): toks.append(norm(w)); owner.append(i)
    rec = [norm(w[0]) for w in words]
    hit = {}
    for a, b, n in difflib.SequenceMatcher(None, toks, rec, autojunk=False).get_matching_blocks():
        for k in range(n): hit.setdefault(owner[a + k], []).append(words[b + k])
    out = []
    for i, s in enumerate(sents):
        h = hit.get(i)
        out.append([s, h[0][1], h[-1][2]] if h else [s, None, None])
    for i, x in enumerate(out):            # fill gaps from neighbours
        if x[1] is None:
            x[1] = out[i - 1][2] + 0.1; x[2] = next(y[1] for y in out[i + 1:] if y[1] is not None) - 0.1
    return out

al = json.load(open(f"{STT}/align.json"))
p3 = align_words(sentences(p3_text), json.load(open(f"{STT}/p3.json")))
segs = []
for s, a, b, *_ in al["p1"]:
    off = B.VO_A_OFF if a < B.VO_A_END else B.VO_B_OFF
    segs.append([s, a + off, b + off])
segs += [[s, a + B.VO_C_OFF, b + B.VO_C_OFF] for s, a, b, *_ in al["p2"]]
segs += [[s, a + B.VO_D_OFF, b + B.VO_D_OFF] for s, a, b in p3]
for i in range(len(segs) - 1):          # minimum readable duration, never overlapping the next line
    segs[i][2] = min(max(segs[i][2], segs[i][1] + 1.0), segs[i + 1][1] - 0.04)

def chunks(text, a, b, maxc=84):
    """split a long sentence into caption cards of <= 2 lines x 42 chars, timed by character share"""
    words, cards, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc and cur: cards.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    cards.append(cur)
    tot = sum(len(c) for c in cards); t = a; res = []
    for c in cards:
        d = (b - a) * len(c) / tot; res.append((c, t, t + d)); t += d
    return res

def wrap(c, n=42):
    if len(c) <= n: return c
    mid = len(c) // 2; sp = min((i for i, ch in enumerate(c) if ch == " "), key=lambda i: abs(i - mid))
    return c[:sp] + "\n" + c[sp + 1:]

ts = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}"
n = 0
with open(OUT, "w") as f:
    for s, a, b in segs:
        for c, x, y in chunks(s, a, b):
            n += 1; f.write(f"{n}\n{ts(x)} --> {ts(y)}\n{wrap(c)}\n\n")
print(n, "captions; last ends", ts(segs[-1][2]))
