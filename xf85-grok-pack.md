# XF-85 Goblin: Grok prompt pack (final script)

For *Why Did This Fighter Have No Landing Gear?*, final script (Ohio ending, tail-sitter tease). This replaces the shot list in `airspeed-grok-prompts.md` for this video.

## How to read the "Upload" column

Every shot tells you exactly which image to upload into Grok before you type the prompt:

- **🆕 first use**: the first time you use this image. Get it or make it now.
- **♻ same as S07**: an image you've already used. Upload the **same file** again, don't make a new one. The note lists every earlier shot that used it, so you can find it.
- **🎞 from S29**: CHAIN. Take a screenshot of the last frame of that clip and upload it.
- **— none**: nothing to upload (AI direct, archival footage or a graphic).

**Shot types:**
- **REUSE**: upload a master and go straight to the video prompt.
- **NEW**: make a new image from the upload first, save it as the shot name (`S07.png`), then make the video from it.
- **ARCH**: real footage or photos, so no Grok.
- **GFX**: made in CapCut or Canva.
- ⚠ = check the result against the real photo.
- **Disc ON** = switch on YouTube's "altered or synthetic content" setting at upload.

**Hard rules:** never make an AI version of Edwin Schoch or any real person. Never make an AI version of the Convair Pogo, the Sparrowhawk, the TB-3, the Boeing 747 or the museum Goblins.

---

## Step 1. Download the real photos and footage first

Nothing in Steps 2–4 works until these are saved in a folder called `XF85-refs`. US Air Force, NARA and Navy material is usually public domain, but check the licence line on each file.

**Photos you'll upload into Grok (get these before Step 2):**

| Save as | What | Where | Search | Needed for |
|---|---|---|---|---|
| **R1** | XF-85 front or front-3/4 photo | nationalmuseum.af.mil, Wikimedia Commons | `XF-85 Goblin` | making M1 |
| **R2** | XF-85 side view, wings spread | Same | `XF-85 Goblin side` | making M2 |
| **R3** | XF-85 on the trapeze under the EB-29B | Same, or catalog.archives.gov | `XF-85 EB-29B trapeze` | making M4 |
| **R4** | Early B-36 in flight (six propellers, no jet pods) | Wikimedia, NARA, SDASM Flickr | `B-36B Peacemaker` | making M5 |

**Real footage and photos used straight in the edit (not uploaded into Grok):**

| Save as | What | Where | Search | Used in |
|---|---|---|---|---|
| **R5** | The Ohio Goblin on its stand, hook raised | nationalmuseum.af.mil | `XF-85 Goblin museum` | S40, S47 |
| **R6** | The Nebraska Goblin | sacmuseum.org, Wikimedia | `XF-85 SAC Aerospace Museum` | S40 |
| **A1** | 1948 Goblin/EB-29B test film | NARA; the San Diego Air & Space Museum's YouTube channel (film "MF 6") | `XF-85 Goblin film 1948` | S05, S27, S34 |
| **A2** | USS Macon or Akron catching a Sparrowhawk | NARA, Naval History and Heritage Command | `F9C Sparrowhawk trapeze` | S14 |
| **A3** | Zveno TB-3 carrying fighters | Wikimedia Commons | `Zveno TB-3` | S15 |
| **A4** | B-29 formations and flak, 1944–45 | NARA, Wikimedia | `B-29 formation 1945` | S12 |
| **A5** | A 1949 mid-air refuelling | NARA | `KB-29 refueling 1949` | S38 |
| **A6** | FICON: an RF-84K under a GRB-36 | NARA, SDASM | `FICON RF-84K GRB-36` | S41 |
| **A7** | Convair XFY-1 Pogo taking off or landing | SDASM (film "F-0645"), NARA | `XFY-1 Pogo` | S49 |

---

## Step 2. Make the master images (in this order)

Make each master, compare it with the real photo, and save it in a `masters` folder. **Don't start Step 4 until all five are approved.**

