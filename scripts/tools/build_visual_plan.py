"""Build the beat-by-beat visual plan, shopping list and sourcing log.

Usage:
  python3 build_visual_plan.py SCRIPT.md SHOTS.txt OUT_PLAN.md OUT_LOG.md "Video title"

SHOTS.txt has one line per beat: n|mode|scene|action|camera|light|mood|search
(see scripts/data/one-paycheck-shots.txt). Beats are cut by split_beats.py.
"""
import collections, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent

MODES = {
    "F": ("🎞️ ARCHIVAL FILM", "real"),
    "P": ("📷 ARCHIVAL PHOTO", "real"),
    "S": ("🎬 MODERN STOCK", "real"),
    "G": ("🔢 GRAPHIC", "graphic"),
    "B": ("🎨 AI IMAGE · B&W era photo", "ai"),
    "C": ("🎨 AI IMAGE · 1960s Kodachrome", "ai"),
    "R": ("🎨 AI IMAGE · cinematic recreation", "ai"),
}
CAMERA = {
    "WS": "wide establishing shot at eye level", "MS": "medium shot at eye level",
    "CU": "close-up detail shot", "OTS": "over-the-shoulder shot from behind, faces not visible",
    "LOW": "low angle looking up", "HIGH": "high angle looking down",
    "TOP": "locked-off top-down flat lay", "AER": "high aerial view",
    "BACK": "shot from behind as the subject moves away, face not visible",
}
LIGHT = {
    "DAWN": "cool blue dawn light with a warm glow on the horizon", "DAY": "soft natural daylight",
    "DUSK": "warm golden-hour light", "NIGHT": "night, pools of warm practical light",
    "TUNG": "warm tungsten interior light", "FLUOR": "flat overhead fluorescent light",
    "WIN": "soft window light with gentle falloff", "OVC": "flat overcast light",
    "FIRE": "hard orange firelight glow against deep shadow",
    "BOOTH": "darkness cut by a bright projector beam", "FLASH": "on-camera press flash",
    "": "flat even studio light",
}
MOOD = {
    "NOS": "warm nostalgic", "PRIDE": "proud and dignified", "QUIET": "quiet and reflective",
    "GRIEF": "melancholy", "COLD": "cold, clinical, ominous",
    "TENSE": "tense and uneasy", "HOPE": "hopeful", "STARK": "stark, empty, abandoned",
    "": "clean and informative",
}
SOURCE = {
    "fsa": ("Library of Congress · FSA/OWI (1935–44)", "loc.gov/pictures/collection/fsa"),
    "fsa-color": ("Library of Congress · FSA/OWI colour", "loc.gov/pictures/collection/fsac"),
    "loc": ("Library of Congress (loc.gov/free-to-use)", "loc.gov/photos"),
    "prelinger": ("Prelinger Archives (archive.org/details/prelinger)", "archive.org/details/prelinger"),
    "nara": ("National Archives (catalog.archives.gov)", "catalog.archives.gov"),
    "nypl": ("NYPL Digital Collections (public domain only)", "digitalcollections.nypl.org"),
    "wiki": ("Wikimedia Commons (check each licence)", "commons.wikimedia.org"),
    "pexels": ("Pexels (free licence)", "pexels.com/videos"),
    "pixabay": ("Pixabay (free licence)", "pixabay.com/videos"),
}
LICENCE = {
    "fsa": ("Public domain · no known restrictions", "Optional: Library of Congress, Prints & Photographs Division, FSA/OWI"),
    "fsa-color": ("Public domain · no known restrictions", "Optional: Library of Congress, Prints & Photographs Division, FSA/OWI"),
    "loc": ("Check the item's Rights line (the fetch tool checks it)", "Optional: Library of Congress"),
    "prelinger": ("Public domain", "No"),
    "nara": ("Public domain (US federal government)", "Optional: U.S. National Archives"),
    "nypl": ("Public domain (ticked filter)", "Optional: NYPL"),
    "wiki": ("Check the file page — PD or CC", "Yes if CC BY"),
    "pexels": ("Pexels licence", "No"),
    "pixabay": ("Pixabay licence", "No"),
}
FETCHABLE = {"fsa", "fsa-color", "loc", "prelinger"}

BW = ("{era} black and white documentary photograph, {scene}, {action}, {camera}, {light}, "
      "{mood} mood, high contrast with deep blacks and bright silvers, heavy film grain, slight softness, "
      "35mm Kodak Tri-X, candid, no text, no logos, no readable signs")
KODA = ("{era} Kodachrome colour photograph, {scene}, {action}, {camera}, {light}, {mood} mood, "
        "faded warm colours, muted saturation, film grain, candid family snapshot feel, "
        "no text, no logos, no readable signs")
CINE = ("photorealistic cinematic film still, {era} America, {scene}, {action}, {camera}, {light}, "
        "{mood} mood, muted period colour grade with walnut browns, navy and beige, 35mm lens, "
        "faces turned away or not visible, fine film grain, no text, no logos")
