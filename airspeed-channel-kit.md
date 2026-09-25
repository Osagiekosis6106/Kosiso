# Channel kit: instructions for building a channel that beats Airspeed

These are **instructions, not decisions**. The channel name, description, colours, logo and banner **haven't been chosen yet**. Decide them with the user when they ask, following the steps below. Nothing here is fixed. The research behind these rules is in `airspeed-model.md`, and the Grok workflow is in `airspeed-grok-prompts.md`.

---

## 1. Name: how to choose it

Offer the user **5–8 candidates** and let them pick. A good name:
- **says the channel's difference**: showing the physics or engineering reason, not just telling the story;
- is **short** (1–3 words) and easy to say, spell and search;
- has an **aviation cue** (hangar, airframe, rivet, wing, flight), but **nothing containing "Air", "Speed" or "Airspeed"**, which reads as a copy;
- **is free on YouTube**. Check every candidate with NexLev `youtube_search` (type: channel) and say what you found. Then ask the user to check the @handle in YouTube Studio.

**Names already taken in this niche (Sep 2026 search; re-check):** *Airframe* (a new 3D clone with a very similar promise, "one strange aircraft decision at a time"; watch it), *This Is Why It Flew*, *Inside the Airframe*, *The Aircraft Files*, *BUILT WEIRD*, *Oddgist*.

---

## 2. Channel description (About): how to write it

Once the user has picked a name, write it in this shape:

