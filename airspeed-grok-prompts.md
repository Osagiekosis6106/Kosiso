# Grok workflow: worked example (XF-85 video)

> **How to use this file.** It's the **format and method** for every Grok prompt pack: real photos → approved masters → lock text → REUSE / NEW / CHAIN per shot. The XF-85 content is only the example. Colours in `[STUDIO LOOK]` and the logo are placeholders until the user chooses the channel's palette (`airspeed-channel-kit.md`, section 3).

This file is for making video #1 (*Why Did This Fighter Have No Landing Gear?*) in **Grok Imagine** instead of Blender. Shot numbers (S01–S41) match the shot sheet in `airspeed-model.md`, section 11.

## How Grok works for this

1. **Make an image:** upload a reference image, then paste an **image prompt**.
2. **Check it** against the real photo. If it's wrong, generate again. Don't move on with a wrong image.
3. **Turn it into video:** use the approved image with Grok's video/"make video" option, then paste the **video prompt**. Grok clips are short (a few seconds). Trim each to 3–5 s in CapCut.

**The honest trade-off:** Grok is quicker to learn than Blender, but it can't keep an aircraft exactly the same from shot to shot. It may add a propeller, change the fins or move the hook. Three habits fix most of it:

- **Build a small set of approved "master images" first (Part 1). Every shot starts from one of them, never from a text-only prompt.** That's what keeps the plane looking the same all video.
- **Paste the same "lock" text (Part 2) into every prompt**, word for word.
- **Throw away any clip where the plane changes shape.** It's faster to re-roll than to fix.

Four shots are weak in AI: **wings folding (S16), X-ray see-through (S18, S21, S36), spinning propellers on the B-36 (S41) and the bomb-bay fit (S14).** Each one below has a simpler fallback.

### What "NEW" and "REUSE" mean below

- **NEW:** generate a new image first, using the reference listed, then make the video from that new image.
- **REUSE:** upload an image you've already approved (M1, M2…) and go straight to the video prompt. Don't generate a new image.
- **CHAIN:** screenshot the **last frame** of the previous clip and use it as the start image, so two shots join smoothly.

Rule: **always reuse a master (M-image) rather than a frame from an earlier video.** Each generation drifts a little, so copying copies drifts further.

---

## Camera-move vocabulary (mix these into video prompts)

slow cinematic orbit · slow push-in · slow pull-back · low-angle dolly past the nose · tracking shot alongside in flight · top-down rotating overhead · slow tilt-up from the belly · static hero shot with subtle parallax. Keep calm documentary pacing, smooth motion, and 3–5 seconds per shot.

## Part 0. Download the real photos first (your "truth")

Save these in a folder called `XF85-refs`. They're the reference uploads for the masters and the photos you compare every result against.

| Save as | What | Where to find it | Search |
|---|---|---|---|
| **R1** | XF-85 front or front-3/4 photo | National Museum of the USAF (nationalmuseum.af.mil), Wikimedia Commons | `XF-85 Goblin` |
| **R2** | XF-85 side view, wings spread | Same | `XF-85 Goblin side` |
| **R3** | XF-85 hanging on the trapeze under the EB-29B | Same, or NARA (catalog.archives.gov) | `XF-85 EB-29B trapeze` |
| **R4** | Early B-36 in flight (six propellers, **no jet pods**) | Wikimedia, NARA, SDASM Flickr | `B-36B Peacemaker` |

US Air Force photos are usually public domain, but check the licence line on each file.

---

## Part 1. Build your master images (do this once, before any shot)

Paste the **lock text** from Part 2 where it says `[GOBLIN LOCK]` etc.