TODAY = ("present-day documentary photograph, {scene}, {action}, {camera}, {light}, {mood} mood, "
         "muted colours, natural texture, no text, no logos, no readable signs")
BOARD = ("top-down flat lay of a vintage graph-paper board, faint grey grid lines, subtle paper texture, "
         "dust specks and a light vignette, soft even light, generous empty space for text, clean and "
         "informative mood, no text, no logos")

def split_era(scene, default):
    m = re.match(r"^((?:19|20)\d0s|(?:19|20)\d\d):\s*(.*)$", scene)
    return (m.group(1), m.group(2)) if m else (default, scene)

def prompt_for(mode, scene, action, cam, light, mood):
    kw = dict(action=action, camera=CAMERA[cam], light=LIGHT[light], mood=MOOD[mood])
    if mode == "B":
        era, s = split_era(scene, "1960s"); return BW.format(era=era, scene=s, **kw)
    if mode == "C":
        era, s = split_era(scene, "1960s"); return KODA.format(era=era, scene=s, **kw)
    if mode == "R":
        era, s = split_era(scene, "1970s"); return CINE.format(era=era, scene=s, **kw)
    if mode == "S":
        return TODAY.format(scene=scene, **kw)
    if mode in "FP":  # fallback for archival beats
        era, s = split_era(scene, "1950s"); return BW.format(era=era, scene=s, **kw)
    return BOARD

def parse_search(s):
    out = []
    for part in filter(None, s.split(";")):
        src, terms = part.split(":", 1)
        out.append((src.strip(), terms.strip()))
    return out

def fetch_cmd(src, terms, beats):
    count = min(10, max(3, len(beats) + 2)) if src != "prelinger" else min(4, len(beats) + 1)
    s = "" if src == "fsa" else f" --source {src}"
    return f'python3 archival_fetch.py "{terms}"{s} --count {count} --beat {",".join(map(str, beats))}'

