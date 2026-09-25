# XF-85 Goblin: Grok prompt pack (final script)

For *Why Did This Fighter Have No Landing Gear?*, final script (Ohio ending, tail-sitter tease). This replaces the shot list in `airspeed-grok-prompts.md` for this video. The method is the same: build masters first, then make every shot from a master.

**Key:**
- **REUSE**: upload an approved master and go straight to the video prompt.
- **NEW**: generate a new image from the named master first, then make the video from it.
- **CHAIN**: use the last frame of the previous clip as the start image.
- **ARCH**: real archival footage or photos, so no Grok.
- **GFX**: a graphic made in CapCut or Canva, so no Grok.
- ⚠ = check the result against the real photo before you keep it.
- **Disc ON** = switch on YouTube's "altered or synthetic content" setting at upload.

**Hard rules:** never make an AI version of Edwin Schoch or any real person. Never make an AI version of the Convair Pogo, the Sparrowhawk, the TB-3, the Boeing 747 or the museum Goblins. Those shots are real footage or graphics only.

---

## 1. Real photos and footage to download

Put them in a folder called `XF85-refs`. US Air Force, NARA and Navy material is usually public domain, but check the licence line on each file.

| Save as | What | Where | Search |
|---|---|---|---|
| **R1** | XF-85 front or front-3/4 photo | nationalmuseum.af.mil, Wikimedia Commons | `XF-85 Goblin` |
| **R2** | XF-85 side view, wings spread | Same | `XF-85 Goblin side` |
| **R3** | XF-85 on the trapeze under the EB-29B | Same, or catalog.archives.gov | `XF-85 EB-29B trapeze` |
| **R4** | Early B-36 in flight (six propellers, **no jet pods**) | Wikimedia, NARA, SDASM Flickr | `B-36B Peacemaker` |
| **R5** | The Ohio Goblin on its stand, hook raised | nationalmuseum.af.mil | `XF-85 Goblin museum` |
| **R6** | The Nebraska Goblin | sacmuseum.org, Wikimedia | `XF-85 SAC Aerospace Museum` |
| **A1** | 1948 Goblin/EB-29B test film | NARA; the San Diego Air & Space Museum's YouTube channel (film "MF 6") | `XF-85 Goblin film 1948` |
| **A2** | USS Macon or Akron catching a Sparrowhawk | NARA, Naval History and Heritage Command | `F9C Sparrowhawk trapeze` |
| **A3** | Zveno TB-3 carrying fighters | Wikimedia Commons | `Zveno TB-3` |
| **A4** | B-29 formations and flak, 1944–45 | NARA, Wikimedia | `B-29 formation 1945` |
| **A5** | A 1949 mid-air refuelling | NARA | `KB-29 refueling 1949` |
| **A6** | FICON: an RF-84K under a GRB-36 | NARA, SDASM | `FICON RF-84K GRB-36` |
| **A7** | Convair XFY-1 Pogo taking off or landing | SDASM (film "F-0645"), NARA | `XFY-1 Pogo` |

---

## 2. Master images (make and approve these first)

| Master | Upload | Image prompt |
|---|---|---|
| **M1** Goblin, studio, head-on, wings folded | R1 | `[GOBLIN LOCK]` Head-on view, perfectly centred and symmetrical, wings folded upward, hook raised above the nose. `[STUDIO LOOK]` |
| **M2** Goblin, studio, front-3/4, wings spread | R2 + M1 | `[GOBLIN LOCK]` Front three-quarter view from the left, wings spread out, hook raised. Same aircraft as the second reference image. `[STUDIO LOOK]` |
| **M3** Goblin in flight, side view | M2 | `[GOBLIN LOCK]` In flight, side view, wings spread, hook folded down, clear blue sky above a 1940s California desert far below. `[FILM LOOK]` |
| **M4** EB-29B with the Goblin on the trapeze | R3 + M3 | `[B-29 LOCK]` Seen from below and behind in flight, a steel trapeze lowered from the bomb bay with the small jet from the second reference hanging from it by its nose hook. Desert far below. `[FILM LOOK]` |
| **M5** B-36 in flight | R4 | `[B-36 LOCK]` Side view in flight, high above the clouds, midday light. `[FILM LOOK]` |