| Master | Upload as reference | Image prompt |
|---|---|---|
| **M1** Goblin, studio, head-on, wings spread | R1 (cleaned museum photo) | `[GOBLIN LOCK]` Head-on view, perfectly centred and symmetrical, wings spread exactly as in the reference, hook raised above the nose, hovering just above the studio floor, no stand, no wheels, no landing gear. `[STUDIO LOOK]` |
| **M2** Goblin, studio, front-3/4, wings spread | R2 **+ M1** | `[GOBLIN LOCK]` Front three-quarter view from the left, wings spread out, hook raised. Same aircraft as the second reference image. `[STUDIO LOOK]` |
| **M3** Goblin, flying, side view | M2 | `[GOBLIN LOCK]` In flight, side view, wings spread, hook folded down, clear blue sky above a 1940s California desert far below. `[FILM LOOK]` |
| **M4** The mother ship: B-29 with the Goblin on the trapeze | R3 **+ M3** | `[B-29 LOCK]` Seen from below and behind in flight, a steel trapeze lowered from the bomb bay with the small jet from the second reference hanging from it by its nose hook. Desert far below. `[FILM LOOK]` |
| **M5** B-36 in flight | R4 | `[B-36 LOCK]` Side view in flight, high above the clouds, midday light. `[FILM LOOK]` |
| **M6** B-36 at dusk | M5 | `[B-36 LOCK]` Same aircraft as the reference, three-quarter rear view at sunset, orange sky, propellers blurred into discs. `[FILM LOOK]` |

**Check every master before using it (⚠ VERIFY):**
- **M1 and M2:** the hook's shape and position, the wings fold *upward*, the number and angle of tail fins, the bubble canopy, and the nose intake. All must match R1 and R2.
- **M4:** the trapeze looks like R3.
- **M5 and M6:** six propellers **behind** the wing, no jet pods.

Only approved masters go into the shots.

---

## Part 2. Lock text (paste word for word, every time)

**`[GOBLIN LOCK]`**
> The McDonnell XF-85 Goblin, a tiny 1948 experimental jet fighter exactly like the reference image: short egg-shaped polished-aluminium fuselage, bubble canopy near the nose, a single steel hook on top of the nose in front of the canopy, small swept wings, a cluster of small tail fins at the rear exactly as in the reference, USAF markings, no landing gear, no wheels, no propeller.

**`[B-29 LOCK]`**
> A 1940s Boeing B-29 Superfortress bomber exactly like the reference: polished aluminium, long rounded glass nose, four propeller engines on a long straight wing, one tall tail fin.

**`[B-36 LOCK]`**
> An early Convair B-36 bomber exactly like the reference: enormous straight wings, polished aluminium, exactly six propeller engines mounted on the back edge of the wing with propellers facing backward, no jet pods, tall single tail.

**`[STUDIO LOOK]`**
> Photoreal 3D product render, dark [BACKGROUND]-to-[ACCENT] gradient studio background, soft white key light from the front, [ACCENT] and [SECOND COLOUR] rim lights from behind, glossy reflective floor, sharp focus, 16:9, no text.

**`[FILM LOOK]`**
> Photoreal cinematic 3D render, 1940s colour film look, muted Kodachrome colours, soft film grain, 16:9, no text.

**`[VIDEO SAFE]`** (end every video prompt with this)
> Keep the aircraft's shape, fins, hook, wings, markings and number of engines and propellers exactly as in the image. No morphing, no extra parts. Realistic motion blur. Smooth motion.

---

## Part 3. Shot by shot

⚠ = check the result against the real photo (R1–R4) before you keep it. **Disc ON** = switch on YouTube's "altered or synthetic content" at upload for this video.

### Cold open

| Shot | Start image | Image prompt (only if NEW) | Video prompt |
|---|---|---|---|
| **S01** studio turntable | **REUSE M1** | — | Slow smooth orbit around the aircraft, a quarter turn to the right, lights glinting on the metal. `[VIDEO SAFE]` ⚠ |
| **S02** under the belly | **NEW** from M2 | `[GOBLIN LOCK]` Low camera looking up at the smooth underside from below: no wheels and no wheel wells, only a thin steel skid along the belly. `[STUDIO LOOK]` | Slow sideways slide under the belly, close macro shot. `[VIDEO SAFE]` ⚠ skid shape |
| **S03** hook reveal | **REUSE M2** | — | Slow pull-back from a close-up of the hook on top of the nose to a full view of the aircraft. `[VIDEO SAFE]` ⚠ |
| **S04** drop from the bomber · **Disc ON** | **REUSE M4** | — | The small jet releases from the trapeze and drops smoothly away below the bomber, the bomber flies on straight, clouds drift below. `[VIDEO SAFE]` ⚠ |

### The problem of the era

