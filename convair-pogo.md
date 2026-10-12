# Convair Pogo: Hangar Physics video #2 (project memory)

Trigger phrase: **"convair pogo"**. In a new chat, say "convair pogo" and Claude reads this file (plus the three airspeed files) and continues from **Status** below.

---

## Status (update this every step)

| Step | What | State |
|---|---|---|
| 1 | Topic, title, hook and description chosen with VidIQ and NexLev | ✅ done (8 Oct 2026) |
| 2 | Full script written and fact-checked | ✅ **FINAL v8 CONFIRMED by the user (9 Oct)** |
| 3 | Grok prompt pack (references R#, masters M#, lock text, shot table, fallbacks, upload list) | ✅ v1 sent 9 Oct, **waiting for the user's OK** |
| 4 | Archival sourcing, one source at a time | 🔄 #1 NARA 428-NPC-1597 ✅ (11 shots A–J saved in `pogo-film/footage/`); #2 = the user searches catalog.archives.gov (`XFY-1`, `Pogo Stick`, `vertical takeoff fighter 1954`, `Coleman Convair`, Moving images) and sends screenshots, looking for Coleman, the tip-over into level flight, and the tethered hangar hover |
| 5 | Voiceover: the user records Parts 1–3 separately and sends them | ✅ all 3 parts received and checked 10 Oct (total 9:08.6) |
| 6 | Claude builds what it can locally (graphics, spec cards, X-ray diagrams, timing sheet / edit list) | 🔄 preview 1 (plain blueprint) sent; user unsure. **Preview 2 (v2 look) built 10 Oct** `pogo-film/pogo_graphics_preview_2.mp4` via `scenes2.py`: real film + blueprint overlays, grid, glow, grain, light vignette, camera push, callout labels. Scenes: S01 typewriter → real shot D; S34 real shot F plays, freezes, zooms 2×, X-ray sight lines over the real Pogo; S33 blueprint pitch-up with step dots and thrust/weight. **User approved the v2 look (10 Oct): use it for every graphic.** Every photo/film the user sends gets used for Ken Burns moves, freeze-zoom X-ray overlays, split screens, callouts and traced outlines. Shots that were AI-direct (S14 cargo ship, S45 storm at sea, S51 drone) become free stock footage (Pexels/Pixabay, user downloads) or a blueprint illustration labelled ILLUSTRATION |
| 7 | Package: thumbnails, pinned comment, Shorts, upload | ⏳ |

Deadline: **upload this weekend** (10–11 Oct 2026). Don't publish on a Wednesday (Airspeed's day).

---


## Production workflow the user asked for (9 Oct 2026)

1. Prompts one by one (like the Goblin video), **skipping Grok wherever possible**.
2. Then the full step list.
3. Then **sources one at a time**: Claude sends each source (link + search terms), the user downloads it and sends the file, Claude confirms it matches the script line, and then moves to the next.
4. Claude **builds the full video** (graphics, X-ray, Ken Burns motion, timing to the voiceover, assembly with ffmpeg) from what the user sends.
Open questions to the user: B-58 example (not in the repo), how files will be sent to Claude, and Option A (no Grok) vs Option B (hybrid).


## Visual style = the B-58 film (no Grok), reviewed 9 Oct 2026