def main(script, shots_path, out_plan, out_log, title):
    beats = json.loads(subprocess.check_output([sys.executable, str(HERE / "split_beats.py"), script]))
    shots = {}
    for line in open(shots_path, encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        f = line.rstrip("\n").split("|")
        f += [""] * (8 - len(f))
        shots[int(f[0])] = dict(mode=f[1], scene=f[2], action=f[3], cam=f[4] or "TOP",
                                light=f[5], mood=f[6], search=parse_search(f[7]))
    missing = [b["n"] for b in beats if b["n"] not in shots]
    extra = [n for n in shots if n > len(beats)]
    if missing or extra:
        sys.exit(f"shot list mismatch: missing {missing[:20]} extra {extra[:20]}")

    # checks: max 3 AI in a row; real beats have a search
    run, problems = 0, []
    for b in beats:
        m = shots[b["n"]]["mode"]
        run = run + 1 if MODES[m][1] == "ai" else 0
        if run > 3:
            problems.append(f"beat {b['n']}: 4+ AI beats in a row")
        if MODES[m][1] == "real" and not shots[b["n"]]["search"]:
            problems.append(f"beat {b['n']}: real beat without a search")
    if problems:
        sys.exit("\n".join(problems))

    cnt = collections.Counter(shots[b["n"]]["mode"] for b in beats)
    total = len(beats)
    real = cnt["F"] + cnt["P"] + cnt["S"]
    ai = cnt["B"] + cnt["C"] + cnt["R"]
    secs = sum(b["sec"] for b in beats)
    pct = lambda n: round(100 * n / total)

    L = [f"# Visual Plan — {title}", "",
         "Generated from the locked script and the Visual Style Profile (STATE 7). "
         "Every beat is 3–5 s max and every image prompt is fully standalone.", "",
         "## Part A — Mix check", "", "```",
         f"Beats: {total} (~{int(secs // 60)} min {int(secs % 60)} s) | 🎞️ film {cnt['F']} | 📷 photo {cnt['P']} | "
         f"🎬 stock {cnt['S']} | 🔢 graphic {cnt['G']} | 🎨 AI {ai} (B&W {cnt['B']}, Kodachrome {cnt['C']}, recreation {cnt['R']})",
         f"Real share: {pct(real)}% {'✅' if pct(real) >= 35 else '⚠️'} (target ≥35%, mix A) | "
         f"AI share: {pct(ai)}% {'✅' if pct(ai) <= 50 else '⚠️'} (target ≤50%) | Graphics: {pct(cnt['G'])}%",
         "Max AI beats in a row: 3 ✅", "```", "",
         "**Finish on every shot:** film grain + dust/scratches, light vignette, occasional orange light leak, "
         "slow Ken Burns push on stills, big semi-transparent entry number (#25…#1) on screen for the whole entry.", "",
         "**Upload reminder:** this video contains realistic AI images → tick YouTube's "
         "**\"altered or synthetic content\" = Yes**.", "",
         "## Part B — Beat list", ""]

    section = None
    for b in beats:
        s = shots[b["n"]]
        if b["section"] != section:
            section = b["section"]
            L += [f"### {section.title().replace('Entry ', 'Entry #')}", ""]
        tag = MODES[s["mode"]][0]
        L.append(f"#### Beat {b['n']} (~{max(2, round(b['sec']))}s) — {tag}")
        L.append(f"**Script:** \"{b['text']}\"  ")
        prompt = prompt_for(s["mode"], s["scene"], s["action"], s["cam"], s["light"], s["mood"])
        if s["mode"] == "G":
            L.append(f"**Build in CapCut:** {s['scene']}. Animation: {s['action']}. Labels in white "
                     "rounded sans ALL CAPS, photos with 2 px dashed #6B6450 border.  ")
            L.append(f"**Background image prompt:** {prompt}  ")
        elif MODES[s["mode"]][1] == "real":
            (src, terms), *rest = s["search"]
            L.append(f"**Get it:** {SOURCE[src][0]} → search `{terms}`  ")
            fb = " · ".join(f"{SOURCE[r][0]} → `{t}`" for r, t in rest)
            L.append(f"**Fallback:** {fb + ' · or ' if fb else ''}the AI prompt below  ")
            L.append(f"**Use:** {split_era(s['scene'], '')[1]}; {s['action']}.  ")
            L.append(f"**Fallback AI prompt:** {prompt}  ")
        else:
            L.append(f"**Image prompt:** {prompt}  ")
        L.append(f"**Camera:** {CAMERA[s['cam']]} · **Lighting:** {LIGHT[s['light']]} · "
                 f"**Mood:** {MOOD[s['mood']]} · **Action:** {s['action']}")
        L.append("")

    # Part C — shopping list grouped by source, then by search terms
    groups = collections.defaultdict(lambda: collections.defaultdict(list))
    for b in beats:
        s = shots[b["n"]]
        if MODES[s["mode"]][1] == "real":
            src, terms = s["search"][0]
            groups[src][terms].append(b["n"])
    L += ["## Part C — Free-footage shopping list", "",
          "Download everything from one site in one sitting. Commands go in Terminal from your "
          "Downloads folder (see `archival-fetch-guide.md`); the tool also writes `sourcing-log.csv` for you.", ""]
    order = ["fsa", "fsa-color", "loc", "prelinger", "nara", "nypl", "wiki", "pexels", "pixabay"]
    for src in order:
        if src not in groups:
            continue
        n = sum(len(v) for v in groups[src].values())
        L += [f"### {SOURCE[src][0]} — {n} beats", ""]
        for terms, bs in groups[src].items():
            L.append(f"- Beat {', '.join(map(str, bs))}: search `{terms}`")
        if src in FETCHABLE:
            L += ["", "```"] + [fetch_cmd(src, t, bs) for t, bs in groups[src].items()] + ["```"]
        L.append("")
    L += [f"### AI to generate: {ai} images",
          f"- {cnt['B']} black & white era photos, {cnt['C']} Kodachrome colour, {cnt['R']} cinematic recreations "
          "(prompts in Part B). Motion prompts come in STATE 9.",
          f"- {cnt['G']} graphic boards to build in CapCut.", ""]
    Path(out_plan).write_text("\n".join(L), encoding="utf-8")

    # sourcing log
    R = [f"# Sourcing Log — {title}", "",
         "One row per real photo, film clip or stock clip. Paste the exact item link into column 4 as you "
         "download (the fetch tool's `sourcing-log.csv` already has links for LOC and Prelinger downloads). "
         "Keep this file: it wins Content ID disputes in minutes.", "",
         "| Beat | What it shows | Source site | Exact link | Licence / status | Credit needed? |",
         "|---|---|---|---|---|---|"]
    for b in beats:
        s = shots[b["n"]]
        if MODES[s["mode"]][1] == "real":
            src, terms = s["search"][0]
            lic, credit = LICENCE[src]
            R.append(f"| {b['n']} | {split_era(s['scene'], '')[1]} | {SOURCE[src][0]} (`{terms}`) | ← paste | {lic} | {credit} |")
    R += ["", "## AI-generated visuals in this video",
          f"- Count: {ai} images ({cnt['B']} B&W, {cnt['C']} colour, {cnt['R']} recreations), motion: see STATE 9",
          "- YouTube \"altered or synthetic content\" box ticked: ☐ Yes", "",
          "## Description credit line (paste into the YouTube description)",
          "> Archival images courtesy of the Library of Congress (FSA/OWI collection), the U.S. National Archives "
          "and the Prelinger Archives (Internet Archive). Stock footage from Pexels. Some scenes are AI-generated "
          "illustrations.", ""]
    Path(out_log).write_text("\n".join(R), encoding="utf-8")
    print(json.dumps(dict(beats=total, secs=round(secs), counts=cnt, real=pct(real), ai=pct(ai),
                          graphic=pct(cnt["G"])), default=dict))

if __name__ == "__main__":
    main(*sys.argv[1:6])