| Order | Master | Upload | Image prompt |
|---|---|---|---|
| 1 | **M1** Goblin, studio, head-on, wings folded | 🆕 **R1** (first use) | `[GOBLIN LOCK]` Head-on view, perfectly centred and symmetrical, wings folded upward, hook raised above the nose. `[STUDIO LOOK]` |
| 2 | **M2** Goblin, studio, front-3/4, wings spread | 🆕 **R2** (first use) **+** ♻ **M1** (same as the one you just made) | `[GOBLIN LOCK]` Front three-quarter view from the left, wings spread out, hook raised. Same aircraft as the second reference image. `[STUDIO LOOK]` |
| 3 | **M3** Goblin in flight, side view | ♻ **M2** (same as the one you just made) | `[GOBLIN LOCK]` In flight, side view, wings spread, hook folded down, clear blue sky above a 1940s California desert far below. `[FILM LOOK]` |
| 4 | **M4** EB-29B with the Goblin on the trapeze | 🆕 **R3** (first use) **+** ♻ **M3** | `[B-29 LOCK]` Seen from below and behind in flight, a steel trapeze lowered from the bomb bay with the small jet from the second reference hanging from it by its nose hook. Desert far below. `[FILM LOOK]` |
| 5 | **M5** B-36 in flight | 🆕 **R4** (first use) | `[B-36 LOCK]` Side view in flight, high above the clouds, midday light. `[FILM LOOK]` |

**Before approving (⚠):**
- **M1 and M2:** hook shape and position, wings folding *upward*, the number of tail fins, the bubble canopy, the nose intake, and **no wheels**.
- **M4:** the trapeze matches R3, and the B-29 has **four** engines.
- **M5:** **six** propellers *behind* the wing, and no jet pods.

---

## Step 3. Lock text (paste word for word, every time)

**`[GOBLIN LOCK]`**
> The McDonnell XF-85 Goblin, a tiny 1948 experimental jet fighter exactly like the reference image: short egg-shaped polished-aluminium fuselage, bubble canopy near the nose, a single steel hook on top of the nose in front of the canopy, small swept wings, a cluster of small tail fins at the rear exactly as in the reference, USAF markings, no landing gear, no wheels, no propeller.

**`[B-29 LOCK]`**
> A 1940s Boeing B-29 Superfortress bomber exactly like the reference: polished aluminium, long rounded glass nose, four propeller engines on a long straight wing, one tall tail fin.

**`[B-36 LOCK]`**
> An early Convair B-36 bomber exactly like the reference: enormous straight wings, polished aluminium, exactly six propeller engines mounted on the back edge of the wing with propellers facing backward, no jet pods, tall single tail.

**`[STUDIO LOOK]`**
> Photoreal 3D product render, dark graphite-to-amber gradient studio background, soft white key light from the front, amber and steel-blue rim lights from behind, glossy reflective floor, sharp focus, 16:9, no text.

**`[FILM LOOK]`**
> Photoreal cinematic 3D render, 1940s colour film look, muted Kodachrome colours, soft film grain, 16:9, no text.

**`[VIDEO SAFE]`** (end every video prompt with this)
> Keep the aircraft's shape, fins, hook, wings, markings and number of engines and propellers exactly as in the image. No morphing, no extra parts. Realistic motion blur. Smooth motion.

---

## Step 4. Shot by shot

Each Grok clip is 3–5 s; trim it in CapCut. "2 clips" means making two videos from the same upload with different camera moves.

### Cold open