The user's B-58 film (11:39, made with Claude in another session, no Grok) uses: archival photos and film with slow Ken Burns moves and small uppercase lower-third labels; a typewriter date opener; steel-blue (#6FA3C8) and amber (#E8A33D) blueprint-style vector diagrams of the aircraft on graphite (#16191E); comparison cards (54 FT vs CITY BUS); animated maps/radar sweeps; timelines; a trophy icon; cut-out objects on a gradient labelled ILLUSTRATION; a red record stamp; a Hangar Physics end screen ("Every strange aircraft is the answer to a problem." + WATCH NEXT + SUBSCRIBE). The B-58 build scripts are not in this repo, so rebuild the same style in `pogo-film/`.
Pogo upgrades planned: much more real moving film (the 1954 Pogo flights were filmed); an animated vector Pogo that rotates from level flight to vertical (the shot Grok can't do); an animated pilot's sight-line cone; counter-rotating propeller discs with torque arrows; thrust-vs-weight arrows; three pulsing altimeter lights (no colours or numbers); a Pogo ✓ vs XFV-1 ✗ split screen; free stock footage for the storm at sea; propeller sound design. Deliver in 1080p.


## Saved files in the repo (so a new chat can use them)

Everything is in `pogo-film/` on branch `claude/convair-pogo`:
- `footage/raw/nara1597_p1–p6.mov`: the National Archives film 428-NPC-1597 exactly as the user sent it, in 6 pieces (P1–P3 Regulus only; P4–P6 Pogo, cameraman, F3D jets). Public domain; credit "U.S. Navy film, National Archives (428-NPC-1597)".
- `footage/shots/A–J*.mp4`: the usable shots, already cut (see source #1 in the Sources log for what each one shows and which script line it's for).
- `nara_pogo_shots.png`: preview image of shots A–E.
- `audio/VO_part1–3.mp3`: the approved ElevenLabs voiceover (Dan), 9:08.6 in total.
- `reference/B58_full_film_style_reference.mp4`: the user's B-58 film, the style to copy.
- `gfx.py`, `scenes.py`: the graphics code; `pogo_graphics_preview_1.mp4`: graphics preview 1 (waiting for the user's OK on the look).
- The final script (v8), the description, tags, the prompt pack and the fact-check table are further down in this file.

## Sources log (step 4, one at a time)

Licence rules found 9 Oct: San Diego Air & Space Museum (SDASM) films and YouTube uploads say "Please do not use without permission" / no commercial use without permission, so they're **not usable on a monetised channel without written OK from archives@sdasm.org** (credit "San Diego Air & Space Museum"). SDASM *Flickr Commons* photos marked "No known copyright restrictions" are fine. British Movietone and Pathé = licensed (AP Archive), so avoid. US Navy / NARA film = public domain. CriticalPast = US government footage, but its free previews are watermarked (buy the clip or get the NARA original).

| # | Source | For shots | State |
|---|---|---|---|
| VO1 | `Convair_Part_1.mp3` (ElevenLabs, Dan): 3:37.6, 44.1 kHz mono 128 kbps, -24.7 LUFS (normalise in mix), peak -2.8 dBTP, ~143 wpm; rough offline transcript matches the script, every line present | narration Part 1 | ✅ approved 10 Oct |
| VO2 | `Convair_part_2.mp3`: 2:43.1, -24.5 LUFS, peak -2.3 dBTP; transcript matches, all lines present | narration Part 2 | ✅ approved 10 Oct |
| VO3 | `Convair_part_3.mp3`: 2:47.9, -24.5 LUFS, peak -2.1 dBTP; transcript matches, all lines present | narration Part 3 | ✅ approved 10 Oct |
| 1 | **NARA 428-NPC-1597** (U.S. Navy film, public domain; credit "U.S. Navy film, National Archives (428-NPC-1597)"). The user sends it in pieces (720×480, 60 fps). P1 0:59 + P2 1:10 + P3 1:04 = Regulus I on its launcher, USS Hancock, launch smoke, deck crew (not used). P4 1:10: 0:00–0:37 deck crew in smoke, film flare, slate "Pac. Fleet Combat Camera Group / Giles KR / Regulus / Oct 19" (not used); **Pogo shots from 0:37**: A 0:37.2–0:43.9 hovering high over land; B 0:43.9–0:50.0 slow tail-first descent toward the ground; C 0:50.1–0:57.3 second hover and descent; D 0:57.4–1:00.5 low angle looking up, hanging on its propellers (hero shot); E 1:00.9–end standing on its tail on the ramp, gantry, trucks, crew. Cut to `scratchpad/footage/shots/A–E.mp4`. Use: D → S01/S02; B → S03/S05/S06; A, C → S24, S26, S35, S37, S39; E → S22/S30. Note: the shot list says "on deck" but E is on land; don't call it a ship. No date on the Pogo shots, so don't label them "November 1954". P5 1:27 (overlaps the end of P4): E2 0:05.4–0:26.1 longer crew/trucks prep around the standing Pogo; F 0:26.4–0:41.7 standing alone, wide lakebed-type concrete; **G 0:41.8–1:02.9 vertical takeoff and climb** (jeep and cart pass in front); **H 1:05.0–1:24.2 second vertical takeoff and climb**; I 1:24.2–P6 0:06.7 Navy cameraman on a tripod, Pogo in background. P6 1:17: Regulus launch (slate "Regulus Oct 19, roll 5"), then **J 0:36.5–1:07.7 F3D Skyknight jets on a carrier deck** (usable for S47 "1950s Navy jets"), End of Recording. Use G/H → S26, S31 (no date or place label). **Not in this film:** tethered hover in the hangar (S28), transition to level flight (S32/S39), Coleman (S29/S40). | ✅ all 6 pieces checked 10 Oct; 11 shots cut (A–J) |
| 2 | NARA search by the user (10 Oct), 5 images. **Kept:** DoD Office of Public Information newsreel release No. 38-54, "Navy unveils experimental vertical take-off planes", hold until 6 PM EST Wed 17 March 1954, 250 ft of official Navy footage of the Lockheed XFV-1 and Convair XFY-1, "under construction for a period of nearly three years", "rotatable seat arrangement" (US government, public domain) → `pogo-film/photos/DoD_newsreel_release_38-54_17Mar1954.jpg`, for S15/S16 as an on-screen document. Don't quote its "turbo-jet engines" line (they were turboprops). **Not used:** pressure tanks, tunnel sting with a man, instrument panel, wind-tunnel interior: nothing in them shows they are Pogo, and no script line needs them. The film record is NARA NAID 102045749, Local ID 111-DD-38-54 (RG 111 Chief Signal Officer, series "Filmed News Releases"), but only the 2-page release sheet is digitised: no video online (would need a NARA reproduction order). | ✅ 1 of 5 kept |
| 3 | Wikimedia Commons search by the user (11–12 Oct), 16 images. Saved to `pogo-film/photos/pending/` until the licence is confirmed: P01 Pogo **tethered inside the hangar** (S28!), P02 on its launching cart (Commons "XFY-1 on launching cart2 NAN5-54.jpg", USN, **public domain ✓**, need original file, have screenshot only), P04 pilot in helmet beside the Pogo (Commons "Convair XFY Pogo, Richie.jpg", R. Y. Richie, **no known copyright restrictions ✓**, need original; pilot not named in caption, so label "Convair test pilot" unless confirmed as Coleman), P05 hovering over buildings, P10 colour photo of a man on the ladder at Brown Field 26 Oct 1954, P11 on its cart in level attitude with jeep, **P12 level flight over San Diego** (S32/S39!), P15 hovering seen from below, **P16 pilot climbing the ladder** (S30!). Licence still needed for P01, P05, P10, P11, P12, P15, P16. **Rejected:** XFY-1 color 1957 (Bill Larkins, CC BY-SA 2.0, not needed); USNI Photo Archive screenshots (copyrighted); NASM web page and Wikipedia screenshots (duplicates)  **Batch 2 (12 Oct) cleared, in `pogo-film/photos/cleared/`:** C01 "Convair XFY-1 in flight.jpg" level flight over San Diego ca. 1954 (USN, PD) → S32/S39, crop out the retouched X/arrow; C02 "Convair XFY-1 taking off at NAAF Brown Field 1954.jpeg" Nov 1954, TBM-3 Avenger chase plane (US Navy, PD) → S31/S39; C03 "Test pilot with Convair XFY-1 c1954.jpeg" (US Navy, PD), caption says only "A Convair test pilot", so label "CONVAIR TEST PILOT" unless a source names him Coleman; C04 "XFY-1 on launching cart NAN5-54.jpg" level on cart with jeep (USN, PD) → S20/S21. Still need licence: P01 tethered hangar, P05, P10, P15, P16, P17 colour hover. Still need full file: launching cart2, Richie. **Batch 3 (12 Oct) cleared (SDASM Archives on Commons, marked Public domain; credit "San Diego Air & Space Museum Archives"):** C05 colour takeoff (0074616) → S26/S31; C06 Pogo in production in the hangar (0074978) → S15 "1951 prototypes ordered"; **C07 Coleman portrait (Bio 000419)** → S29; **C08 Coleman (Marine uniform, helmet) with a Navy captain and a civilian by the Pogo (000423)** → S29/S40; C09 + C10 Coleman in the cockpit at the top of the ladder (000414, 000411) → S30. The SDASM colour slides have a strong magenta fade: colour-correct before use. Pending licence: P18 Coleman with a Navy captain, **P19 pilot in the cockpit turning to look back** (perfect for S04/S38 "looks back over his shoulder"). | 🔄 10 cleared |

## Why this topic (research, 8 Oct 2026)

- VidIQ: **"convair xfy-1 pogo" ≈ 35,000 searches/month, +164%**, competition 22/100. "convair xfy pogo" ≈ 14,000. "convair pogo", "pogo plane", "tail sitter", "vertical takeoff fighter": all under 750.
- NexLev YouTube search for "convair xfy-1 pogo": the top results are 4–17-year-old archive clips. The 2026 Pogo videos (KovaDocs 865, Jetline Journal 536, The high nut 992) **don't rank, because their titles leave out "Convair XFY-1"**. The top search spot is open.
- YouTube is **not** recommending Pogo videos right now, but it **is** pushing VTOL to this audience: Airspeed's *Why the V-22 Osprey Is So Complicated* got 139K in about a day (7 Oct). So the V-22 link goes in the description and tags to catch recommended traffic.
- The Ki-84 idea was rejected: it's WW2 Cipher's 29 Sep outlier (90-day rule), and it gets under 750 searches.

---

## Final package (paste-ready)

**Title (VidIQ 90/100, 54 characters, exact search phrase):**
> Why Did the Convair XFY-1 Pogo Have to Land Backwards?

**Hook (first 15 seconds, already in the script):** a backwards landing, then "Lockheed built a rival. It never once took off or landed vertically. Convair's did."

**Description:**

```
The Convair XFY-1 Pogo took off standing on its tail and had to land backwards, with the pilot looking over his shoulder at ground he couldn't see. Here's the physics of why.

Fifty years before the V-22 Osprey, the US Navy tried vertical takeoff with a fighter that sat on its tail. Lockheed built a rival, the XFV-1, but it never once took off or landed vertically. Convair's Pogo did, in 1954, with test pilot James "Skeets" Coleman at the controls.

In this episode of Hangar Physics we take the Pogo into the hangar to find out why the Navy wanted a fighter that could fly from a cargo ship, how two contra-rotating propellers let it hang in the air, why landing it meant flying backwards and blind, and why that one problem ended the programme.

Chapters
0:00 The fighter that landed backwards
0:45 The Navy's convoy problem
1:50 A fighter that sits on its tail
2:40 X-ray: how it hangs on its propellers
3:30 Inside the airship hangar
4:25 Landing blind
5:40 2 November 1954
6:35 Lockheed's rival
7:30 Why the Navy said no
8:30 What came next
(Chapter times are estimates. Update them after the edit.)

Researched and written by [your name]. 3D and AI-assisted animation; archival film and photographs are U.S. Navy / public domain.

SOURCES
• Norman Polmar, "Historic Aircraft: Tail-Sitters, Part II: Convair", Naval History magazine (USNI), July 2013
• Defense Media Network, "Tail-Sitters: XFY-1 Pogo and XFV-1"
• Vertical Flight Society (VTOL.org), Vertiflite history and James F. Coleman biography
• Smithsonian National Air and Space Museum, Convair XFY-1 Pogo (collection object)
• [archival film/photo credits: fill in from the sourcing list]

Some visuals are AI-generated or digitally enhanced illustrations, used to show what archival footage cannot.

#ConvairPogo #VTOL #AviationHistory
```

**Tags, in this order:** Convair XFY-1 Pogo, Convair XFY Pogo, XFY-1 Pogo, Convair Pogo, VTOL fighter, tail sitter aircraft, Skeets Coleman, Lockheed XFV-1, V-22 Osprey, experimental aircraft, Cold War aircraft, Hangar Physics

**Rules:** say "Convair XFY-1 Pogo" out loud in the first 30 seconds (it's in the script); upload the script as captions; no text on the thumbnail; category Science & Technology; end screen → the XF-85 video.

---

## Step 3: Grok prompt pack (v1, 9 Oct 2026, for FINAL script v8)

Shot numbers S01–S55 follow the final script in order. Shot types: 🎞 archival film · 📷 archival photo · 🤖 Grok · 🩻 X-ray graphic · 📊 graphic. **Disc ON** = turn on YouTube's "altered or synthetic content" switch (one 🤖 Disc ON shot is enough to turn it on for the whole video). ⚠ = check against the real photo before keeping.
Rules: the Pogo is a real aircraft and Coleman a real person, so **no AI-direct Pogo** (every 🤖 Pogo shot starts from an approved master) and **no AI faces of Coleman** (helmet from behind only). All Lockheed XFV-1 shots are archival.

### Part 0. Reference photos to download first (folder `pogo-refs`)
| Save as | What | Where | Search |
|---|---|---|---|
| R1 | Pogo standing on its tail, front 3/4, full aircraft | Wikimedia Commons, NARA, SDASM Flickr | `Convair XFY-1 Pogo` |
| R2 | Pogo standing, side view (delta wing + top and bottom fins + tip wheels visible) | same | `XFY-1 Pogo side` |
| R3 | Pogo in level flight | same / NARA | `XFY-1 Pogo in flight` |
| R4 | Close-up of a tip wheel on its strut | same | `XFY-1 Pogo wheel` / zoom a high-res R1/R2 |
| R5 | Nose and propellers close-up (count 3 + 3 blades) | same | `XFY-1 Pogo propeller` |
| R6 | Lockheed XFV-1 on its temporary landing gear | Wikimedia, NARA, SDASM | `Lockheed XFV-1` |
| R7 | Hangar One, Moffett Field (1950s or NASA photo) | NASA Ames image library, Wikimedia | `Hangar One Moffett Field` |
US Navy photos are usually public domain; check the licence line on each file. SDASM Flickr images say "No known copyright restrictions" on most, but check each.

### Part 1. Masters (make and approve these first)
| Master | Upload | Image prompt |
|---|---|---|
| **M1** Pogo standing on its tail, studio, front 3/4 | R1 + R2 | `[POGO LOCK]` Standing upright on its tail on the four tip wheels, front three-quarter view from the left, nose and propellers pointing straight up. `[STUDIO LOOK]` |
| **M2** Pogo standing, studio, side view | R2 + M1 | `[POGO LOCK]` Exact side view, standing upright on its tail, the delta wing and the large top and bottom fins clearly visible, same aircraft as the second reference. `[STUDIO LOOK]` |
| **M3** Pogo in level flight | R3 + M1 | `[POGO LOCK]` In normal level flight, side view, wings horizontal, propellers blurred into discs, clear sky above a 1950s California desert far below. `[FILM LOOK]` |
| **M4** Pogo hovering tail-down near the ground | M1 | `[POGO LOCK]` Hovering upright about 10 m above a concrete pad, nose and propellers pointing at the sky, the tail wheels facing the ground, propellers blurred into discs, light dust blowing outward on the pad, late-afternoon light. `[FILM LOOK]` |
⚠ Check every master against R1–R5: six propeller blades in two rows of three; delta wing; one large fin on top and one underneath (a cross from behind); a wheel at each wing tip and fin tip; bubble canopy; markings as in the reference.

### Part 2. Lock text (paste word for word)
**`[POGO LOCK]`**
> The Convair XFY-1 Pogo, a 1954 US Navy experimental tail-sitter fighter exactly like the reference image: short thick fuselage, bubble canopy near the nose, large delta wings, one very large swept fin on top and one equally large fin underneath so the wings and fins form a cross seen from behind, two three-bladed propellers in two rows at the nose turning in opposite directions with a pointed spinner, a small wheel on a short strut at the tip of each wing and each fin, no other landing gear, colours and markings exactly as in the reference.

**`[STUDIO LOOK]`**
> Photoreal 3D product render, dark graphite-to-amber gradient studio background, soft white key light, amber and steel-blue rim lights, glossy reflective floor, sharp focus, 16:9, no text.

**`[FILM LOOK]`**
> Photoreal cinematic 3D render, 1950s colour film look, muted colours, soft film grain, 16:9, no text.

**`[VIDEO SAFE]`** (end every video prompt with this)
> Keep the aircraft's shape, wings, fins, tip wheels, canopy, markings and exactly six propeller blades in two rows exactly as in the image. No morphing, no extra parts. Realistic motion blur. Smooth motion.

### Part 3. Shot by shot

**Cold open (0:00–0:30)**
| Shot | Line | Type | Start image / source | Image prompt (NEW only) | Video prompt / edit note |
|---|---|---|---|---|---|
| S01 | "November 1954." | 🎞 + 📊 | Real film: Pogo descending tail-first (SDASM "XFY-1"; NARA "Pogo") | — | 2 s black + propeller roar, then film; small "November 1954" lower-third |
| S02 | "hanging in the sky… propellers roaring" | 🤖 Disc ON | **REUSE M4** | — | Slow push-in from below, propellers blurred, dust swirling on the pad. `[VIDEO SAFE]` ⚠ |
| S03 | "coming down… tail first" | 🎞 | Real film: the tail-first descent, closest angle you have | — | Cut on "tail first" |
| S04 | "can't see the ground… looks back over his shoulder" | 🤖 Disc ON | **NEW** from M4 | `[POGO LOCK]` Close-up of the bubble canopy while hovering upright, a helmeted pilot seen from behind turning his head to look down over his shoulder, face not visible. `[FILM LOOK]` | The pilot's helmet turns slowly to look back and down, slight vibration. `[VIDEO SAFE]` ⚠ canopy shape |
| S05 | "lowers more than five tonnes… mostly by eye" | 🤖 Disc ON | **NEW** from M4 | `[POGO LOCK]` Low camera on the concrete looking up at the tail wheels a few metres above the ground, the huge aircraft towering above, dust blowing. `[FILM LOOK]` | The aircraft sinks slowly toward the camera, dust thickens. `[VIDEO SAFE]` ⚠ wheels |
| S06 | "too fast… slams… drift… tip over" | 🤖 Disc ON | **CHAIN** (last frame of S05) | — | A gust rocks the aircraft slightly sideways, it corrects, camera shakes. `[VIDEO SAFE]` |
| S07 | "His rival at Lockheed…" | 📷 | **R6** XFV-1 | — | Slow Ken Burns push-in |
| S08 | "This one did. This is the Convair XFY-1 Pogo." | 🤖 | **REUSE M1** | — | Slow hero orbit, a quarter turn, lights glinting. `[VIDEO SAFE]` |
| S09 | — | 📊 | Title card: Hangar Physics | — | Hard cut, 2 s |

**Curiosity loop**
| S10 | "why would anyone build…" | 🤖 | **REUSE M2** | — | Slow push-in, studio lights dimming. `[VIDEO SAFE]` |
| S11 | "comes down to one problem" | 🤖 | **NEW** from M1 | `[POGO LOCK]` Only the canopy and nose lit by one amber rim light, the rest fading into black. `[STUDIO LOOK]` | Almost still, the light slowly brightens. `[VIDEO SAFE]` |

**The problem**
| S12 | WWII convoys, U-boats and aircraft | 🎞 | NARA / Internet Archive (public domain): `Atlantic convoy 1942`, `U-boat` | — | 3–4 cuts |
| S13 | "carriers… expensive and limited" | 📊 | Map: Atlantic convoy route, few carriers (Claude builds) | — | |
| S14 | "What if any ship could carry its own fighter?" | 🤖 AI direct | **NEW, no reference** | A 1950s grey cargo ship at sea seen from above, a small empty square platform on its rear deck, calm grey Atlantic. `[FILM LOOK]` | Slow drift over the deck. Label "Illustration" in the edit |
| S15 | "After years of study… 1951… Convair and Lockheed" | 📊 | Card: "1951: prototypes ordered from Convair and Lockheed" (Claude builds) | — | |
| S16 | "same basic idea. A fighter that sits on its tail." | 📷 | Split screen: R1 (Pogo) + R6 (XFV-1) standing on tails | — | |
| S17 | "the catch… pilot sits in the nose, at the very top" | 🤖 | **NEW** from M2 | `[POGO LOCK]` Low camera at the tail wheels looking straight up the fuselage to the canopy high above. `[STUDIO LOOK]` | Slow tilt up from the tail to the canopy. `[VIDEO SAFE]` |
| S18 | "the ground is behind his back" | 🩻 | Side diagram on M2: pilot at top, arrow "ground" behind (Claude builds) | — | |
| S19 | "Keep that in mind." | 🤖 | **REUSE M1** | — | Slow push-in to the canopy. `[VIDEO SAFE]` |

**The machine**
| S20 | fuselage, delta wing, cross | 🤖 | **NEW** from M1 | `[POGO LOCK]` Seen exactly from behind and below, wings and the top and bottom fins forming a perfect cross. `[STUDIO LOOK]` | Slow orbit from the side to directly behind. `[VIDEO SAFE]` ⚠ fins |
| S21 | "no conventional landing gear… four small wheels" | 🤖 | **NEW** from M1 + R4 | `[POGO LOCK]` Close-up of one fin tip with its small wheel on a short strut resting on the studio floor. `[STUDIO LOOK]` | Slow slide along the strut to the wheel. `[VIDEO SAFE]` ⚠ wheel vs R4 |
| S22 | "it didn't sit. It stood." | 📷 | **R1** real photo standing on the ramp | — | Slow push-in |
| S23 | Allison T40, two propellers, opposite directions | 🤖 | **NEW** from M1 + R5 | `[POGO LOCK]` Close-up of the nose: the spinner and the two rows of three propeller blades. `[STUDIO LOOK]` | Propellers start turning slowly, front row clockwise, rear row anticlockwise. `[VIDEO SAFE]` ⚠ **weak in AI**: count the blades; fallback = still + slow zoom |

**X-ray (physics)**
| S24 | hover: thrust vs weight | 🩻 | M2 still + up/down arrows (Claude builds) | — | Thrust arrow grows → climbs; shrinks → sinks |
| S25 | torque cancels | 🩻 | Top view of the propellers: one spin = red twist arrow on the body; two = green, cancelled (Claude builds) | — | |
| S26 | "easy part… frightening" | 🎞 | Real film: vertical takeoff | — | |

**Testing**
| S27 | Moffett Field, Hangar One | 📷 | **R7** | — | Slow pan |
| S28 | tethered inside the hangar | 🎞 | Real film: tethered hover (SDASM "XFY-1"; NARA) | — | |
| S29 | James "Skeets" Coleman | 📷 | Real photo of Coleman with the Pogo (SDASM/Navy) | — | **Archival only** |
| S30 | ladder, two storeys, on his back, seat 45° | 📷 or 🤖 Disc ON | Real photo of the boarding ladder if found; else **NEW** from M1 | `[POGO LOCK]` A tall boarding ladder leaning against the upright fuselage up to the open canopy, a helmeted pilot climbing seen from behind, no face. `[FILM LOOK]` | Slow tilt up the ladder. `[VIDEO SAFE]` |
| S31 | 1 Aug 1954, cables off | 🎞 | Real film: first free flight outdoors | — | |
| S32 | takeoff, nose over, flew like a normal plane | 🎞 + 🤖 | Real film of the transition, then **REUSE M3** | — | M3: camera tracks alongside in level flight. `[VIDEO SAFE]` |

**Landing blind**
| S33 | pull nose up, hang, come down tail-first | 🤖 Disc ON | **REUSE M3**, then **REUSE M4** | — | **Weak in AI; don't ask Grok to rotate the plane 90°.** 1 s of M3 → cross-dissolve → 1 s of M4 |
| S34 | what he could see: sky / own aircraft / over shoulder | 🩻 | Sight-line diagram on M2 (Claude builds) | — | |
| S35 | three questions | 📊 | Three lines on screen over real descent film | — | |
| S36 | radar altimeter, three warning lights | 🩻 | M2 with the left wingtip pod highlighted + three unlabelled lights (Claude builds) | — | No colours shown |
| S37 | too fast / drift / gusts | 🤖 Disc ON | **REUSE M4** | — | A gust pushes the aircraft sideways, it rocks and corrects, dust swirls. `[VIDEO SAFE]` |
| S38 | "backwards, mostly by eye… four cars" | 🤖 Disc ON | **REUSE S04 image** | — | Very slow push-in on the helmet looking back. `[VIDEO SAFE]` |

**Payoff**
| S39 | 2 Nov 1954, the whole cycle | 🎞 | Real film: transitional flights (SDASM "F-0645") | — | Let it breathe, music up |
| S40 | Harmon Trophy; Coleman's skill | 📷 + 📊 | Coleman photo + "Harmon Trophy" text | — | |

**The rival**
| S41 | "remember the rival" | 📷 | **R6** | — | Push-in |
| S42 | waiting for the T54; temporary landing gear | 📷/🎞 | XFV-1 on its gear (photo or Lockheed film) | — | |
| S43 | tipped it up at altitude; never VTOL | 📷/🎞 | XFV-1 in flight | — | |
| S44 | "only one did the full cycle" | 📊 | Card: Pogo ✓ vertical takeoff and landing / XFV-1 ✗ (Claude builds) | — | |

**Why it ended**
| S45 | small ship, Atlantic, night, bad weather | 🤖 AI direct | **NEW, no reference** | Night storm at sea, the rear deck of a small 1950s warship pitching up and down in heavy waves, rain and spray, a small empty landing platform, no aircraft. `[FILM LOOK]` | Deck heaves, spray crosses the lens. Label "Illustration" |
| S46 | demanded exceptional skill | 🤖 | **REUSE M2** | — | Slow pull-back, light dims. `[VIDEO SAFE]` |
| S47 | faster jets; gearbox wearing out | 🎞 + 🩻 | 1950s Navy jet film (NARA, public domain) + M2 with the gearbox glowing red (Claude builds) | — | |
| S48 | 1955 wound down, 1956 ended | 📊 | Timeline card (Claude builds) | — | |
| S49 | three airframes, one flew, Smithsonian | 📷 + 📊 | Photo of the surviving Pogo (check licence) + "3 built · 1 flew" | — | |

**What came next and ending**
| S50 | Harrier, 1960s | 🎞 | DVIDS (US DoD, public domain): `AV-8B Harrier hover` | — | |
| S51 | V-22 tilts rotors; tail-sitter drones | 🎞 + 🤖 AI direct | DVIDS `MV-22 Osprey conversion`; drone: **NEW, no reference** | A small unmarked modern tail-sitter drone standing on its tail on a ship's deck, then lifting off vertically. `[FILM LOOK]` | Lifts straight up. Label "Illustration" |
| S52 | pilot never lands looking backwards | 🩻 | Split-screen sight lines: Pogo vs Harrier (Claude builds) | — | |
| S53 | closing line | 🤖 | **REUSE M1** | — | Slow pull-back, lights fade to black. `[VIDEO SAFE]` |
| S54 | comment question | 🤖 | **REUSE S04 image** | — | Hold, slow push |
| S55 | XF-85 tease + subscribe | 🎞 | 4 s from your own XF-85 video + end screen | — | |

### Part 4. Fallbacks
- **Propellers (S23 and every Pogo clip):** Grok often adds or loses blades. Count six (3 + 3). If wrong, use the still with a slow zoom.
- **Pitch-up from level to vertical (S33):** never ask Grok to rotate the aircraft. Dissolve M3 → M4.
- **X-ray and physics (S18, S24, S25, S34, S36, S47, S52):** Claude builds these as graphic clips on the M2 still. Don't use Grok.
- **Pilot:** no faces; helmet from behind only. Coleman = archival photos only.
- **Wheels and fins:** if a Grok image loses the tip wheels or the bottom fin, throw it away and regenerate.

### Part 5. What to upload for each shot
| Upload | Shots |
|---|---|
| **M1** (reuse) | S08, S19, S53 |
| **M2** (reuse) | S10, S46 |
| **M3** (reuse) | S32, S33 (part 1) |
| **M4** (reuse) | S02, S33 (part 2), S37 |
| **NEW from M1** | S11, S20, S21 (+R4), S23 (+R5), S30 |
| **NEW from M2** | S17 |
| **NEW from M4** | S04, S05 |
| **CHAIN** | S06 (after S05) |
| **Reuse an earlier shot's image** | S38, S54 (S04 image) |
| **NEW, no reference** (AI direct) | S14, S45, S51 (drone) |
| **Archival (you download)** | S01, S03, S07, S12, S16, S22, S26–S29, S31, S32, S39–S43, S47, S49, S50, S51 |
| **Claude builds** (graphics and X-ray) | S01 lower-third, S09, S13, S15, S18, S24, S25, S34–S36, S40 text, S44, S47 gearbox, S48, S49 text, S52 |


---

## FINAL SCRIPT (v8, CONFIRMED by the user 9 Oct 2026; fully verified; ≈1,580 words ≈ 10:30)

November 1954.

A fighter is hanging in the sky. Nose pointed straight up. Propellers roaring.

And it's coming down… tail first.

The pilot can't see the ground ahead of him. It's behind him. So he twists round in his seat, looks back over his shoulder, and lowers more than five tonnes of fighter toward the earth, mostly by eye.

Come down too fast, and it slams onto its tail. Drift, and it can tip over.

His rival at Lockheed built a plane to do exactly this. It never once managed it.

This one did. This is the Convair XFY-1 Pogo.

So why would anyone build a fighter you have to land backwards? And if it actually worked, why has almost nobody heard of it?

The answer comes down to one problem. And by the end of this video, you'll see exactly why it helped kill the Pogo.

It starts at sea. During the Second World War, Allied convoys crossing the Atlantic faced attacks from German U-boats and aircraft. Protecting those ships meant getting fighters over the ocean—but conventional fighters needed runways or aircraft carriers, and carriers were expensive and limited in number.

After the war, the Navy asked a radical question. What if any ship could carry its own fighter? No runway. No catapult. No carrier. Just a small platform on the deck.

After years of study, the Navy wanted a fighter that could take off straight up from a ship and land straight back down on it. In 1951, it ordered prototypes from Convair and Lockheed.

And both companies came up with the same basic idea. A fighter that sits on its tail.

And here's the catch nobody could design away. If a plane takes off pointing at the sky, it has to land pointing at the sky. The pilot sits in the nose, at the very top. So when he comes down to land, the ground is behind his back.

Keep that in mind. It's the whole story.

Convair's answer looked like nothing else in the sky. A short, fat fuselage. A delta wing. And a huge tail fin above and below, so from behind it looked like a cross.

It had no conventional landing gear. Just four small wheels, on the tips of the wings and the fins. When it was parked, it didn't sit. It stood.

In the nose was an Allison T40, really two turbine engines driving one gearbox, about 5,850 horsepower. It turned two propellers, each with three blades, sixteen feet across, about five metres, spinning in opposite directions.

Here's how it hung in the air. To hover, the propellers have to push upward harder than the whole aircraft weighs. At maximum takeoff weight, about sixteen thousand pounds, that's over seven tonnes. More thrust than weight, it climbs. Less, and it sinks. The throttle controls the climb and the sink. But the pilot still has to balance it on its tail with the controls, every second.

And there's a second problem. Spin one huge propeller one way, and the airframe wants to spin the other way. That's Newton's third law. So the Pogo has two. One turns clockwise, one turns anticlockwise, and their twist cancels out. Without that, it would just spin on its tail like a top.

Getting it into the air turned out to be the easy part. Getting it back down is where this story gets frightening.

In the spring of 1954, the Pogo was taken to Moffett Field in California, inside Hangar One, a building so big it was built to house a Navy airship.

For safety, it flew tied to cables, hovering under the roof. Over and over, it rose, hung there, and came back down.

The man flying it was Convair's test pilot, James "Skeets" Coleman.

Just getting in was strange. He climbed a ladder to a cockpit two storeys up, and settled in almost flat on his back, looking straight at the ceiling. For vertical flight, his seat tilted about 45 degrees toward the instrument panel, but landing still left him struggling to see the ground.

On the first of August, 1954, the cables came off. The Pogo took off outside, free, for the first time.

Taking off was simple. Point it up, open the throttle, and climb. Once it was high enough, the pilot pushed the nose over, and it flew like a normal plane.

Landing was the problem. He had to slow down, pull the nose up until the whole aircraft was pointing at the sky, and hang there on the propellers. Then he had to come down tail-first.

Now look at what he could actually see. In front of him, sky. Below him, his own aircraft. The only way to see the ground was to twist round and look back over his shoulder.

From there, he had to judge three things at once. How high am I? How fast am I sinking? And am I drifting sideways?

A radar altimeter in the wingtip drove three warning lights to help Coleman judge his descent. But the lights couldn't do the landing for him.

Come down too fast, and the impact could damage the aircraft or make it tip over. Drift sideways, and the narrow landing stance left little room for error. And all the time, any gust of wind is pushing on that big wing and those tall fins.

He's doing this backwards, mostly by eye, in a fighter that weighs as much as four cars.

On the second of November, 1954, Coleman did the whole thing. Straight up from the ground, over into level flight, back up to vertical, and down, backwards, onto its tail. No aircraft like it had ever done that before.

It earned him the Harmon Trophy, one of aviation's highest awards. The Pogo worked. But it took a pilot of Coleman's skill to land it.

And remember the rival I mentioned at the start? Its story explains why the Navy got nervous.

Lockheed's XFV-1 never got that far. It was waiting for a more powerful engine, the Allison T54, that never materialised. So it fitted temporary landing gear and flew its prototype off a runway like a normal plane.

High in the air, its pilot did tip it up and hang it on its propellers. But the XFV-1 never once took off or landed vertically.

So only one tail-sitter fighter did the full cycle. And that one showed the Navy exactly where the problem was.

Think about where this fighter was meant to live. Not a calm airfield in California. A small platform on a ship, rolling in the Atlantic, at night, in bad weather. Flown by an ordinary squadron pilot, not one of the best test pilots in the country. Landing backwards, onto a deck that's moving.

The testing made it clear. Landing the Pogo demanded exceptional skill, and that made it unsuitable for ordinary pilots operating from ordinary ships.

And it wasn't the only problem. New jet fighters were arriving that were faster than any propeller-driven fighter, Pogo included. And the Pogo's huge gearbox was wearing out, shedding metal into its oil.

By 1955, the programme was being wound down, and by 1956, the Navy had ended its work on the Pogo.

Convair built three Pogo airframes. Only one ever flew. That aircraft still exists in the collection of the Smithsonian's National Air and Space Museum.

But the idea didn't die. In the 1960s, the Harrier took a different route to vertical flight. It kept the pilot level and pointed the engine's thrust down instead.

The V-22 Osprey tilts its rotors, not the whole aircraft. And some modern drones do take off and land on their tails, just like the Pogo, because there's nobody inside who has to look back.

Every answer that came after has one thing in common. The pilot never has to land looking backwards.

The Pogo proved a fighter could take off without a runway. It couldn't prove that ordinary pilots could land it safely, at sea.

If you were in that seat, looking back over your shoulder at the ground, would you have trusted it? Tell me in the comments.

And the Pogo wasn't even the strangest answer to "how do you fight without a runway?" A few years earlier, the Air Force tried a fighter with no landing gear at all, one that lived inside a bomber. That story is right here. And if you want one strange aircraft explained every week, subscribe to Hangar Physics.

All claims verified 9 Oct 2026. Wheels confirmed by the Smithsonian and USNI (castering wheels on struts at the tips of the wings and fins). Hangar One was built for the airship USS Macon (NPS). v7 changes: the Lockheed reason is now "waiting for a more powerful engine that never arrived" (the "only engine cleared" quote couldn't be confirmed); "Dozens of times" became "Over and over" (sources give about 60 hours, not a flight count). v8: new present-tense cold open (Nov 1954), 'same basic idea', 'no conventional landing gear'. v7.1: Lockheed engine named (Allison T54); the 7,100 hp figure was left out because it appears in only one secondary source and the same 7,100 figure is elsewhere given for the T40-A-14.


---

### History

## Script (v5 = user's own edit of v4, 9 Oct 2026)

v5 is v4 with the user's changes: the convoy paragraph rewritten (U-boats and aircraft; carriers expensive and limited); the radar altimeter reduced to "three warning lights to help Coleman judge his descent"; the landing-risk lines reworded ("impact could damage the aircraft or make it tip over", "narrow landing stance"); Lockheed's reason given as "the two programmes faced different engine and development challenges"; the ending reworded as "By 1955 the programme was being wound down, and by 1956 the Navy had ended its work on the Pogo."
Claude's suggested tweaks (pending the user's answer): (1) restore the Smithsonian-backed Lockheed reason: "The Navy gave Convair the only engine cleared for both vertical and horizontal flight. Lockheed never got one."; (2) "any gust of wind was pushing" → "is pushing" (present tense, to match the scene).
The full v5 text is in the chat of 9 Oct; on approval, paste the final text here.

### Previous: Script (v4 FINAL candidate, 9 Oct 2026: all fact-checks applied, rewritten for watch time; ≈1,560 words ≈ 10:20)

One continuous script for one video. Section labels in [brackets] are for the editor, not to be read aloud.

[HOOK]

In 1954, a test pilot brought a fighter in to land… backwards.

The ground wasn't in front of him. It was behind him. So he twisted round in his seat, looked back over his shoulder, and lowered more than five tonnes of fighter onto its tail.

His rival at Lockheed built a plane to do the same thing. It never once took off or landed vertically.

This one did. This is the Convair XFY-1 Pogo.

[CURIOSITY LOOP]

So why would anyone build a fighter you have to land backwards? And if it actually worked, why has almost nobody heard of it?

The answer comes down to one problem. And by the end of this video, you'll see exactly why it helped kill the Pogo.

[MAIN STORY: THE PROBLEM]

It starts at sea. In the Second World War, the convoys crossing the Atlantic were hunted from below by U-boats, and from above by long-range aircraft.

The best protection was a fighter overhead. But fighters needed carriers, and there were never enough carriers to go round.

After the war, the Navy asked a radical question. What if any ship could carry its own fighter? No runway. No catapult. No carrier. Just a small platform on the deck.

After years of study, the Navy wanted a fighter that could take off straight up from a ship, and land straight back down on it. In 1951, it ordered prototypes from Convair and Lockheed.

And both companies came up with the same answer. A fighter that sits on its tail.

[KEY INSIGHT 1]

And here's the catch nobody could design away. If a plane takes off pointing at the sky, it has to land pointing at the sky. The pilot sits in the nose, at the very top. So when he comes down to land, the ground is behind his back.

Keep that in mind. It's the whole story.

[THE MACHINE]

Convair's answer looked like nothing else in the sky. A short, fat fuselage. A delta wing. And a huge tail fin above and below, so from behind it looked like a cross.

It had no normal landing gear at all. Just four small wheels, on the tips of the wings and the fins. When it was parked, it didn't sit. It stood.

In the nose was an Allison T40, really two turbine engines driving one gearbox, about 5,850 horsepower. It turned two propellers, each with three blades, sixteen feet across, about five metres, spinning in opposite directions.

[KEY INSIGHT 2: X-RAY]

Here's how it hung in the air. To hover, the propellers have to push upward harder than the whole aircraft weighs. At maximum takeoff weight, about sixteen thousand pounds, that's over seven tonnes. More thrust than weight, it climbs. Less, and it sinks. The throttle controls the climb and the sink. But the pilot still has to balance it on its tail with the controls, every second.

And there's a second problem. Spin one huge propeller one way, and the airframe wants to spin the other way. That's Newton's third law. So the Pogo has two. One turns clockwise, one turns anticlockwise, and their twist cancels out. Without that, it would just spin on its tail like a top.

[RETENTION POINT]

Getting it into the air turned out to be the easy part. Getting it back down is where this story gets frightening.

[MAIN STORY: TESTING]

In the spring of 1954, the Pogo was taken to Moffett Field in California, inside Hangar One, a building so big it was built to house a Navy airship.

For safety, it flew tied to cables, hovering under the roof. Dozens of times, it rose, hung there, and came back down.

The man flying it was Convair's test pilot, James "Skeets" Coleman.

Just getting in was strange. He climbed a ladder to a cockpit two storeys up, and settled in almost flat on his back, looking straight at the ceiling. For vertical flight, his seat tilted about 45 degrees toward the instrument panel, but landing still left him struggling to see the ground.

On the first of August, 1954, the cables came off. The Pogo took off outside, free, for the first time.

Taking off was simple. Point it up, open the throttle, and climb. Once it was high enough, the pilot pushed the nose over, and it flew like a normal plane.

[KEY INSIGHT 3: LANDING BLIND]

Landing was the problem. He had to slow down, pull the nose up until the whole aircraft was pointing at the sky, and hang there on the propellers. Then he had to come down tail-first.

Now look at what he could actually see. In front of him, sky. Below him, his own aircraft. The only way to see the ground was to twist round and look back over his shoulder.

From there, he had to judge three things at once. How high am I? How fast am I sinking? And am I drifting sideways?

A radar altimeter in the wingtip drove three warning lights, from green for a safe descent to red for coming down too fast. It helped, but it couldn't do the landing for him.

Come down too fast, and the aircraft slams onto its tail. Drift, and it can tip over. And all the time, any gust of wind is pushing on that big wing and those tall fins.

He's doing this backwards, mostly by eye, in a fighter that weighs as much as four cars.

[PAYOFF]

On the second of November, 1954, Coleman did the whole thing. Straight up from the ground, over into level flight, back up to vertical, and down, backwards, onto its tail. No aircraft like it had ever done that before.

It earned him the Harmon Trophy, one of aviation's highest awards. The Pogo worked. But it took a pilot of Coleman's skill to land it.

[RETENTION POINT]

And remember the rival I mentioned at the start? Its story explains why the Navy got nervous.

[THE RIVAL]

Lockheed's XFV-1 never got that far. The Navy gave Convair the only engine cleared for both vertical and horizontal flight. Lockheed never got one. So it bolted on temporary landing gear, and flew it off a runway like a normal plane.

High in the air, its pilot did tip it up and hang it on its propellers. But without that engine, the XFV-1 never once took off, or landed, vertically.

So only one tail-sitter fighter did the full cycle. And that one showed the Navy exactly where the problem was.

[KEY INSIGHT 4: WHY IT ENDED]

Think about where this fighter was meant to live. Not a calm airfield in California. A small platform on a ship, rolling in the Atlantic, at night, in bad weather. Flown by an ordinary squadron pilot, not one of the best test pilots in the country. Landing backwards, onto a deck that's moving.

The testing made it clear. Landing the Pogo demanded exceptional skill, and that made it unfit for ordinary pilots on ordinary ships.

And it wasn't the only problem. New jet fighters were arriving that were faster than any propeller-driven fighter, Pogo included. And the Pogo's huge gearbox was wearing out, shedding metal into its oil.

By 1955 the programme was shelved, and in 1956 the Navy closed the books on it.

Convair built three Pogo airframes. Only one ever flew. That aircraft still exists, in the collection of the Smithsonian's National Air and Space Museum.

[WHAT CAME NEXT]

But the idea didn't die. In the 1960s, the Harrier took a different route to vertical flight. It kept the pilot level and pointed the engine's thrust down instead.

The V-22 Osprey tilts its rotors, not the whole aircraft. And some modern drones do take off and land on their tails, just like the Pogo, because there's nobody inside who has to look back.

Every answer that came after has one thing in common. The pilot never has to land looking backwards.

[CLOSING LINE]

The Pogo proved a fighter could take off without a runway. It couldn't prove that ordinary pilots could land it safely, at sea.

[CTA]

If you were in that seat, looking back over your shoulder at the ground, would you have trusted it? Tell me in the comments.

And the Pogo wasn't even the strangest answer to "how do you fight without a runway?" A few years earlier, the Air Force tried a fighter with no landing gear at all, one that lived inside a bomber. That story is right here. And if you want one strange aircraft explained every week, subscribe to Hangar Physics.

---

Before recording, check on the Smithsonian page (object A19730274000): (1) the radar-altimeter light colours (green → red); (2) the gearbox-wear wording; (3) the four wheels on the tips of the wings and fins (photo). Fallbacks: "three warning lights that warned him if he came down too fast" / "small wheels on the tips of its tail fins".

v4 changes: no 1950 date; "Convair built three Pogo airframes. Only one ever flew."; seat tilted about 45° toward the instrument panel; radar altimeter, three lights (safe wording); gearbox wear added; new closing line; restructured for watch time (hook → curiosity loop → story → 4 key insights → 2 retention points → payoff → CTA).


## Pronunciation

| Word | Say |
|---|---|
| Convair | CON-vair |
| XFY-1 | ex-eff-why-one |
| XFV-1 | ex-eff-vee-one |
| Moffett | MOFF-it |
| Allison | AL-ih-sun |
| Skeets | SKEETS |
| Harmon | HAR-mun |
| Hangar One | HANG-er one |

---

## Fact check (done 8 Oct 2026 with web searches; Wikipedia and archive sites are blocked from the container, so checked against several secondary sources each)

| # | Claim in script | Verdict | Notes |
|---|---|---|---|
| 1 | 1950 Navy requirement for a convoy-escort VTOL fighter from small platforms on ships | ✓ | USNI / Polmar; Defense Media Network |
| 2 | 1951 prototypes ordered from Convair and Lockheed | ✓ | Most sources say March 1951 (one says May), so the script says only "1951" |
| 3 | Both were tail-sitters | ✓ | |
| 4 | Allison T40, two turbines driving one gearbox, about 5,500 hp | ✓ (≈) | Sources give 5,500–5,850 hp, so the script says "about 5,500" |
| 5 | Two contra-rotating 3-blade props, 16 ft (4.88 m) | ✓ | Curtiss-Wright |
| 6 | Four small wheels on the tips of the wings and fins | ⚠ VERIFY | One secondary source ("four tiny caster wheels"). Check against a photo of the tail before recording |
| 7 | Max takeoff ≈ 16,250 lb (7,370 kg); empty ≈ 11,700 lb (5,310 kg) | ✓ | "More than five tonnes" (empty) and "about sixteen thousand pounds at full fuel" are both safe |
| 8 | Tethered flights inside Moffett Field Hangar One (airship hangar), spring 1954 | ✓ | Start date April 19 or 29 1954 (sources differ), so the script says "spring of 1954" |
| 9 | First free (untethered) flight 1 Aug 1954 | ✓ | The location differs between sources (Moffett vs Brown Field), so the script doesn't name it |
| 10 | Pilot: James F. "Skeets" Coleman, Convair test pilot | ✓ | |
| 11 | Pilot sat almost flat on his back on the ground; climbed a ladder | ✓ | migflug.com. No seat-tilt angle used |
| 12 | Landing = look back over shoulder | ✓ | Multiple sources |
| 13 | 2 Nov 1954 full cycle: vertical takeoff → level → vertical landing; first of its kind | ✓ | VTOL.org / Coleman bio |
| 14 | Coleman awarded the Harmon Trophy | ✓ | Year differs (1955/1956), so the script gives no year |
| 15 | Only an expert pilot could land it | ✓ | Secondary sources |
| 16 | Jets were faster; programme ended 1955 | ✓ | "Navy declared concluded Aug 1955" (one source); Coleman flew until June 1955 |
| 17 | Three ordered, only one flew (BuNo 138649) | ✓ | |
| 18 | Survivor in the Smithsonian NASM collection | ✓ | The exact building isn't confirmed (Garber vs Udvar-Hazy), so the script says "collection" |
| 19 | XFV-1: temporary landing gear; transitions to hover at altitude; awaited the T54 engine; never VTO/VL | ✓ | Polmar; migflug; Palm Springs Air Museum |
| 20 | Harrier, 1960s; keeps the pilot level | ✓ | general knowledge (P.1127 first hovered 1960) |
| 21 | V-22 tilts its rotors; some drones are tail-sitters | ✓ | general |
| 22 | "Weighs as much as four cars" (≈ 11,700–16,000 lb ÷ ~3,500–4,000 lb per car) | ✓ (≈) | comparison |
| 23 | Hangar One was built for a Navy airship | ✓ | (USS Macon) |

**No direct quotes are used**, because none could be verified from here. If you find a verified Coleman quote (USNI article or VFS bio), it can replace S28's last line.

---

## Access notes (so a new chat doesn't retry)

- From Claude's container these are **blocked**: Wikipedia, Wikimedia Commons, archive.org, NARA catalog, YouTube/ytimg, airandspace.si.edu, navy.mil, vtol.org, sandiegoairandspace.org. Web **search** works; page fetching mostly doesn't.
- So **the user downloads the archival files** (Claude gives exact searches and links in step 4). `ffmpeg` and `python3` are available, so Claude can make graphics, maps, cards and X-ray diagram clips locally.
- VidIQ has generation tools (b-roll, video, voiceover, thumbnail, motion graphics) that cost credits. Check the balance before using them.
