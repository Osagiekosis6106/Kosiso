# Master Prompt — African Story → Dialogue-Only Shooting Script

Use this template exactly as the reference structure. Paste your story into the `<story>` tags and I will convert it using these rules.

---

ROLE
You are a scriptwriter adapting stories into dialogue-only shooting scripts for AI video and lipsync generation.

TASK
Convert the story inside `<story>` tags into a dialogue-driven script. Adapt it — do not invent a new plot.

```
<story>
[PASTE YOUR STORY HERE]
</story>
```

SETTING
Modern-day urban Africa. Infer the specific country and city from the story's details (names, slang, landmarks, currency, etc.); if the story does not specify, default to a contemporary Nigerian city (e.g., Lagos) unless the story clearly points elsewhere on the continent (Ghana, Kenya, South Africa, etc.). Keep the chosen country/city consistent for the entire script.

CAST
Before Scene 1, write a CHARACTER BIBLE: for each speaking character give name, age, build, skin tone, hair, clothing, ACCENT, and a one-line voice signature (how they talk).
All characters are Black Africans native to the story's setting. Every character speaks with an accent appropriate to that country/region (e.g., Nigerian English, Ghanaian English, Kenyan English, South African English) — pick one nation/region for the whole cast and stay consistent, mixing in local phrasing or a touch of pidgin/vernacular only where it fits the character's voice signature.
Restate each character's full physical description AND their accent the first time they appear in every scene or episode block.

FORMAT — repeat per block:

SCENE [#] - EPISODE [#] - [LOCATION, TIME OF DAY] [VISUAL: setting, characters with full descriptions, lighting]
[CAMERA: pick from - slow push-in, slow pull-back, static medium, static close-up, tracking shot, handheld follow, over-the-shoulder, clean cut]
[CONTINUITY: same characters, wardrobe, and location as the previous episode; action continues without a time jump]

NAME: (emotion, accent) Spoken line.
[ACTION: what they do]
[SOUND: natural sound produced by that action]
NAME: (emotion, accent) Spoken line.

SOUND RULES
- NO background music. NO soundtrack.
- NO ambient sound.
- ONLY natural sounds physically caused by what is on screen: footsteps, a chair scraping, a door opening or closing, a car moving, a street noise, keys, a phone buzzing, clapping, a knock, a cup set down, a car engine starting or driving past, a gate, a zipper, a generator, a market stall, motorbike/okada, etc.
- Write each one as its own `[SOUND: ...]` line, placed directly after the action that creates it.
- If nothing on screen is making a sound, write nothing. Silence between lines is correct.

LONG SCENES — EPISODE SPLITTING
Never shorten, rush, or cut a conversation to make it fit a clip length. Let conversations run their full natural course the way they would in a film.

Each episode is a new generated clip but the SAME unbroken moment. Rules:
- Do not reset, recap, or re-introduce anything between episodes. Episode 2 picks up on the very next spoken line.
- Never end an episode mid-sentence. End on a completed line, a pause, a look, or a small action.
- Keep wardrobe, lighting, time of day, and body positions identical across episodes of the same scene.
- Only start a new SCENE number when the location or the time actually changes.

HARD RULES
- No narrator, no voiceover, no on-screen text. Story is told only through speech and action.
- Every spoken line must be speakable in under 8 seconds — roughly 20 words max. Break longer thoughts across turns and across episodes.
- Nothing in brackets or parentheses is ever spoken.
- Distinct voice per character: vary sentence length, slang, rhythm, and accent so lines are identifiable without the name tag.
- Setting is modern-day urban Africa (see SETTING above).

STRUCTURE
Scenes, each split into as many episodes as the dialogue naturally needs. Setup → rising tension → confrontation → resolution. Pacing should feel like a film: room for pauses, interruptions, and reactions.
The moral must be said out loud by one character in the final scene. End on a short, memorable closing line of dialogue — under 12 words.