| Shot | Script | Upload | Type | Image prompt (NEW only) | Video prompt |
|---|---|---|---|---|---|
| S01 | "Why would anyone build a fighter jet with no landing gear?" | 🆕 **M1** (first shot use) | REUSE | — | Slow smooth orbit, a quarter turn to the right, light glinting on the metal. `[VIDEO SAFE]` ⚠ |
| S02 | "Not small wheels… No wheels at all." | 🆕 **M2** (first shot use) | NEW → save as **S02.png** | `[GOBLIN LOCK]` Low camera looking up at the smooth underside from below: no wheels and no wheel wells, only a thin steel skid along the belly. `[STUDIO LOOK]` | Slow sideways slide under the belly, close macro shot. `[VIDEO SAFE]` ⚠ skid |
| S03 | "Just a hook… on the top of its nose." | ♻ **M2**, same as S02 | REUSE | — | Slow pull-back from a close-up of the hook to the full aircraft. `[VIDEO SAFE]` |
| S04 | "Because this fighter was never supposed to… over 200 miles an hour." · **Disc ON** | 🆕 **M4** (first shot use) | REUSE, 2 clips | — | Clip 1: slow drift alongside, both aircraft steady. Clip 2: the small jet releases and drops smoothly away, the bomber flies on. `[VIDEO SAFE]` ⚠ |
| S05 | "And the first time a pilot tried to fly back to it…" | — none | ARCH **A1** (first use) | — | — |

### Stakes

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S06 | "This is the McDonnell XF-85 Goblin, the smallest American jet fighter ever built." | ♻ **M2**, same as S02, S03 | REUSE + title card "XF-85 GOBLIN · 1948" | — | Very slow push-in, almost still. `[VIDEO SAFE]` |
| S07 | "about the length of a family car, and shaped like an egg with wings." | ♻ **M2**, same as S02, S03, S06 | NEW → save as **S07.png** | `[GOBLIN LOCK]` Standing on the studio floor beside a grey faceless 1.8 m human mannequin and a generic 1940s family car for scale, the jet about the same length as the car. `[STUDIO LOOK]` | Slow pan from left to right across all three. `[VIDEO SAFE]` ⚠ sizes |
| S08 | "It only makes sense once you understand the problem… inside its bombers." | 🆕 **M5** (first shot use) | REUSE | — | Slow push-in toward the bomber's belly. `[VIDEO SAFE]` ⚠ six props |

### The problem of the era

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S09 | "At the end of World War Two… and back without landing." | ♻ **M5**, same as S08 | REUSE | — | Slow track along the wing from the fuselage to the wingtip. `[VIDEO SAFE]` ⚠ six props, no jets |
| S10 | "Its wingspan was about 70 metres… wider than a Boeing 747's." | — none | GFX | — | Flat top-view silhouettes: B-36 over 747, with a 230 ft / 70 m label. |
| S11 | "The B-36 could fly for well over a day… a fraction of the way." | — none | GFX → save as **S11-map** | — | Map: a long bomber arc across the Arctic and a small fighter-range circle stopping near the coast. |
| S12 | "Every bomber crew of the last war… terrible losses." | — none | ARCH **A4** (first use) | — | — |
| S13 | "So the Air Force asked a strange question… carry the fighter?" | ♻ **M5**, same as S08, S09 | NEW | `[B-36 LOCK]` Small in the lower third of the frame, flying alone across a vast empty pale sky. `[FILM LOOK]` | Very slow drift, the bomber crosses left to right, thin clouds below. `[VIDEO SAFE]` |

### "It wasn't a new idea"

| Shot | Script | Upload | Type | Notes |
|---|---|---|---|---|
| S14 | "In the 1930s the US Navy flew giant airships…" | — none | ARCH **A2** (first use) | Never AI. |
| S15 | "The Soviet Union went further… real combat missions." | — none | ARCH **A3** (first use) | Slow Ken Burns zoom on the photo. |