| Shot | Start image | Image prompt | Video prompt |
|---|---|---|---|
| **S07** B-36 wing | **REUSE M5** | — | Slow camera track along the enormous wing from the fuselage to the wingtip. `[VIDEO SAFE]` ⚠ six props, no jets |
| **S10** lone bomber | **NEW** from M5 | `[B-36 LOCK]` Small in the lower third of the frame, flying alone across a vast empty pale sky. `[FILM LOOK]` | Very slow drift to the right, the bomber crosses left to right, thin clouds below. `[VIDEO SAFE]` |

### Partial answer and walkaround

| Shot | Start image | Image prompt | Video prompt |
|---|---|---|---|
| **S13** "no wheels" | **REUSE M2** | — | Slow orbit to the left. *(In CapCut, draw glowing outlines where wheels would be, then fade them out.)* `[VIDEO SAFE]` |
| **S14** bomb bay fit | **NEW** from M2 | `[GOBLIN LOCK]` Sitting inside a glowing blue wireframe outline of a narrow bomber bomb bay, only a hand's width of space around it, blueprint style. `[STUDIO LOOK]` | Slow push-in. `[VIDEO SAFE]` ⚠ **Weak in AI.** Fallback: M2 still plus a rectangle drawn in CapCut |
| **S15** scale | **NEW** from M2 | `[GOBLIN LOCK]` Standing on the studio floor beside a grey faceless 1.8 m human mannequin and a 1940s family car for scale, the jet slightly shorter than the car. `[STUDIO LOOK]` | Slow pan from left to right across all three. `[VIDEO SAFE]` ⚠ sizes: Goblin ~4.5 m long |
| **S16** wings unfold | **Archival first** | — | **Weak in AI; don't ask Grok to fold the wings.** M1 is now wings-spread (it matches the real R1 photo), so the M1-to-M2 cross-dissolve no longer shows a fold. Use a real photo or film of the Goblin with its wings folded if you find one. Otherwise skip the fold visual and hold on M2 while the line plays. |
| **S17** tail fins | **NEW** from M2 | `[GOBLIN LOCK]` Rear three-quarter close-up of the cluster of tail fins and the jet exhaust. `[STUDIO LOOK]` | Slow orbit around the tail. `[VIDEO SAFE]` ⚠ fin count vs R2 |
| **S18** X-ray engine | **NEW** from M2 | `[GOBLIN LOCK]` Ghosted semi-transparent X-ray cutaway: the aluminium skin see-through like glass, a single jet engine inside glowing orange running from the nose intake to the tail exhaust. `[STUDIO LOOK]` | Slow orbit, the orange glow pulses gently. `[VIDEO SAFE]` ⚠ **weak in AI**. Fallback: M2 with an orange glow drawn in CapCut |
| **S19** guns | **NEW** from M2 | `[GOBLIN LOCK]` Extreme close-up of the nose showing the machine-gun ports. `[STUDIO LOOK]` | Slow slide along the nose. `[VIDEO SAFE]` ⚠ 4 guns and port positions |
| **S20** cockpit, looking up | **NEW** from M4 | Point-of-view from inside the tiny cockpit of the jet in the reference, looking up through the bubble canopy at the steel hook and the silver bomber belly just above. `[FILM LOOK]` | Small shakes as if in rough air, light streaks across the canopy. `[VIDEO SAFE]` ⚠ canopy frame |
| **S21** "no gear" X-ray | **REUSE S18 image** | — | **Weak in AI.** Use the S18 image and animate red wheel and strut icons bouncing off it in CapCut. No Grok video needed. |

### The test (thriller section)

