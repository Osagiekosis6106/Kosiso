"""Build image-prompts.md and sourcing-log.md from the beat data in beats_*.py.

Every beat carries: exact script text, one tag (america-memory.md rules), a free
source + search words for real-footage beats, and a standalone image prompt
(the primary prompt for AI/graphic beats, the fallback for real-footage beats).
Run: python3 render.py
"""
import importlib, glob, re
from collections import OrderedDict

WPS = 2.75

ANCHOR = {
    "A": "Style: 1950s-60s black and white documentary photograph, candid newspaper-photographer look, 35mm lens, soft focus, lifted blacks, heavy film grain, dust specks, one faint vertical scratch, aged silver-gelatin print, faces small or turned away, no text, no logos.",
    "B": "Style: degraded 16mm black and white industrial film frame, 4:3 aspect, slight blur and gate weave, milky blown highlights, thin vertical scratch line, visible film-frame edge, grain and flicker, no text, no logos.",
    "C": "Style: 1970s-80s 35mm colour film still, faded warm colours, tobacco-brown and navy palette, soft focus, visible grain, muted skin tones, candid framing, faces turned away, no text, no logos.",
    "D": "Style: single vintage object as a clean cut-out, centered, shot straight-on in soft even light, on a warm grey aged graph-paper background with thin grid lines, faint white chalk doodle lines and dust specks, empty space above for labels, no text, no logos.",
    "E": "Style: black and white mid-century photograph with a purple-and-green halftone dot moire overlay, retro print texture, thin vertical scratch line, soft grain, faces turned away, no text, no logos.",
    "F": "Style: present-day documentary photograph, slightly desaturated muted colours, empty and quiet, natural detail, no people or one distant figure, no text, no logos.",
}
MODE_NAME = {"A": "B&W era photo", "B": "archival film frame", "C": "faded 70s-80s colour",
             "D": "grid-paper cut-out", "E": "halftone portrait", "F": "present day"}

TAGS = OrderedDict([
    ("FILM", ("🎞️ ARCHIVAL FILM", "prelinger", "B")),
    ("PHOTO", ("📷 ARCHIVAL PHOTO", "loc", "A")),
    ("AD", ("📰 ARCHIVAL AD", "loc", "D")),
    ("STOCK", ("🎬 MODERN STOCK", "pexels", "F")),
    ("GFX", ("🔢 GRAPHIC", None, "D")),
    ("AI", ("🎨 AI IMAGE", None, "A")),
])
REAL = {"FILM", "PHOTO", "AD", "STOCK"}

SOURCES = {
    "fsa": ("Library of Congress: FSA/OWI 1935-44 (loc.gov/free-to-use)", "fsa"),
    "fsa-color": ("Library of Congress: FSA/OWI colour (loc.gov/free-to-use)", "fsa-color"),
    "loc": ("Library of Congress (loc.gov/pictures)", "loc"),
    "prelinger": ("Prelinger Archives (archive.org/details/prelinger)", "prelinger"),
    "nara": ("National Archives (catalog.archives.gov)", None),
    "documerica": ("National Archives: DOCUMERICA 1971-77 (catalog.archives.gov)", None),
    "smithsonian": ("Smithsonian Open Access, CC0 only (si.edu/openaccess)", None),
    "wikimedia": ("Wikimedia Commons, check each licence (commons.wikimedia.org)", None),
    "nypl": ("NYPL Digital Collections, public domain only (digitalcollections.nypl.org)", None),
    "pexels": ("Pexels / Pixabay (free licence)", None),
    "archive": ("Internet Archive texts, pre-1931 pages only (archive.org)", None),
}
LICENCE = {
    "fsa": "Public domain", "fsa-color": "Public domain", "loc": "Check 'Rights' line: needs 'No known restrictions'",
    "prelinger": "Public domain", "nara": "Public domain (US government)", "documerica": "Public domain (US government)",
    "smithsonian": "CC0", "wikimedia": "Check file licence; credit if CC BY", "nypl": "Public domain",
    "pexels": "Pexels / Pixabay licence", "archive": "Public domain if pre-1931",
}

BEATS = []

def b(text, tag, q, scene, cam, light, mood, action, src=None, mode=None, gfx=None, overlay=None):
    label, default_src, default_mode = TAGS[tag]
    BEATS.append(dict(text=text, tag=tag, q=q, scene=scene, cam=cam, light=light, mood=mood,
                      action=action, src=src or default_src, mode=mode or default_mode,
                      gfx=gfx, overlay=overlay))

