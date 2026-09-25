# Grok workflow: reference photo → video (worked example: XF-85)

> **How to use this file.** This is the **default method** for every Grok prompt pack. Prepare the real reference photos, then go **straight to video**: upload a reference, paste one video prompt, done. There's no image-generation step. Everything the old "master image" step did is merged into each video prompt. The XF-85 content is the worked example. Shot numbers (S01–S41) match the shot sheet in `airspeed-model.md`, section 11.

## How it works

1. **Upload the reference photo** named for the shot (R1–R5) in Grok's video / "make video" option.
2. **Paste the video prompt** for that shot, exactly as written. Every prompt already contains the aircraft description, the look and the no-morphing rules.
3. **Check the clip** against the real photo. Throw away any clip where the plane changes shape.
4. Trim each clip to 3–5 s in CapCut.

**Two rules that make this work:**

- **Your photo is the first frame.** Whatever is in the photo (background, colour, clutter) shows at the start of the clip. So **clean the reference first**: crop it, remove stands and clutter, put it on a plain dark background, as you did for R1. Cleaning an image is editing, not generating, so do it in Canva or with Magic Eraser.
- **Small camera moves stay accurate; big ones morph.** A slow orbit or push-in from the photo's angle keeps the real shape. Asking the camera to fly to a completely different angle (under the belly, inside the cockpit, into a desert) is where AI invents parts. Those shots are marked **⚠ weak** and have a fallback.

**Look plan (it solves consistency for free):**

- **Studio shots:** colour, dark graphite studio, from cleaned R1, R2 and R5.
- **The 1948 test section (drop, hook-ups, crash):** **black-and-white test-film look**, from the real B&W archival photos (R3). It looks authentic, and you don't need to colourise anything.
- **B-36 shots:** keep whatever R4 is (colour or B&W), and use the matching look line.

---

## Part 0. Prepare the reference photos (the only prep step)

| Save as | What | Where | Status / what to do |
|---|---|---|---|
| **R1** | XF-85 head-on, wings spread, hook raised | USAF Museum photo | ✅ **Approved** (cleaned: no stand, dark background, post under the nose removed) |
| **R2** | XF-85 side or front-3/4 view, wings spread | nationalmuseum.af.mil, Wikimedia Commons (`XF-85 Goblin side`) | Send it to be checked. Then clean it the same way as R1: plain dark background, no stand. |
| **R3** | XF-85 on the trapeze under the EB-29B | USAF Museum, NARA (`XF-85 EB-29B trapeze`) | Send it to be checked. Keep it black and white. |
| **R4** | Early B-36 in flight: six propellers behind the wing, **no jet pods** | Wikimedia, NARA, SDASM Flickr (`B-36B Peacemaker`) | Send it to be checked |
| **R5** | **Crop of R1**: just the nose, hook and canopy | Made from R1 (crop only, no AI) | Crop R1 tight around the nose and hook frame |

US Air Force and National Archives photos are usually public domain; check each file's licence line.

---

## Part 1. The lines already built into every prompt (for reference)

You don't need to paste these separately; they're already inside each shot's prompt. They're listed so you can reuse them for future aircraft.

- **Goblin lock:** *Keep the XF-85 Goblin exactly as in the image: egg-shaped polished-aluminium body, round nose intake, dark panel on top of the nose, bubble canopy, a short boxy dark hook frame on the nose just in front of the canopy, two upswept tail fins, a small fin on each wingtip, one star insignia, no wheels, no propeller.*
- **B-29 lock:** *Keep the B-29 exactly as in the image: four propeller engines, rounded glass nose, one tall tail fin, the trapeze under the bomb bay.*
- **B-36 lock:** *Keep the B-36 exactly as in the image: exactly six propellers mounted behind the wing, no jet pods, never add or remove engines.*
- **Studio look:** *Dark graphite studio, soft white key light, warm gold and steel-blue rim lights, glossy reflective floor, photoreal, 16:9.*
- **Test-film look:** *Black-and-white 1948 test film look, soft grain, gentle flicker, 16:9.*
- **Safe ending:** *No morphing, no extra parts, smooth realistic motion.*

