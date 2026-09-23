#!/usr/bin/env python3
"""Download free archival images and film clips for "america memory" videos.

Sources:
  fsa        Library of Congress FSA/OWI black-and-white photos, 1935-44 (all public domain)
  fsa-color  Library of Congress FSA/OWI colour photos, 1939-44 (all public domain)
  loc        Every Library of Congress photo (rights checked one by one)
  prelinger  Prelinger Archives film on the Internet Archive (moving footage)

Examples:
  python3 archival_fetch.py "steel mill"
  python3 archival_fetch.py "assembly line" --source prelinger --count 5
  python3 archival_fetch.py "department store" --source loc --count 15 --beat 22

Files land in ~/Downloads/archival/<search words>/ and every download is
added to sourcing-log.csv in that folder. Standard library only; no installs.
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (archival_fetch for personal documentary research)"

LOC_COLLECTIONS = {
    "fsa": "https://www.loc.gov/collections/fsa-owi-black-and-white-negatives/",
    "fsa-color": "https://www.loc.gov/collections/fsa-owi-color-photographs/",
    "loc": "https://www.loc.gov/photos/",
}

# Prelinger video formats, best first. The 512Kb derivative is small but soft.
PRELINGER_FORMATS = ["h.264", "MPEG4", "h.264 IA", "512Kb MPEG4"]


def get_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except Exception as error:
            if attempt == 2:
                raise
            print(f"  retrying after error: {error}")
            time.sleep(2 * (attempt + 1))


def download(url, destination):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response, open(destination, "wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)


def safe_name(text, limit=60):
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")[:limit] or "untitled"


def first(value):
    return value[0] if isinstance(value, list) and value else value


def loc_rights(item_url):
    """Return the rights statement from a Library of Congress item page."""
    try:
        data = get_json(item_url.rstrip("/") + "/?fo=json")
    except Exception:
        return ""
    item = data.get("item", {})
    rights = item.get("rights_advisory") or item.get("rights") or ""
    return " ".join(rights) if isinstance(rights, list) else str(rights)


def search_loc(query, source, count):
    base = LOC_COLLECTIONS[source]
    params = {"q": query, "fo": "json", "c": min(max(count * 3, 25), 150), "at": "results"}
    if source == "loc":
        params["fa"] = "online-format:image"
    data = get_json(base + "?" + urllib.parse.urlencode(params))

    results = []
    for entry in data.get("results", []):
        images = [u for u in entry.get("image_url", []) if u]
        if not images:
            continue
        item_url = entry.get("url") or entry.get("id") or ""
        if source == "loc":
            rights = loc_rights(item_url)
            if "no known restrictions" not in rights.lower():
                continue
        else:
            rights = "Public domain (FSA/OWI, U.S. government work)"
        results.append({
            "title": first(entry.get("title")) or "untitled",
            "date": first(entry.get("date")) or "",
            "page": item_url,
            # image_url runs small to large; the last one is the biggest.
            "file_url": images[-1].split("#")[0],
            "ext": ".jpg",
            "rights": rights.strip(),
        })
        if len(results) >= count:
            break
    return results


def search_prelinger(query, count, max_mb):
    params = [("q", f"collection:prelinger AND ({query})"), ("rows", count * 3), ("output", "json")]
    params += [("fl[]", field) for field in ("identifier", "title", "year")]
    data = get_json("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params))

    results = []
    for doc in data.get("response", {}).get("docs", []):
        identifier = doc["identifier"]
        files = get_json(f"https://archive.org/metadata/{identifier}").get("files", [])
        chosen = None
        for wanted in PRELINGER_FORMATS:
            chosen = next((f for f in files if f.get("format") == wanted), None)
            if chosen and int(chosen.get("size", 0)) <= max_mb * 1024 * 1024:
                break
            chosen = None
        if not chosen:
            continue
        results.append({
            "title": first(doc.get("title")) or identifier,
            "date": str(first(doc.get("year")) or ""),
            "page": f"https://archive.org/details/{identifier}",
            "file_url": f"https://archive.org/download/{identifier}/{urllib.parse.quote(chosen['name'])}",
            "ext": Path(chosen["name"]).suffix or ".mp4",
            "size_mb": round(int(chosen.get("size", 0)) / 1048576),
            "rights": "Prelinger Archives: public domain / free to reuse",
        })
        if len(results) >= count:
            break
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help='search words, e.g. "steel mill" or "kitchen 1950s"')
    parser.add_argument("--source", choices=["fsa", "fsa-color", "loc", "prelinger"], default="fsa")
    parser.add_argument("--count", type=int, default=10, help="how many files to download (default 10)")
    parser.add_argument("--beat", default="", help="beat number(s) from your visual plan, saved in the log")
    parser.add_argument("--max-mb", type=int, default=400, help="skip Prelinger films bigger than this (default 400)")
    parser.add_argument("--list-only", action="store_true", help="show links without downloading")
    parser.add_argument("--out", default=str(Path.home() / "Downloads" / "archival"))
    args = parser.parse_args()

    print(f"Searching {args.source} for '{args.query}'...")
    if args.source == "prelinger":
        results = search_prelinger(args.query, args.count, args.max_mb)
    else:
        results = search_loc(args.query, args.source, args.count)
    if not results:
        print("Nothing found. Try shorter or different words (e.g. 'factory' instead of 'factory workers 1941').")
        return 1

    folder = Path(args.out) / safe_name(args.query)
    folder.mkdir(parents=True, exist_ok=True)
    log_path = folder / "sourcing-log.csv"
    new_log = not log_path.exists()

    with open(log_path, "a", newline="") as log_file:
        log = csv.writer(log_file)
        if new_log:
            log.writerow(["beat", "file", "what it shows", "date", "source", "link", "licence / status"])
        for number, result in enumerate(results, 1):
            name = f"{args.source}-{number:02d}-{safe_name(result['title'], 40)}{result['ext']}"
            size = f" ({result['size_mb']} MB)" if "size_mb" in result else ""
            print(f"[{number}/{len(results)}] {result['title'][:70]}{size}\n    {result['page']}")
            if args.list_only:
                continue
            target = folder / name
            if not target.exists():
                try:
                    download(result["file_url"], target)
                except Exception as error:
                    print(f"    download failed: {error}")
                    continue
            log.writerow([args.beat, name, result["title"], result["date"], args.source,
                          result["page"], result["rights"]])

    if not args.list_only:
        print(f"\nDone. Files and sourcing-log.csv are in: {folder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