**Before approving (⚠):**
- **M1 and M2:** hook shape and position, wings folding *upward*, the number of tail fins, the bubble canopy, the nose intake, and **no wheels**.
- **M4:** the trapeze matches R3, and the B-29 has **four** engines.
- **M5:** **six** propellers *behind* the wing, and no jet pods.

---

## 3. Lock text (paste word for word, every time)

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

## 4. Shot by shot

Each Grok clip is 3–5 s; trim it in CapCut. Where a line needs more time, make 2 clips from the same start image with different camera moves.

### Cold open

| Shot | Script | Type | Image prompt (NEW only) | Video prompt |
|---|---|---|---|---|
| S01 | "Why would anyone build a fighter jet with no landing gear?" | **REUSE M1** | — | Slow smooth orbit, a quarter turn to the right, light glinting on the metal. `[VIDEO SAFE]` ⚠ |
| S02 | "Not small wheels… No wheels at all." | **NEW** from M2 | `[GOBLIN LOCK]` Low camera looking up at the smooth underside from below: no wheels and no wheel wells, only a thin steel skid along the belly. `[STUDIO LOOK]` | Slow sideways slide under the belly, close macro shot. `[VIDEO SAFE]` ⚠ skid |
| S03 | "Just a hook… on the top of its nose." | **REUSE M2** | — | Slow pull-back from a close-up of the hook to the full aircraft. `[VIDEO SAFE]` |
| S04 | "Because this fighter was never supposed to… over 200 miles an hour." · **Disc ON** | **REUSE M4** (2 clips) | — | Clip 1: slow drift alongside, both aircraft steady. Clip 2: the small jet releases and drops smoothly away, the bomber flies on. `[VIDEO SAFE]` ⚠ |
| S05 | "And the first time a pilot tried to fly back to it…" | **ARCH** A1 | — | — |

### Stakes

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S06 | "This is the McDonnell XF-85 Goblin, the smallest American jet fighter ever built." | **REUSE M2** + GFX title card "XF-85 GOBLIN · 1948" | — | Very slow push-in, almost still. `[VIDEO SAFE]` |
| S07 | "about the length of a family car, and shaped like an egg with wings." | **NEW** from M2 | `[GOBLIN LOCK]` Standing on the studio floor beside a grey faceless 1.8 m human mannequin and a generic 1940s family car for scale, the jet about the same length as the car. `[STUDIO LOOK]` | Slow pan from left to right across all three. `[VIDEO SAFE]` ⚠ sizes |
| S08 | "It only makes sense once you understand the problem… inside its bombers." | **REUSE M5** | — | Slow push-in toward the bomber's belly. `[VIDEO SAFE]` ⚠ six props |

### The problem of the era

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S09 | "At the end of World War Two… and back without landing." | **REUSE M5** | — | Slow track along the wing from the fuselage to the wingtip. `[VIDEO SAFE]` ⚠ six props, no jets |
| S10 | "Its wingspan was about 70 metres… wider than a Boeing 747's." | **GFX** | — | Flat top-view silhouettes: B-36 over 747, with a 230 ft / 70 m label. |
| S11 | "The B-36 could fly for well over a day… a fraction of the way." | **GFX** | — | Map: a long bomber arc across the Arctic and a small fighter-range circle stopping near the coast. |
| S12 | "Every bomber crew of the last war… terrible losses." | **ARCH** A4 | — | — |
| S13 | "So the Air Force asked a strange question… carry the fighter?" | **NEW** from M5 | `[B-36 LOCK]` Small in the lower third of the frame, flying alone across a vast empty pale sky. `[FILM LOOK]` | Very slow drift, the bomber crosses left to right, thin clouds below. `[VIDEO SAFE]` |