---

## Part 2. Shot by shot: upload + one prompt

⚠ = check against the real photo before keeping it. **Disc ON** = switch on YouTube's "altered or synthetic content" at upload.

### Cold open

| Shot | Upload | Video prompt (paste as is) | Check |
|---|---|---|---|
| **S01** studio turntable | **R1** | Slow smooth quarter orbit to the right around the small jet hovering just above the floor, lights gliding across the polished metal. Keep the XF-85 Goblin exactly as in the image: egg-shaped polished-aluminium body, round nose intake, dark panel on top of the nose, bubble canopy, a short boxy dark hook frame on the nose just in front of the canopy, two upswept tail fins, a small fin on each wingtip, one star insignia, no wheels, no propeller. Dark graphite studio, soft white key light, warm gold and steel-blue rim lights, glossy reflective floor, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ hook, fins, no wheels |
| **S02** under the belly | **R1** | The camera slowly lowers and glides under the nose, looking up at the smooth underside: no wheels, no wheel wells, only a thin steel skid along the belly. Keep the XF-85 Goblin exactly as in the image: egg-shaped polished-aluminium body, round nose intake, bubble canopy, two upswept tail fins, a small fin on each wingtip, no wheels, no propeller. Dark graphite studio, warm gold and steel-blue rim lights, glossy floor, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ **weak** (big camera move). No wheels must appear. Fallback: a slow push-in on R1 while the narration says "no wheels at all". |
| **S03** hook reveal | **R5** | Slow pull-back from a close-up of the short boxy hook frame on the nose until the whole small jet is in view. Keep the XF-85 Goblin exactly as in the image: the hook frame, bubble canopy, dark nose panel, round nose intake, two upswept tail fins, wingtip fins, no wheels, no propeller. Dark graphite studio, warm gold and steel-blue rim lights, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ hook shape stays boxy |
| **S04** drop from the bomber · **Disc ON** | **R3** | The small jet releases from the trapeze and drops smoothly away below the bomber while the bomber flies on straight, clouds drifting past below. Keep the B-29 exactly as in the image: four propeller engines, rounded glass nose, one tall tail fin, the trapeze under the bomb bay. Keep the small jet's egg-shaped body, canopy, hook and fins exactly as in the image, no wheels. Black-and-white 1948 test film look, soft grain, gentle flicker, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ 4 engines on the B-29, trapeze shape |

### The problem of the era

| Shot | Upload | Video prompt | Check |
|---|---|---|---|
| **S07** B-36 wing | **R4** | Slow camera track along the enormous wing from the fuselage out to the wingtip, propellers spinning as blurred discs. Keep the B-36 exactly as in the image: exactly six propellers mounted behind the wing, no jet pods, never add or remove engines. Same look, colour and light as the image, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ six props, no jets |
| **S10** lone bomber | **R4** | Very slow pull-back and drift to the right until the bomber is small in a vast empty sky, thin clouds below. Keep the B-36 exactly as in the image: exactly six propellers behind the wing, no jet pods. Same look and colour as the image, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ engine count |

### Partial answer and walkaround

