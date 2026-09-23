# Airspeed Memory — Aviation Visual Prompting Style

Trigger phrase: **"airspeed memory"**. When the user says it, load this file and write every image/video prompt in this style.

Reference channel: Airspeed (@AirspeedChannel) — 3D-animated aviation history, "Why…" titles, ~11 min videos, calm documentary narration.

---

## Core rule: image-to-video, never text-only

Always start from a REAL reference picture of the aircraft, then animate it:

1. Get a still of the exact aircraft — a render of a bought 3D model (Sketchfab / CGTrader / TurboSquid / Hum3D) or a public-domain photo (National Archives, NASA, USAF, Wikimedia Commons, SDASM Flickr).
2. Upload that still to an image-to-video tool (Kling, Google Veo, Runway, Hailuo).
3. Add a short motion prompt in the formula below.

A text-only prompt makes the AI invent the plane (wrong engines, windows, markings). A reference image keeps it accurate.

---

## Prompt formula

```
[camera move] + [subject: aircraft + color/material] + [environment] + [lighting] + [mood/pacing]
```

Master example:

> slow cinematic orbit around a white aircraft in a minimalist studio hangar, soft lighting

---

## Style building blocks

**Camera moves** — slow cinematic orbit · slow push-in · slow pull-back · low-angle dolly past the nose · tracking shot alongside in flight · top-down rotating overhead · slow tilt-up from landing gear · static hero shot with subtle parallax

**Subject** — white/clay matte aircraft · brushed aluminium aircraft · silver fabric-skinned fuselage · x-ray / ghosted transparent fuselage showing [internal part]

**Environment** — minimalist white studio hangar · clean grey hangar with reflective floor · dark studio, deep red-to-black gradient backdrop · simplified 3D ocean at dusk · soft rolling hills · empty sky with light clouds

**Lighting** — soft lighting · high-key studio lighting with soft floor shadows · golden-hour side light · rim light on dark background

**Mood / finish** — calm documentary pacing · smooth, no shake · photoreal 3D render look · 5-second shot

---

## Ready-to-use prompts

1. slow cinematic orbit around a white aircraft in a minimalist studio hangar, soft lighting
2. slow push-in on the nose and propeller of a brushed aluminium aircraft, clean grey hangar, reflective floor, soft lighting
3. white aircraft on a dark studio floor, deep red-to-black gradient backdrop, rim lighting, slow low-angle dolly past the wing
4. tracking shot alongside a silver aircraft flying over a calm ocean at dusk, golden-hour side light, smooth motion
5. top-down slow rotating overhead view of a white aircraft in a minimalist hangar, soft even lighting
6. x-ray ghosted fuselage revealing the [fuel tank / cockpit / engine], slow orbit, studio hangar, soft lighting
7. static hero shot of a white aircraft facing camera in a white hangar, subtle parallax, soft lighting (thumbnail / intro)
8. two aircraft side by side on a dark studio floor, national flags in background, slow pull-back, soft lighting (comparison videos)

## Thumbnail style

White/grey aircraft, dark red-black studio background, minimal or no text, optional flags for "X vs Y" topics.

## Rules

- 3–5 seconds per shot; regenerate and discard any shot where the aircraft shape is wrong.
- Use AI-only (no reference) prompts only for B-roll: skies, oceans, factories, crowds.
- Mix in public-domain archival photos/film between renders.
- Accuracy first — aviation viewers catch every error.