### "It wasn't a new idea"

| Shot | Script | Type | Notes |
|---|---|---|---|
| S14 | "In the 1930s the US Navy flew giant airships…" | **ARCH** A2 | Never AI (a real aircraft). |
| S15 | "The Soviet Union went further… real combat missions." | **ARCH** A3 | Slow Ken Burns zoom on the photo. |

### Partial answer and walkaround

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S16 | "So the obvious answer is… only half the story." | **REUSE M2** | — | Slow orbit to the left. `[VIDEO SAFE]` In CapCut: glowing outlines where wheels would be, fading out. |
| S17 | "…comes down to one number… no more than about 15 feet long." | **NEW** from M2 | `[GOBLIN LOCK]` Sitting inside a glowing steel-blue wireframe box, only a narrow gap at the nose and tail, blueprint style. `[STUDIO LOOK]` | Slow push-in. `[VIDEO SAFE]` In CapCut, add the label "≈ 15 ft limit". ⚠ **weak in AI**, see fallbacks |
| S18 | "The fighter had to fit inside the B-36… had to go." | **REUSE M5** still + GFX | — | In CapCut: a slow zoom on the still, with the bomb-bay area outlined in amber. |
| S19 | "The result was 14 feet 10 inches… family car." | **REUSE S07 image** | — | Slow pan the other way. In CapCut: label "14 ft 10 in · 4.52 m". `[VIDEO SAFE]` |
| S20 | "The wings folded upward… 21 feet." | **REUSE M1**, then **REUSE M2** | — | 1 s tiny push-in on M1, cross-dissolve into 1 s on M2, then label "21 ft · 6.4 m". Don't ask Grok to fold the wings. |
| S21 | "The tail was so cramped… almost no length." | **NEW** from M2 | `[GOBLIN LOCK]` Rear three-quarter close-up of the cluster of tail fins and the jet exhaust. `[STUDIO LOOK]` | Slow orbit around the tail. `[VIDEO SAFE]` ⚠ fin count vs R2 |
| S22 | "Inside that egg was a single Westinghouse J34… 650 miles an hour." | **NEW** from M2 (2 clips) | `[GOBLIN LOCK]` Ghosted semi-transparent X-ray cutaway: the aluminium skin see-through like glass, a single jet engine inside glowing orange from the nose intake to the tail exhaust. `[STUDIO LOOK]` | Slow orbit, the orange glow pulsing gently. `[VIDEO SAFE]` ⚠ **weak in AI** |
| S23 | "It was designed to carry four .50-calibre machine guns…" | **NEW** from M2 | `[GOBLIN LOCK]` Extreme close-up of the nose showing the machine-gun ports. `[STUDIO LOOK]` | Slow slide along the nose. `[VIDEO SAFE]` ⚠ 4 ports |
| S24 | "And the pilot sat in a seat with an ejection system… his only way home." | **NEW** from M4 | Point of view from inside the tiny cockpit of the jet in the reference, looking up through the bubble canopy at the steel hook and the silver bomber belly just above. No people visible. `[FILM LOOK]` | Small shakes as if in rough air, light streaks across the canopy. `[VIDEO SAFE]` |
| S25 | "Landing gear would have meant… already squeezed into a box." | **REUSE S22 image** | — | No Grok video. In CapCut: red wheel and strut icons float in and bounce off the steel-blue box outline. |
| S26 | "So the engineers took it out… a steel skid underneath for emergencies." | **REUSE S02 image** | — | Slow slide the other way along the belly. `[VIDEO SAFE]` |