| Shot | Upload | Video prompt | Check |
|---|---|---|---|
| **S13** "no wheels" | **R2** | Slow orbit to the left around the small jet hovering above the floor. Keep the XF-85 Goblin exactly as in the image: egg-shaped polished-aluminium body, round nose intake, bubble canopy, short boxy hook frame, two upswept tail fins, a small fin on each wingtip, no wheels, no propeller. Dark graphite studio, warm gold and steel-blue rim lights, glossy floor, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. *(In CapCut, draw glowing outlines where wheels would be, then fade them out.)* | ⚠ fins |
| **S14** bomb bay fit | **R2 still** | **No Grok video.** Put the R2 still in CapCut and draw a glowing blue rectangle tightly around it, labelled "15 ft limit". | — |
| **S15** scale | **R2** | Slow pull-back revealing a grey faceless human mannequin about 1.8 m tall standing beside the jet for scale, the jet about the length of a family car. Keep the XF-85 Goblin exactly as in the image: egg-shaped body, canopy, hook frame, two upswept tail fins, wingtip fins, no wheels. Dark graphite studio, warm gold and steel-blue rim lights, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ **weak** (adds new objects). Fallback: place a person silhouette next to the R2 still in CapCut. |
| **S16** wings unfold | **Archival** | **No Grok video.** Use a real photo of the Goblin with its wings folded if you find one; otherwise hold on the S13 clip during this line. | — |
| **S17** tail fins | **R2** | Slow orbit around to the rear of the small jet, ending on a close view of the tail fins and the jet exhaust. Keep the XF-85 Goblin exactly as in the image: two upswept tail fins, a small fin on each wingtip, egg-shaped body, hook frame, no wheels, no propeller. Dark graphite studio, warm gold and steel-blue rim lights, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ fin count vs R2 |
| **S18** X-ray engine | **R2** | The aluminium skin slowly turns semi-transparent like glass, revealing a single jet engine inside glowing orange, running from the nose intake to the tail exhaust; slow orbit. Keep the XF-85 Goblin's outline exactly as in the image: egg-shaped body, canopy, hook frame, two upswept tail fins, wingtip fins, no wheels. Dark graphite studio, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ **weak**. Fallback: the R2 still with an orange glow drawn in CapCut |
| **S19** guns | **R5** | Slow slide along the nose, close up, showing the machine-gun ports beside the nose intake. Keep the XF-85 Goblin exactly as in the image: round nose intake, dark nose panel, hook frame, canopy. Dark graphite studio, warm gold and steel-blue rim lights, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ port positions vs photos |
| **S20** cockpit, looking up | **R3** | The camera slowly pushes in toward the small jet's bubble canopy until we are looking up through the glass at the hook and the bomber's belly just above; slight shaking as if in rough air. Keep both aircraft exactly as in the image. Black-and-white 1948 test film look, soft grain, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ **weak** (big move). Fallback: a slow push-in on R3 without entering the cockpit. |
| **S21** "no gear" X-ray | **S18 clip or R2 still** | **No Grok video.** Animate red wheel and strut icons bouncing off it in CapCut. | — |

### The test (black-and-white test-film look)

| Shot | Upload | Video prompt | Check |
|---|---|---|---|
| **S23** under the bomber · **Disc ON** *(only if you find no archival film)* | **R3** | Slow drift alongside, both aircraft flying steadily, clouds passing below. Keep the B-29 exactly as in the image: four propeller engines, rounded glass nose, one tall tail fin, the trapeze. Keep the small jet exactly as in the image, no wheels. Black-and-white 1948 test film look, soft grain, gentle flicker, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ |
| **S24** release and engine start · **Disc ON** | **R3** | The small jet unhooks and falls a short way below the bomber, its tail exhaust flares with heat shimmer as the engine lights, and it levels off; camera tracks alongside. Keep the small jet's egg-shaped body, canopy, hook frame, two upswept tail fins and wingtip fins exactly as in the image, no wheels. Keep the B-29 exactly as in the image. Black-and-white 1948 test film look, soft grain, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ |
| **S25** turbulence · **Disc ON** | **R3** | Close under the bomber's belly: visible churning air and heat-haze ripples, the steel trapeze bar swinging and shaking, clouds racing below, camera shaking. Keep the B-29 and trapeze exactly as in the image. Black-and-white 1948 test film look, soft grain, 16:9. No morphing, no extra parts. | ⚠ trapeze shape |
| **S26** the approach · **Disc ON** | **CHAIN**: last frame of S24 | The small jet rises and bounces unsteadily toward the swinging trapeze bar, rocking side to side in rough air, camera shaking. Keep the small jet's body, canopy, hook frame and fins exactly as in the image, no wheels. Black-and-white 1948 test film look, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ |
| **S27** canopy hit · **Disc ON** | **CHAIN**: last frame of S26 | The steel trapeze bar strikes the small jet's bubble canopy; the glass cracks and shatters outward in slow motion, fragments whipping away in the wind. Keep the jet's shape exactly as in the image. Black-and-white 1948 test film look, 16:9. No morphing, no extra parts. | ⚠ event details (see fact-check) |
| **S28** belly landing · **Disc ON** | **Archival first**, else **R2** | *(If no archival photo of the skid landing:)* The scene becomes a vast cracked dry lakebed in the California desert; the small jet touches down on its belly skid and slides, throwing up a long plume of dust, slowing to a stop; camera tracks low alongside. Keep the XF-85 Goblin exactly as in the image: egg-shaped body, canopy, hook frame, two upswept tail fins, wingtip fins, no wheels. Black-and-white 1948 test film look, soft grain, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ **weak** (scene change). No wheels must appear. |

