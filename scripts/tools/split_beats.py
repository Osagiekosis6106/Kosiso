"""Split a script into beats of 3-5 seconds (<=12 spoken words at ~2.4 words/sec).

Usage: python3 split_beats.py script.md > beats.json
Clauses (split at sentence ends and commas) are packed greedily up to 12 words;
a clause longer than 12 words is cut before a natural break word near its middle.
"""
import json, re, sys

MAX = 12
BREAK_WORDS = {"and", "but", "with", "to", "that", "who", "which", "in", "of", "for",
               "on", "from", "until", "because", "so", "while", "where", "when", "after",
               "into", "at", "then", "or", "by", "as"}

def clauses(par):
    out = []
    for s in re.split(r'(?<=[.!?])\s+', par.strip()):
        out += [c for c in re.split(r'(?<=[,:;])\s+', s) if c]
    return out

def cut_long(words):
    if len(words) <= MAX:
        return [words]
    n = len(words)
    target = n // 2 if n <= 2 * MAX else MAX
    lo, hi = max(4, n - MAX) if n <= 2 * MAX else 4, min(MAX, n - 4)
    best = None
    for i in range(lo, hi + 1):
        if words[i].lower().strip(",.") in BREAK_WORDS:
            if best is None or abs(i - target) < abs(best - target):
                best = i
    i = best if best is not None else min(MAX, max(lo, target))
    return [words[:i]] + cut_long(words[i:])

def main(path):
    section, beats = None, []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[(HOOK|ENTRY \d+|FIRST PATTERN BREAK|SECOND PATTERN BREAK|THIRD PATTERN BREAK|OUTRO)\]$", line)
        if m:
            section = m.group(1); continue
        if line.startswith("["):
            continue
        pieces = []
        for c in clauses(line):
            pieces += cut_long(c.split())
        packed = []
        for p in pieces:
            if packed and len(packed[-1]) + len(p) <= MAX:
                packed[-1] = packed[-1] + p
            else:
                packed.append(p)
        for p in packed:
            beats.append({"n": len(beats) + 1, "section": section, "text": " ".join(p),
                          "words": len(p), "sec": round(len(p) / 2.4, 1)})
    json.dump(beats, sys.stdout, indent=0, ensure_ascii=False)

if __name__ == "__main__":
    main(sys.argv[1])