> [One-line promise: strange part of a famous aircraft + the reason behind it.]
>
> [Two example questions in the channel's title style.] [What every video does: one aircraft, one strange design choice, rebuilt in 3D, the answer shown visually.]
>
> [Trust line: researched from primary sources, fact-checked, sources listed in every description.]
>
> [Upload promise, e.g. "New video every week."]

Rules:
- **Never write "made entirely by humans" or "no AI".** The user uses Grok. If asked, the honest line is *"3D and AI-assisted animation, with a human-written, fact-checked script."*
- **Keywords** (YouTube Studio → Settings → Channel → Basic info): `aviation history, aircraft engineering, aircraft design, 3D animation, aviation explained, military aviation, experimental aircraft, Cold War aircraft, WWII aircraft, how planes work`.
- **Country:** set it truthfully.

---

## 3. Colours and fonts: how to choose them

When the user asks, propose **2–3 palettes**, each with:
- a dark background colour and a gradient accent;
- a rim or X-ray line colour;
- an off-white text colour;
- hex codes for all of them.

Rules:
- **Not Airspeed's navy-to-crimson.** The channel must be recognisable as different.
- Colours must **work on a dark studio background** and stay readable on a phone.
- Once chosen, the palette goes into the Grok `[STUDIO LOOK]` text, the thumbnails, the logo and the banner, **so everything looks like one brand**. Then record it in `CLAUDE.md`.
- Fonts: suggest one condensed heading font plus one clean label font, both free on Google Fonts / Canva (e.g. Barlow Condensed + Inter).

---

## 4. Logo (profile picture): how to make it

- **Concept rule:** one simple aircraft silhouette or outline that hints at the channel's difference (for example X-ray lines or a centre-of-gravity dot). It must read as "aircraft" at tiny circle size.
- **Make the icon in Grok. Don't put text in it**, because AI spells badly. Prompt template:
  > Minimal flat vector logo icon, a simple generic [aircraft type] seen perfectly head-on, drawn as clean thin glowing [ACCENT COLOUR] outline lines like an X-ray blueprint, [optional small detail in SECOND COLOUR], on a solid [BACKGROUND COLOUR] background, centred, symmetrical, lots of empty space around it, no text, no letters, 1:1
- **Finish in Canva:**
  1. Make an 800 × 800 px design and keep the icon inside a circle-safe area (YouTube crops to a circle).
  2. Export as PNG.
  3. Make a 150 × 150 px version for the watermark (YouTube Studio → Customisation → Branding).

---

## 5. Banner: how to make it

- **Size:** 2560 × 1440 px. Keep everything important inside the centre **1546 × 423 px**, which is all that shows on phones.
- **Grok background prompt template:**
  > Wide cinematic dark studio hangar, [BACKGROUND]-to-[ACCENT] gradient back wall, polished reflective floor, a single silver [era] aircraft seen from the front three-quarter, soft white key light, [ACCENT] and [SECOND COLOUR] rim lights, lots of empty dark space on both sides, photoreal 3D render, no text, 16:9
- **In Canva, add:**
  - the channel name in the heading font across the centre;
  - one short tagline under it (write 3 options for the user);
  - the upload promise, small at the right.

---

## 6. Voiceover

### The voice

- **One voice, forever.** Airspeed's calm male "museum guide" voice is part of its brand. Pick yours once and never change it.
- **The tone to aim for:** warm, confident and slightly lower-pitched, like a friendly pilot explaining something in a hangar. A little more energy than Airspeed's flat delivery.
- **Pace:** 145–155 words per minute. A 1,750-word script is about 11:30–12:00.
- **Accent:** a clear, neutral English accent. Just over half of Airspeed's viewers are in the US, so choose a voice those viewers find easy to follow.

### Your options (pick one)

1. **Your own voice (best for trust and for YouTube's rules on original content).** Use a USB microphone (Fifine K669 or Samson Q2U are cheap and good) in a room with soft things around you: clothes, a bed, curtains. Record in Audacity or CapCut (both free). Read each paragraph twice and keep the better take.
2. **A hired narrator:** Fiverr or Voices.com, from about $30–100 per video. Send the script with the delivery notes below.
3. **An AI voice (ElevenLabs):** choose one "narration / documentary" voice and save it. Test 3 voices by reading the cold open of the XF-85 script and keep the one you'd listen to for 12 minutes.

   Suggested starting settings (ElevenLabs sliders): Stability ~50%, Similarity ~75%, Style ~20%. Adjust by ear. Generate one paragraph at a time, never the whole script at once.

### Delivery marks to put in every script

| Mark | Meaning |
|---|---|
| `/` | short breath |
| `//` | one-second pause (use before every payoff line) |
| **bold word** | stress this word |
| `[slower]` … `[/slower]` | slow down, used in the tension beats |
| `[quiet]` | drop to near-whisper (the S26–S27 canopy moment) |

For ElevenLabs, pauses come from punctuation: use an em dash "—" or "…" and start a new paragraph for longer pauses.

### Say these right (aviation viewers will notice)

| Word | Say |
|---|---|
| Orteig (Prize) | OR-tig |
| Lindbergh | LIND-berg |
| Dornier | DOR-nee-ay |
| Luftwaffe | LOOFT-vah-fuh |
| Pfeil (Do 335) | FILE |
| Messerschmitt | MESS-er-shmit |
| Tupolev | too-POL-ev |
| Sikorsky | sih-KOR-skee |
| Muroc | MYOOR-ock |
| Le Bourget | luh boor-ZHAY |

Before recording a new aircraft, look up any foreign name on YouTube or Forvo.com.

---

## 7. Music and sound

- **Music:** low cinematic orchestral with a slow build (search "documentary tension" or "cinematic ambient"). Keep it about 20 dB below the voice, and drop it out completely for the two or three tension beats.
- **An engine bed for every aircraft:** the real sound type (radial piston, V12, early jet whine). Epidemic Sound, Artlist, or free in the YouTube Audio Library and Pixabay sound effects.
- **Whooshes** on camera moves and a **soft riser** into each payoff line.
- **Level check:** voice peaks at around −6 dB, and nothing ever louder than the voice.

---

## 8. Every upload (settings checklist)

- [ ] **Title:** one of the patterns in `airspeed-model.md` section 6, under 55 characters, with the aircraft named. Load **3 title and thumbnail pairs into Test & Compare**.
- [ ] **Thumbnail:** one aircraft, the strange part visible without text, the channel's chosen studio colours, readable at phone size. Make it from the M1/M2 master in Grok, then add a subtle rim glow in Canva. No arrows, no meme text.
- [ ] **Description:**
  1. two-sentence summary;
  2. chapters (the first must be `0:00`);
  3. *"Researched and written by [name]. 3D and AI-assisted animation."*;
  4. sources and licences for each archival clip;
  5. 3 hashtags, e.g. `#AviationHistory #XF85 #AircraftDesign`.
- [ ] **Category:** Science & Technology (the same as Airspeed).
- [ ] **Altered or synthetic content: YES** whenever a realistic AI shot shows a real event or person (the shot sheet marks these **Disc ON**).
- [ ] **Made for kids: No.** **Language:** English. **Captions:** upload the script as a transcript so the captions are accurate.
- [ ] **End screen:** the chained video (the one your ending teases) plus Subscribe.
- [ ] **Playlist:** put it in **"Strange Airframes"** (every video) and one era playlist (*WWII*, *Cold War*, *Golden Age*, *Jets*).
- [ ] **Pinned comment:** a *would-you* question about the pilot's choice.
- [ ] **Three Shorts:** cut from the best moments (the strangest part reveal, the X-ray, the tension beat) in 9:16, 30–45 s, each ending *"Full story on the channel."* Use the same title pattern.

**Schedule:** launch **3 linked videos on the same day** (XF-85 → B-36 → Do 335), then **one long video every week on the same weekday and time**, with its Shorts spread over the following days.

---

## 9. The weekly routine, start to finish

| Day | Job | Where |
|---|---|---|
| 1 | **Pick the topic:** NexLev outlier search. Check it isn't done well in the last 90 days, and read the top 3 existing videos' comments for corrections. | `airspeed-model.md` sections 10 and 12 |
| 1–2 | **Research and write** the script with the Airspeed+ table, the research checklist and the delivery marks. | `airspeed-model.md` section 9, this file section 6 |
| 2 | **Shot sheet:** label every visual (REUSE / NEW / CHAIN / AI direct / archival / graphic, VERIFY, Disclosure). | `airspeed-grok-prompts.md` |
| 3 | **Masters:** download the real photos (R1…), generate and approve M1…M6. | Grok |
| 3–4 | **Generate all shots**, 3–5 s each. Throw away anything where the plane changes shape. | Grok |
| 4 | **Archival and graphics:** download footage, make the spec cards and maps. | NARA, USAF Museum, Wikimedia, Canva / CapCut |
| 5 | **Voiceover**, then **edit:** cut on narration beats, ~4 s average shot, music and engine bed. | CapCut / DaVinci Resolve |
| 6 | **Package:** 3 titles, 3 thumbnails, description, chapters, Shorts. | Grok, Canva, YouTube Studio |
| 7 | **Publish.** Pin the comment, reply to the first hour of comments, and note any corrections for the next script. | YouTube Studio |

---

## 10. What to say to get all this back

In any new session in this repo, say **"airspeed"** plus what you want. For example:
- *"airspeed: help me choose the channel name"*
- *"airspeed: write a script about [aircraft]"*
- *"airspeed: make the Grok prompts for this script"*

That loads the research, the formulas, these instructions and the Grok workflow. Names, colours, topics and scripts are only decided when you ask.