### Partial answer and walkaround

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S16 | "So the obvious answer is… only half the story." | ♻ **M2**, same as S02, S03, S06, S07 | REUSE | — | Slow orbit to the left. `[VIDEO SAFE]` In CapCut: glowing outlines where wheels would be, fading out. |
| S17 | "…comes down to one number… no more than about 15 feet long." | ♻ **M2**, same as S02–S16 | NEW | `[GOBLIN LOCK]` Sitting inside a glowing steel-blue wireframe box, only a narrow gap at the nose and tail, blueprint style. `[STUDIO LOOK]` | Slow push-in. `[VIDEO SAFE]` In CapCut, add the label "≈ 15 ft limit". ⚠ **weak in AI** |
| S18 | "The fighter had to fit inside the B-36… had to go." | ♻ **M5**, same as S08, S09, S13 | GFX on the still (no Grok) | — | In CapCut: a slow zoom on M5, with the bomb-bay area outlined in amber. |
| S19 | "The result was 14 feet 10 inches… family car." | ♻ **S07.png** (the image you made in S07) | REUSE | — | Slow pan the other way. In CapCut: label "14 ft 10 in · 4.52 m". `[VIDEO SAFE]` |
| S20 | "The wings folded upward… 21 feet." | ♻ **M1**, same as S01; then ♻ **M2**, same as S02–S17 | REUSE, 2 clips | — | 1 s tiny push-in on M1, cross-dissolve into 1 s on M2, then label "21 ft · 6.4 m". Don't ask Grok to fold the wings. |
| S21 | "The tail was so cramped… almost no length." | ♻ **M2** | NEW | `[GOBLIN LOCK]` Rear three-quarter close-up of the cluster of tail fins and the jet exhaust. `[STUDIO LOOK]` | Slow orbit around the tail. `[VIDEO SAFE]` ⚠ fin count vs R2 |
| S22 | "Inside that egg was a single Westinghouse J34… 650 miles an hour." | ♻ **M2** | NEW → save as **S22.png**, 2 clips | `[GOBLIN LOCK]` Ghosted semi-transparent X-ray cutaway: the aluminium skin see-through like glass, a single jet engine inside glowing orange from the nose intake to the tail exhaust. `[STUDIO LOOK]` | Slow orbit, the orange glow pulsing gently. `[VIDEO SAFE]` ⚠ **weak in AI** |
| S23 | "It was designed to carry four .50-calibre machine guns…" | ♻ **M2** | NEW | `[GOBLIN LOCK]` Extreme close-up of the nose showing the machine-gun ports. `[STUDIO LOOK]` | Slow slide along the nose. `[VIDEO SAFE]` ⚠ 4 ports |
| S24 | "And the pilot sat in a seat with an ejection system… his only way home." | ♻ **M4**, same as S04 | NEW | Point of view from inside the tiny cockpit of the jet in the reference, looking up through the bubble canopy at the steel hook and the silver bomber belly just above. No people visible. `[FILM LOOK]` | Small shakes as if in rough air, light streaks across the canopy. `[VIDEO SAFE]` |
| S25 | "Landing gear would have meant… already squeezed into a box." | ♻ **S22.png** (the X-ray image from S22) | GFX on the still (no Grok) | — | In CapCut: red wheel and strut icons float in and bounce off the steel-blue box outline. |
| S26 | "So the engineers took it out… a steel skid underneath for emergencies." | ♻ **S02.png** (the belly image from S02) | REUSE | — | Slow slide the other way along the belly. `[VIDEO SAFE]` |

