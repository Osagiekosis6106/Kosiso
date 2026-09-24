# How to download free archival images and films (Mac)

`archival_fetch.py` searches the Library of Congress and the Prelinger Archives and downloads the results straight to your Mac. It also fills in a `sourcing-log.csv` for you.

## One-time setup (5 minutes)

1. Download `archival_fetch.py` from this repo (on GitHub, open the file and click **Download raw file**). It will land in your **Downloads** folder.
2. Open **Terminal**: press ⌘ + Space, type `Terminal`, press Enter.
3. Type this and press Enter:
   ```
   python3 --version
   ```
   If a box pops up asking to install **command line developer tools**, click **Install** and wait. You only do this once.

## Every time you need footage

Open Terminal, then paste one line at a time:

```
cd ~/Downloads
python3 archival_fetch.py "steel mill"
```

Your images appear in **Downloads → archival → steel-mill**, next to `sourcing-log.csv`.

## Recipes

| You need | Paste this |
|---|---|
| Black & white 1930s–40s photos (safest, all public domain) | `python3 archival_fetch.py "factory workers"` |
| Colour 1940s photos | `python3 archival_fetch.py "main street" --source fsa-color` |
| Any era of Library of Congress photo (checks rights one by one) | `python3 archival_fetch.py "Detroit factory" --source loc --count 15` |
| Moving film clips (assembly lines, 1950s kitchens, old ads) | `python3 archival_fetch.py "assembly line" --source prelinger --count 5` |
| Just see the links, no download | add `--list-only` |
| Record which beat it's for | add `--beat 14` |

## Search tips

- Use **short, simple words**: `steel mill`, `kitchen`, `department store`, `textile mill`, `coal town`, `diner`.
- FSA photos cover 1935–1944, so modern brand names won't match there. Use `--source loc` for company names like `Studebaker` or `Ford plant`.
- Prelinger films are long. Download one, then trim the 3–5 seconds you need in CapCut.
- Films bigger than 400 MB are skipped. Add `--max-mb 1000` to allow bigger ones.