### "Imagine that…" (AI direct: no upload)

| Shot | Upload | Video prompt | Check |
|---|---|---|---|
| **S31** Arctic night | **None** (text to video) | Night over a frozen Arctic sea under a violent storm, a huge bomber seen only as a tiny dark distant silhouette against lightning, faint tracer fire in the clouds, snow streaking past the camera, ominous, cinematic, photoreal, 16:9. | Add an on-screen "Illustration" label in the edit |

### Payoff and ending

| Shot | Upload | Video prompt | Check |
|---|---|---|---|
| **S35** back to the studio | **R1** | Slow smooth quarter orbit to the left around the small jet hovering just above the floor. Keep the XF-85 Goblin exactly as in the image: egg-shaped polished-aluminium body, round nose intake, dark nose panel, bubble canopy, short boxy hook frame, two upswept tail fins, a small fin on each wingtip, one star insignia, no wheels, no propeller. Dark graphite studio, soft white key light, warm gold and steel-blue rim lights, glossy reflective floor, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ |
| **S36** X-ray bomber | **R4 + R1 stills** | **No Grok video.** In CapCut, place the R1 Goblin (background removed) small inside the R4 bomber with a blue glow and do a slow zoom out. | — |
| **S37** push-in on hook | **R5** | Slow push-in onto the short boxy hook frame on the nose. Keep the hook, canopy and dark nose panel exactly as in the image. Dark graphite studio, warm gold and steel-blue rim lights, photoreal, 16:9. No morphing, no extra parts, smooth realistic motion. | ⚠ hook shape |
| **S38** hook in the dark | **R5** | The studio lights slowly fade to black until only the hook frame and the top of the nose remain, lit by one warm gold rim light. Keep the hook exactly as in the image. Photoreal, 16:9. No morphing, no extra parts. | ⚠ |
| **S40** modern drones *(only if you don't name a real programme)* | **None** (text to video) | A large modern grey military transport plane flying at sunset above the clouds, a small sleek unmarked drone rising slowly toward its belly, no insignia, photoreal, cinematic, 16:9. | — |
| **S41** next-video tease | Depends on the next video's aircraft | Use that aircraft's approved reference photo and a slow push-in prompt with its own lock line. | ⚠ |

Archival and graphics shots (S05, S06, S08, S09, S11, S12, S22, S29, S30, S32–S34, S39) are unchanged. See `airspeed-model.md`.

---

## Quick reference: what to upload for each shot

| Upload | Shots |
|---|---|
| **R1** (head-on, cleaned) | S01, S02, S35 |
| **R2** (side, cleaned) | S13, S15, S17, S18, (S28 fallback) |
| **R3** (on the trapeze, B&W) | S04, S20, S23, S24, S25 |
| **R4** (B-36) | S07, S10 |
| **R5** (nose and hook crop) | S03, S19, S37, S38 |
| **CHAIN** (last frame of the previous clip) | S26 (after S24), S27 (after S26) |
| **None** (text to video) | S31, S40 |
| **No Grok video** (CapCut or archival) | S14, S16, S21, S36 |

**Fallback if one shot keeps failing:** make one still image of that exact frame first (upload the reference plus the prompt without the camera move), fix it, then animate it. Use this only for that shot.