### The test

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S27 | "The B-36 wasn't ready… after the whale that swallowed Pinocchio." | — none | ARCH ♻ **A1**, same as S05 (or the R3 photo) | — | — |
| S28 | "The pilot was McDonnell test pilot Edwin Schoch… in flight." | ♻ **M4**, same as S04, S24 (only if you have no real photo of him) | ARCH photo, or REUSE · Disc ON | — | Slow drift alongside. `[VIDEO SAFE]` Never an AI face. |
| S29 | "On the 23rd of August 1948, Schoch dropped free." · **Disc ON** | ♻ **M4**, same as S04, S24 | NEW | `[GOBLIN LOCK]` Side view just below the bomber's trapeze, falling away, a faint orange glow in its tail exhaust. `[FILM LOOK]` | The jet falls a short way, its exhaust flares orange with heat shimmer, then it levels off. Camera tracks alongside. `[VIDEO SAFE]` ⚠ |
| S30 | "But the air under a four-engine bomber isn't still…" · **Disc ON** | ♻ **M4** | NEW | `[B-29 LOCK]` Close-up under the belly and the steel trapeze bar, clouds racing below, visible churning air. `[FILM LOOK]` | Heat-haze ripples under the belly, the trapeze bar swings and shakes, the camera shakes. `[VIDEO SAFE]` |
| S31 | "Schoch closed in. The Goblin bounced. The trapeze swung…" · **Disc ON** | 🎞 **last frame of the S29 clip** | CHAIN | — | The small jet rises and bounces toward the swinging trapeze bar, rocking side to side. `[VIDEO SAFE]` ⚠ |
| S32 | "…and the bar hit his canopy…" · **Disc ON** | ♻ **M4** | NEW | `[GOBLIN LOCK]` Extreme close-up of the bubble canopy with the steel trapeze bar a few centimetres away. No pilot face visible. `[FILM LOOK]` | The bar strikes the canopy, the glass cracks and shatters outward in slow motion. `[VIDEO SAFE]` |
| S33 | "He flew down to the dry lakebed… He survived." · **Disc ON** | 🆕 **M3** (first shot use) | NEW | `[GOBLIN LOCK]` A metre above a vast cracked dry lakebed in the Mojave desert at golden hour, 1948, long shadows, about to touch down on its belly skid. `[FILM LOOK]` | It touches down on its belly and slides across the lakebed throwing a long plume of dust, slowing to a stop. Camera low alongside. No wheels. `[VIDEO SAFE]` ⚠ |
| S34 | "Weeks later, in October 1948, a Goblin finally hooked back…" | — none | ARCH ♻ **A1**, same as S05, S27 | — | — |
| S35 | "Over the whole programme there were seven free flights…" | — none | GFX → save as **S35-tally** | — | A tally board of 7 flights; ✓ ✗ marks fill in one by one (3 ✓). |
| S36 | "These were test pilots in clear California weather…" | ♻ **M3**, same as S33 | REUSE | — | Slow tracking shot alongside in calm air, bright sun. `[VIDEO SAFE]` |
| S37 | "Now imagine that at night, in bad weather…" | — none | AI direct | Night over a frozen Arctic sea under a violent storm, a huge generic bomber only as a tiny dark distant silhouette against lightning, faint tracer fire in the clouds, ominous. `[FILM LOOK]` | Lightning flickers, storm clouds roll, snow streaks past the camera. Add an "Illustration" label. |

### What killed it

| Shot | Script | Upload | Type | Notes |
|---|---|---|---|---|
| S38 | "By 1949 the Air Force had a better idea… much further." | — none | ARCH **A5** (first use) | — |
| S39 | "The Goblin programme was cancelled. Only two were ever built." | ♻ **S35-tally** (the board from S35) | GFX | Stamp "CANCELLED · 1949" over it. |
| S40 | "Both survive today… Ohio… Nebraska." | — none | ARCH **R5** + **R6** (first use) | Split screen or two Ken Burns zooms. Never AI. |

### What it led to

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S41 | "In the 1950s the Air Force tried it again…" | — none | ARCH **A6** (first use) | — | — |
| S42 | "…the small ones are drones, with no pilot hanging under a hook." | — none | AI direct | A large modern grey military transport plane in flight at sunset above clouds, a small sleek unmarked drone approaching beneath it, no insignia. `[FILM LOOK]` | The drone rises slowly toward the transport's belly, clouds drift below. Add an "Illustration" label. |

### The payoff

| Shot | Script | Upload | Type | Image prompt | Video prompt |
|---|---|---|---|---|---|
| S43 | "Which brings us back to the question… no landing gear?" | ♻ **M1**, same as S01, S20 | REUSE | — | Same as S01, but orbit to the left. `[VIDEO SAFE]` |
| S44 | "Because its landing gear wasn't meant to be on the fighter at all… the other side of the world." | ♻ **M5**, same as S08–S18, **+** ♻ **M1**, same as S01, S20, S43 | NEW, 2–3 clips | `[B-36 LOCK]` Ghosted semi-transparent X-ray view, the small jet from the second reference visible inside the bomb bay, blueprint glow in amber and steel blue. `[STUDIO LOOK]` | Slow pull-back. `[VIDEO SAFE]` ⚠ **weak in AI**. Finish with ♻ **S11-map** (the map from S11). |
| S45 | "And that's also why it failed… more often than it worked." | ♻ **M2**, same as S02–S23 | REUSE | — | Slow push-in onto the hook. `[VIDEO SAFE]` |
| S46 | "Landing gear would have made the Goblin heavier. Having none made it helpless." | ♻ **M2** | NEW → save as **S46.png** | `[GOBLIN LOCK]` Only the nose and hook visible, lit by one amber rim light, everything else fading into pure black. `[STUDIO LOOK]` | Almost still, the light slowly brightening on the hook. `[VIDEO SAFE]` |