| Shot | Start image | Image prompt | Video prompt |
|---|---|---|---|
| **S23** under the bomber *(only if you find no archival film)* · **Disc ON** | **REUSE M4** | — | Slow drift alongside, both aircraft steady. `[VIDEO SAFE]` |
| **S24** release and engine start · **Disc ON** | **NEW** from M4 | `[GOBLIN LOCK]` Side view just below the bomber's trapeze, falling away, a faint orange glow in its tail exhaust. `[FILM LOOK]` | The jet falls a short way, its exhaust flares orange with heat shimmer, it levels off. Camera tracks alongside. `[VIDEO SAFE]` ⚠ |
| **S25** turbulence · **Disc ON** | **NEW** from M4 | `[B-29 LOCK]` Close-up under the belly and the steel trapeze bar, clouds racing below, visible churning air. `[FILM LOOK]` | Heat-haze ripples under the belly, the trapeze bar swings and shakes, camera shakes. `[VIDEO SAFE]` |
| **S26** the approach · **Disc ON** | **CHAIN** (last frame of S24) | — | The small jet rises and bounces toward the swinging trapeze bar, rocking side to side in rough air. `[VIDEO SAFE]` ⚠ |
| **S27** canopy hit · **Disc ON** | **NEW** from M4 | `[GOBLIN LOCK]` Extreme close-up of the bubble canopy with the steel trapeze bar a few centimetres away. `[FILM LOOK]` | The bar strikes the canopy, the glass cracks and shatters outward in slow motion. `[VIDEO SAFE]` ⚠ event details |
| **S28** belly landing · **Disc ON** | **NEW** from M3 | `[GOBLIN LOCK]` A metre above a vast cracked dry lakebed in the Mojave desert at golden hour, 1948, long shadows, about to touch down on its belly skid. `[FILM LOOK]` | The jet touches down on its belly and slides across the lakebed throwing up a long plume of dust, slowing to a stop. Camera tracks low alongside. No wheels. `[VIDEO SAFE]` ⚠ |

### "Imagine that…" (AI direct: no reference image)

| Shot | Start image | Image prompt | Video prompt |
|---|---|---|---|
| **S31** Arctic night | **NEW, no reference** | Night over a frozen Arctic sea under a violent storm, a huge bomber only as a tiny dark distant silhouette against lightning, faint tracer fire in the clouds, ominous. `[FILM LOOK]` | Lightning flickers, storm clouds roll, snow streaks past the camera. Add an on-screen "Illustration" label in the edit. |

### Payoff and ending

| Shot | Start image | Image prompt | Video prompt |
|---|---|---|---|
| **S35** back to the studio | **REUSE M1** | — | Same as S01 but orbit to the left. `[VIDEO SAFE]` |
| **S36** X-ray bomber | **NEW** from M5 **+ M1** | `[B-36 LOCK]` Ghosted semi-transparent X-ray view, the small jet from the second reference visible inside the bomb bay, blueprint glow. `[STUDIO LOOK]` | Slow pull-back. `[VIDEO SAFE]` ⚠ **weak in AI**. Fallback: M5 with M1 cut out and placed over it in CapCut |
| **S37** push-in on hook | **REUSE M2** | — | Slow push-in onto the hook on top of the nose. `[VIDEO SAFE]` |
| **S38** hook in the dark | **NEW** from M2 | `[GOBLIN LOCK]` Only the nose and hook visible, lit by one [ACCENT] rim light, everything else fading into pure black. `[STUDIO LOOK]` | Almost still, the light slowly brightens on the hook. `[VIDEO SAFE]` |
| **S40** modern drones *(only if you don't name a real programme)* | **NEW, no reference** | A large modern grey military transport plane in flight at sunset above clouds, a small sleek unmarked drone approaching beneath it, no insignia. `[FILM LOOK]` | The drone rises slowly toward the transport's belly, clouds drift below. |
| **S41** B-36 tease | **REUSE M6** | — | Slow push-in from behind, the six propellers spinning as blurred discs behind the wing. `[VIDEO SAFE]` ⚠ **Weak in AI**: count the propellers in every frame. If they change, use a slow zoom on the M6 still instead. |

Archival and graphics shots (S05, S06, S08, S09, S11, S12, S22, S29, S30, S32–S34, S39) are unchanged. See the table in `airspeed-model.md`.

---

## Quick reference: what to upload for each shot

| Upload | Shots |
|---|---|
| **M1** (reuse) | S01, S16 (part 1), S35 |
| **M2** (reuse) | S03, S13, S16 (part 2), S37 |
| **M4** (reuse) | S04, S23 |
| **M5** (reuse) | S07 |
| **M6** (reuse) | S41 |
| **NEW from M2** | S02, S14, S15, S17, S18, S19, S38 |
| **NEW from M3** | S28 |
| **NEW from M4** | S20, S24, S25, S27 |
| **NEW from M5** | S10 |
| **NEW from M5 + M1** | S36 |
| **CHAIN** (last frame of the previous clip) | S26 (after S24) |
| **Reuse an earlier shot's image** | S21 (the S18 image) |
| **NEW, no reference** (AI direct) | S31, S40 |

Keep every approved image in a folder named `masters`, and name every file by shot (`S18.png`), so next video you can reuse your studio look straight away.