def prompt(x):
    return (f"{x['scene']}. Camera: {x['cam']}. Lighting: {x['light']}. Mood: {x['mood']}. "
            f"{ANCHOR[x['mode']]}")

def main():
    global BEATS
    import render
    for f in sorted(glob.glob("beats_*.py")):
        importlib.import_module(f[:-3])
    BEATS = render.BEATS
    # integrity: beats must reproduce the script word for word
    src = [l.strip() for l in open("script.md", encoding="utf-8")]
    src = " ".join(l for l in src if l and not l.startswith("# ") and not re.fullmatch(r"\[.+\]", l))
    got = " ".join(x["text"] for x in BEATS)
    sw, gw = src.split(), got.split()
    if sw != gw:
        i = next((k for k, (p, q) in enumerate(zip(sw, gw)) if p != q), min(len(sw), len(gw)))
        raise SystemExit(f"Script mismatch at word {i}: script={' '.join(sw[i-5:i+8])!r} beats={' '.join(gw[i-5:i+8])!r}")
    for i, x in enumerate(BEATS, 1):
        n = len(x["text"].split())
        assert n <= 14, f"beat {i} too long ({n} words)"
        assert (x["q"] is not None) == (x["tag"] in REAL), f"beat {i}: real beats need search words, others none"
        if x["tag"] == "GFX":
            assert x["gfx"], f"beat {i}: graphic needs build notes"
    # no more than 3 AI beats in a row
    run = 0
    for i, x in enumerate(BEATS, 1):
        run = run + 1 if x["tag"] == "AI" else 0
        assert run <= 3, f"beat {i}: more than 3 AI beats in a row"

    total = len(BEATS)
    count = {t: sum(x["tag"] == t for x in BEATS) for t in TAGS}
    real = sum(count[t] for t in REAL)
    secs = sum(len(x["text"].split()) / WPS for x in BEATS)

    out = []
    out.append("# Image Prompts: 25 One-Paycheck Jobs That Could Buy a House in 1960s America (Now Gone Forever)\n")
    out.append(f"Script: `script.md` (locked, word for word). {total} beats, about {secs/60:.0f} min at {WPS} words/s, each beat 3-5 s or shorter.\n")
    out.append("## Part A: Mix check\n```")
    out.append(f"Beats: {total} | 🎞️ film {count['FILM']} | 📷 photo {count['PHOTO']} | 📰 ad {count['AD']} | "
               f"🎬 stock {count['STOCK']} | 🔢 graphic {count['GFX']} | 🎨 AI {count['AI']}")
    rs, ai = 100 * real / total, 100 * count["AI"] / total
    out.append(f"Real share: {rs:.0f}% {'✅' if rs >= 55 else '⚠️'} (target ≥55%) | AI share: {ai:.0f}% {'✅' if ai <= 25 else '⚠️'} (target ≤25%)")
    out.append("```\n")
    out.append("**How to read each beat.** Every beat has a standalone image prompt. On 🎞️ 📷 📰 🎬 beats, download the real footage first and use the prompt only if the search finds nothing. On 🎨 and 🔢 beats, the prompt is the visual. Brand names, dates and numbers go on as CapCut text, never inside an AI image. If any AI image looks like a real historical photo, tick YouTube's **\"altered or synthetic content\" = Yes**.\n")
    out.append("**Style modes** (from the Visual Style Profile): " + " · ".join(f"{k} = {v}" for k, v in MODE_NAME.items()) + ".\n")
    out.append("## Part B: Beat list\n")
    section = None
    heads = [l.strip()[1:-1] for l in open("script.md", encoding="utf-8") if re.fullmatch(r"\[.+\]", l.strip())]
    # attach section headers: a section starts at each "Number N." / pattern break / outro opener
    starts = {}
    si = 0
    for i, x in enumerate(BEATS):
        t = x["text"]
        if i == 0 or t.startswith("Number ") and re.match(r"Number \d+\. The ", t) or t.startswith(("First pattern break", "Second pattern break", "Third pattern break", "So here is what I want you to do")):
            starts[i] = heads[si]; si += 1
    assert si == len(heads), f"found {si} section starts, script has {len(heads)}"
    for i, x in enumerate(BEATS):
        if i in starts:
            out.append(f"\n---\n\n## {starts[i].title()}\n")
        n = i + 1
        label = TAGS[x["tag"]][0]
        dur = max(1, round(len(x["text"].split()) / WPS))
        out.append(f"### Beat {n} (~{dur}s) — {label}")
        out.append(f"**Script:** \"{x['text']}\"  ")
        if x["tag"] in REAL:
            site = SOURCES[x["src"]][0]
            out.append(f"**Get it:** {site} → search `{x['q']}`  ")
        if x["gfx"]:
            out.append(f"**Build in CapCut:** {x['gfx']}  ")
        lab = "Fallback image prompt" if x["tag"] in REAL else "Image prompt"
        out.append(f"**{lab} ({MODE_NAME[x['mode']]}):** {prompt(x)}  ")
        out.append(f"**Camera angle:** {x['cam']} · **Lighting:** {x['light']} · **Mood:** {x['mood']} · **Action:** {x['action']}  ")
        if x["overlay"]:
            out.append(f"**Overlay:** {x['overlay']}  ")
        out.append("")

    # Part C: shopping list grouped by source, then search words
    out.append("\n---\n\n## Part C: Free-footage shopping list\n")
    out.append("Download everything from one site in one sitting. The commands use `archival_fetch.py` (see `archival-fetch-guide.md`); run them from the folder where the script is saved.\n")
    groups = OrderedDict()
    for i, x in enumerate(BEATS, 1):
        if x["tag"] in REAL:
            groups.setdefault(x["src"], OrderedDict()).setdefault(x["q"], []).append(i)
    order = ["loc", "fsa", "fsa-color", "prelinger", "nara", "documerica", "smithsonian", "nypl", "wikimedia", "archive", "pexels"]
    for s in order:
        if s not in groups:
            continue
        g = groups[s]
        n = sum(len(v) for v in g.values())
        out.append(f"### {SOURCES[s][0]}: {n} beats\n")
        for q, ids in g.items():
            out.append(f"- Beat {', '.join(map(str, ids))}: search `{q}`")
        flag = SOURCES[s][1]
        if flag:
            out.append("\n```")
            for q, ids in g.items():
                cnt = max(3, min(15, len(ids) * 2)) if flag != "prelinger" else max(2, min(5, len(ids)))
                extra = "" if flag == "fsa" else f" --source {flag}"
                out.append(f"python3 archival_fetch.py \"{q}\"{extra} --count {cnt} --beat {','.join(map(str, ids))}")
            out.append("```")
        out.append("")
    ai_n = count["AI"]
    gfx_n = count["GFX"]
    out.append(f"### AI to generate: {ai_n} images (prompts above)\n")
    out.append(f"### Graphics to build in CapCut: {gfx_n}\n")
    open("image-prompts.md", "w", encoding="utf-8").write("\n".join(out) + "\n")

    # sourcing log
    log = ["# Sourcing Log: 25 One-Paycheck Jobs That Could Buy a House in 1960s America\n",
           "One row per real photo, film clip or stock clip. Paste the exact link when you download it (`archival_fetch.py` writes it to `sourcing-log.csv` for Library of Congress and Prelinger files). Keep this file: it wins Content ID disputes in minutes.\n",
           "| Beat | What it shows | Source site | Search used | Exact link | Licence / status | Credit needed? |",
           "|---|---|---|---|---|---|---|"]
    for i, x in enumerate(BEATS, 1):
        if x["tag"] in REAL:
            credit = {"loc": "Optional: \"Library of Congress, Prints & Photographs Division\"",
                      "fsa": "Optional: \"Library of Congress, FSA/OWI\"", "fsa-color": "Optional: \"Library of Congress, FSA/OWI\"",
                      "wikimedia": "Yes if CC BY: author + licence"}.get(x["src"], "No")
            what = x["scene"].split(",")[0]
            log.append(f"| {i} | {what} | {SOURCES[x['src']][0].split(' (')[0]} | `{x['q']}` | _paste link_ | {LICENCE[x['src']]} | {credit} |")
    log += ["", "## AI-generated visuals in this video",
            f"- Count: {ai_n} images (plus fallback prompts for any real beat where the search found nothing), __ with motion",
            "- YouTube \"altered or synthetic content\" box ticked: ☐ Yes", "",
            "## Description credit line (paste into the YouTube description)",
            "> Archival images courtesy of the Library of Congress, the U.S. National Archives and the Prelinger Archives (Internet Archive). Some scenes are AI-generated illustrations."]
    open("sourcing-log.md", "w", encoding="utf-8").write("\n".join(log) + "\n")
    print(f"{total} beats | film {count['FILM']} photo {count['PHOTO']} ad {count['AD']} stock {count['STOCK']} gfx {count['GFX']} ai {count['AI']} | real {rs:.0f}% ai {ai:.0f}% | {secs/60:.1f} min")

if __name__ == "__main__":
    main()
