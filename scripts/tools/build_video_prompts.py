"""Build image-to-video prompts for every beat of a visual plan.

Usage:
  python3 build_video_prompts.py SCRIPT.md SHOTS.txt OUT.md "Video title"

Reads the same inputs as build_visual_plan.py. AI beats get an image-to-video prompt;
archival and stock beats get editor motion plus a fallback video prompt; graphics get
CapCut animation notes.
"""
import collections, json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_visual_plan import MODES, CAMERA, LIGHT, MOOD, prompt_for, split_era, parse_search  # noqa: E402

HERE = Path(__file__).parent

MOVE = {
    "WS": "very slow push-in", "MS": "very slow push-in", "CU": "gentle slow drift sideways",
    "OTS": "slow dolly forward over the shoulder", "LOW": "slow tilt up", "HIGH": "slow tilt down",
    "TOP": "static top-down with a slight slide", "AER": "slow aerial glide forward",
    "BACK": "camera holds still while the subject moves away",
}
KEN_BURNS = {
    "WS": "slow push-in 100% → 110%", "MS": "slow push-in 100% → 108%", "CU": "slow pan left to right at 110%",
    "OTS": "slow push-in 100% → 110%", "LOW": "slow pan bottom to top at 115%", "HIGH": "slow pan top to bottom at 115%",
    "TOP": "slow push-in 100% → 105%", "AER": "slow pan left to right at 110%", "BACK": "slow push-in 100% → 108%",
}
FINISH = {
    "B": "black and white, heavy film grain, subtle projector flicker",
    "C": "faded Kodachrome colour, film grain",
    "R": "cinematic, muted period colour grade, fine film grain",
    "S": "muted natural colour",
    "F": "black and white, heavy film grain, subtle projector flicker",
    "P": "black and white, heavy film grain, subtle projector flicker",
}
SAFE = "minimal motion, no morphing, no warping, keep faces and hands stable, no text appearing, 24 fps"

def secs(b):
    return max(3, min(5, round(b["sec"] + 0.4)))

def video_prompt(mode, s, n):
    motion = s["action"]
    return (f"{MOVE[s['cam']]}, {motion}, {LIGHT[s['light']]} stays consistent, "
            f"{MOOD[s['mood']]} mood, {FINISH[mode]}, {SAFE}, {n} seconds")

def main(script, shots_path, out, title):
    beats = json.loads(subprocess.check_output([sys.executable, str(HERE / "split_beats.py"), script]))
    shots = {}
    for line in open(shots_path, encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            f = line.rstrip("\n").split("|"); f += [""] * (8 - len(f))
            shots[int(f[0])] = dict(mode=f[1], scene=f[2], action=f[3], cam=f[4] or "TOP",
                                    light=f[5], mood=f[6], search=parse_search(f[7]))

    # priority: the hook's AI beats plus the first AI beat of every section
    priority, seen = set(), set()
    for b in beats:
        m = shots[b["n"]]["mode"]
        if MODES[m][1] == "ai" and (b["section"] == "HOOK" or b["section"] not in seen):
            priority.add(b["n"]); seen.add(b["section"])

    cnt = collections.Counter(MODES[shots[b["n"]]["mode"]][1] for b in beats)
    L = [f"# Video Prompts — {title}", "",
         "One motion instruction for every beat. Match each to the image with the same beat number in "
         "`one-paycheck-visual-plan.md`.", "",
         "## How to use", "",
         f"- **🎨 AI beats ({cnt['ai']}):** generate the still first, then paste the video prompt into "
         "Kling / Veo / Runway **image-to-video**. Generate 5 s and trim to the beat length in CapCut.",
         f"- **⭐ Animate first ({len(priority)} beats):** the hook and the first AI shot of each entry. "
         "They carry the most weight. Other AI beats can stay as stills with a Ken Burns push if you run low on credits.",
         f"- **🎞️📷🎬 Real beats ({cnt['real']}):** no AI needed. Use the real clip, or add the Ken Burns move in CapCut. "
         "The fallback video prompt is only for when the search finds nothing.",
         f"- **🔢 Graphics ({cnt['graphic']}):** animate in CapCut as described (keyframes, 0.3 s ease-in).",
         "- **Every clip:** keep motion slow. Morphing faces and hands are what make AI look fake to this audience.", ""]
    section = None
    for b in beats:
        s = shots[b["n"]]; m = s["mode"]; n = secs(b)
        if b["section"] != section:
            section = b["section"]
            L += [f"## {section.title().replace('Entry ', 'Entry #')}", ""]
        star = " ⭐" if b["n"] in priority else ""
        L.append(f"**Beat {b['n']} (~{n}s) — {MODES[m][0]}{star}**  ")
        L.append(f"Script: \"{b['text']}\"  ")
        if MODES[m][1] == "ai":
            L.append(f"🎥 Video prompt (image-to-video): {video_prompt(m, s, n)}")
        elif m == "G":
            L.append(f"🔢 CapCut animation: {s['action']}; slow 5% push-in on the board, 0.3 s ease-in on each element, "
                     "light dust overlay, hold the final frame")
        elif m == "F":
            L.append(f"🎞️ Editor: trim the best {n} s of the real clip ({s['action']}); keep it 4:3 pillarboxed, add grain + scratches.  ")
            L.append(f"Fallback video prompt: {video_prompt(m, s, n)}")
        else:  # P or S
            L.append(f"{'📷' if m == 'P' else '🎬'} Editor: Ken Burns {KEN_BURNS[s['cam']]} over {n} s.  ")
            L.append(f"Fallback video prompt: {video_prompt(m, s, n)}")
        L.append("")
    Path(out).write_text("\n".join(L), encoding="utf-8")
    print(json.dumps(dict(beats=len(beats), priority=len(priority), **cnt)))

if __name__ == "__main__":
    main(*sys.argv[1:5])