### The test

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S27 | "The B-36 wasn't ready… after the whale that swallowed Pinocchio." | **ARCH** A1 / R3 | — | — |
| S28 | "The pilot was McDonnell test pilot Edwin Schoch… in flight." | **ARCH** a period photo if you find one, otherwise **REUSE M4** · Disc ON | — | Slow drift alongside. `[VIDEO SAFE]` Never an AI face. |
| S29 | "On the 23rd of August 1948, Schoch dropped free." · **Disc ON** | **NEW** from M4 | `[GOBLIN LOCK]` Side view just below the bomber's trapeze, falling away, a faint orange glow in its tail exhaust. `[FILM LOOK]` | The jet falls a short way, its exhaust flares orange with heat shimmer, then it levels off. Camera tracks alongside. `[VIDEO SAFE]` ⚠ |
| S30 | "But the air under a four-engine bomber isn't still…" · **Disc ON** | **NEW** from M4 | `[B-29 LOCK]` Close-up under the belly and the steel trapeze bar, clouds racing below, visible churning air. `[FILM LOOK]` | Heat-haze ripples under the belly, the trapeze bar swings and shakes, the camera shakes. `[VIDEO SAFE]` |
| S31 | "Schoch closed in. The Goblin bounced. The trapeze swung…" · **Disc ON** | **CHAIN** from S29 | — | The small jet rises and bounces toward the swinging trapeze bar, rocking side to side. `[VIDEO SAFE]` ⚠ |
| S32 | "…and the bar hit his canopy…" · **Disc ON** | **NEW** from M4 | `[GOBLIN LOCK]` Extreme close-up of the bubble canopy with the steel trapeze bar a few centimetres away. No pilot face visible. `[FILM LOOK]` | The bar strikes the canopy, the glass cracks and shatters outward in slow motion. `[VIDEO SAFE]` |
| S33 | "He flew down to the dry lakebed… He survived." · **Disc ON** | **NEW** from M3 | `[GOBLIN LOCK]` A metre above a vast cracked dry lakebed in the Mojave desert at golden hour, 1948, long shadows, about to touch down on its belly skid. `[FILM LOOK]` | It touches down on its belly and slides across the lakebed throwing a long plume of dust, slowing to a stop. Camera low alongside. No wheels. `[VIDEO SAFE]` ⚠ |
| S34 | "Weeks later, in October 1948, a Goblin finally hooked back…" | **ARCH** A1 | — | — |
| S35 | "Over the whole programme there were seven free flights…" | **GFX** | — | A tally board of 7 flights; ✓ ✗ marks fill in one by one (3 ✓). |
| S36 | "These were test pilots in clear California weather…" | **REUSE M3** | — | Slow tracking shot alongside in calm air, bright sun. `[VIDEO SAFE]` |
| S37 | "Now imagine that at night, in bad weather…" | **AI direct**, no reference | Night over a frozen Arctic sea under a violent storm, a huge generic bomber only as a tiny dark distant silhouette against lightning, faint tracer fire in the clouds, ominous. `[FILM LOOK]` | Lightning flickers, storm clouds roll, snow streaks past the camera. Add an "Illustration" label in the edit. |

### What killed it

| Shot | Script | Type | Notes |
|---|---|---|---|
| S38 | "By 1949 the Air Force had a better idea… much further." | **ARCH** A5 | — |
| S39 | "The Goblin programme was cancelled. Only two were ever built." | **GFX** | "CANCELLED · 1949" stamped over the S35 tally board. |
| S40 | "Both survive today… Ohio… Nebraska." | **ARCH** R5, then R6 | Split screen or two Ken Burns zooms. Never AI. |

### What it led to

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S41 | "In the 1950s the Air Force tried it again…" | **ARCH** A6 | — | — |
| S42 | "…the small ones are drones, with no pilot hanging under a hook." | **AI direct**, no reference | A large modern grey military transport plane in flight at sunset above clouds, a small sleek unmarked drone approaching beneath it, no insignia. `[FILM LOOK]` | The drone rises slowly toward the transport's belly, clouds drift below. Add an "Illustration" label. |

### The payoff