### Ending

| Shot | Script | Upload | Type | Notes |
|---|---|---|---|---|
| S47 | "Today, the Goblin in Ohio sits on a stand, its hook still raised…" | — none | ARCH ♻ **R5**, same as S40 | Slow push-in on the hook in the real photo. Never AI. |
| S48 | "Every strange aircraft is the answer to a problem. That's what this channel is about…" | ♻ **S46.png** (the hook-in-the-dark image from S46) | REUSE | Slow pull-back as the amber light fades, then the channel logo fades in. `[VIDEO SAFE]` |
| S49 | "And the Goblin isn't the strangest one… looking over his shoulder." | — none | ARCH **A7** (first use) | The real Pogo film. Never AI. |
| S50 | "That's next. Subscribe so you're here when it lands." | — none | GFX end screen | A graphite card with a subscribe button and a "next video" slot. Hold it 10–15 s under music. |

---

## Step 5. Fallbacks for shots AI handles badly

| Problem | Shots | Fallback |
|---|---|---|
| Wings folding | S20 | Never animate it. Cross-dissolve M1 (folded) into M2 (spread). |
| X-ray see-through | S22, S25, S44 | Use the plain M2/M5 still, lower its opacity in CapCut over a black copy, and draw the engine glow or bomb-bay outline yourself. |
| The bomb-bay box | S17 | Use the M2 still and draw a steel-blue rectangle around it in CapCut. |
| Propeller and engine counts | S08, S09, S13, S44 (B-36 = 6, B-29 = 4) | Count them in every frame. If they change, use a slow zoom on the approved still instead. |
| The trapeze or hook drifting | S04, S29–S32 | Re-roll. After two bad rolls, use archival A1 for that line. |
| The canopy shattering | S32 | If the glass morphs oddly, cut to a white flash plus the crack sound effect over the S24 image. |
| Wheels appearing | Any Goblin shot | Discard the clip. Never keep a Goblin with wheels. |

---

## Step 6. Reference tracker: every image, and every shot that reuses it

Use this to check you're uploading the same file each time.

| Image | Made from | First used | Reused in |
|---|---|---|---|
| **R1** | download | M1 | — |
| **R2** | download | M2 | — |
| **R3** | download | M4 | S27 (as an archival still, optional) |
| **R4** | download | M5 | — |
| **M1** | R1 | M2 (as a reference) | S01, S20, S43, S44 |
| **M2** | R2 + M1 | M3 (as a reference) | S02, S03, S06, S07, S16, S17, S20, S21, S22, S23, S45, S46 |
| **M3** | M2 | M4 (as a reference) | S33, S36 |
| **M4** | R3 + M3 | S04 | S24, S28, S29, S30, S32 |
| **M5** | R4 | S08 | S09, S13, S18, S44 |
| **S02.png** | M2 | S02 | S26 |
| **S07.png** | M2 | S07 | S19 |
| **S22.png** | M2 | S22 | S25 |
| **S46.png** | M2 | S46 | S48 |
| **S29 clip, last frame** | S29 | S31 (CHAIN) | — |
| **S11-map** | CapCut/Canva | S11 | S44 |
| **S35-tally** | CapCut/Canva | S35 | S39 |
| **R5** (Ohio photo) | download | S40 | S47 |
| **A1** (1948 film) | download | S05 | S27, S34 |

**Nothing to upload:** S10, S12, S14, S15, S37, S38, S41, S42, S49, S50.

Name every approved image by its shot (`S22.png`) and keep the masters in a `masters` folder so you can reuse the studio look next video.