| Shot | Script | Type | Image prompt | Video prompt |
|---|---|---|---|---|
| S43 | "Which brings us back to the question… no landing gear?" | **REUSE M1** | — | Same as S01, but orbit to the left. `[VIDEO SAFE]` |
| S44 | "Because its landing gear wasn't meant to be on the fighter at all… the other side of the world." | **NEW** from M5 + M1 (2–3 clips) | `[B-36 LOCK]` Ghosted semi-transparent X-ray view, the small jet from the second reference visible inside the bomb bay, blueprint glow in amber and steel blue. `[STUDIO LOOK]` | Slow pull-back. `[VIDEO SAFE]` ⚠ **weak in AI**. Finish with the S11 map arc. |
| S45 | "And that's also why it failed… more often than it worked." | **REUSE M2** | — | Slow push-in onto the hook. `[VIDEO SAFE]` |
| S46 | "Landing gear would have made the Goblin heavier. Having none made it helpless." | **NEW** from M2 | `[GOBLIN LOCK]` Only the nose and hook visible, lit by one amber rim light, everything else fading into pure black. `[STUDIO LOOK]` | Almost still, the light slowly brightening on the hook. `[VIDEO SAFE]` |

### Ending

| Shot | Script | Type | Notes |
|---|---|---|---|
| S47 | "Today, the Goblin in Ohio sits on a stand, its hook still raised…" | **ARCH** R5 | Slow push-in on the hook in the real museum photo. Never AI. |
| S48 | "Every strange aircraft is the answer to a problem. That's what this channel is about…" | **REUSE S46 image** | Slow pull-back as the amber light fades, then the channel logo fades in. `[VIDEO SAFE]` |
| S49 | "And the Goblin isn't the strangest one… looking over his shoulder." | **ARCH** A7 | The real Pogo film, rising off its tail. Never AI. |
| S50 | "That's next. Subscribe so you're here when it lands." | **GFX** end screen | A graphite card with a subscribe button and a "next video" slot. Hold it 10–15 s under music; YouTube end screens need at least 5 s. |

---

## 5. Fallbacks for shots AI handles badly

| Problem | Shots | Fallback |
|---|---|---|
| Wings folding | S20 | Never animate it. Cross-dissolve M1 (folded) into M2 (spread). |
| X-ray see-through | S22, S25, S44 | Use the plain M2/M5 still, lower its opacity in CapCut over a black copy, and draw the engine glow or bomb-bay outline yourself. |
| The bomb-bay box | S17 | Use the M2 still and draw a steel-blue rectangle around it in CapCut. |
| Propeller and engine counts | S08, S09, S13, S44 (B-36 = 6, B-29 = 4) | Count them in every frame. If they change, use a slow zoom on the approved still instead of a video. |
| The trapeze or hook drifting | S04, S29–S32 | Re-roll. After two bad rolls, use archival A1 for that line. |
| The canopy shattering | S32 | If the glass morphs oddly, cut to a fast white flash plus the crack sound effect over the S24 image. |
| Wheels appearing | Any Goblin shot | Discard the clip. Never keep a Goblin with wheels. |

---

## 6. What to upload for each shot

| Upload | Shots |
|---|---|
| **M1** (reuse) | S01, S20 (part 1), S43 |
| **M2** (reuse) | S03, S06, S16, S20 (part 2), S45 |
| **M3** (reuse) | S36 |
| **M4** (reuse) | S04, S28 (if there's no photo) |
| **M5** (reuse) | S08, S09, S18 (still) |
| **NEW from M2** | S02, S07, S17, S21, S22, S23, S46 |
| **NEW from M3** | S33 |
| **NEW from M4** | S24, S29, S30, S32 |
| **NEW from M5** | S13 |
| **NEW from M5 + M1** | S44 |
| **CHAIN** | S31 (from S29) |
| **An earlier shot's approved image** | S19 (S07), S25 (S22), S26 (S02), S48 (S46) |
| **AI direct**, no reference | S37, S42 |
| **Archival** | S05, S12, S14, S15, S27, S28, S34, S38, S40, S41, S47, S49 |
| **Graphics** | S06 (title), S10, S11, S35, S39, S50 |

Name every approved image by its shot (`S22.png`) and keep the masters in a `masters` folder so you can reuse the studio look next video.
