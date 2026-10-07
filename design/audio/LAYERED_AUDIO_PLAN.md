# Layered audio plan — courier, shadow, and journey

**Status:** sound design proposal with a new [layered listening prototype](layered-audio-review.html), 7 October 2026. It auditions all 18 courier names and 19 shadow looks through shared sound families and individual motifs. These are provisional procedural sounds, not final recordings or integrated gameplay audio. The playable game has not been changed.

The arrangement is an **adaptive music and soundscape mix**. A level supplies a chapter music palette and its chosen shadow look; the player supplies an equipped courier. Gameplay then controls how strongly each layer is heard. These identities are cosmetic audio cues, with no change to light, patrol, Echo, movement, or collision rules.

## One mix, with clear jobs

| Layer | Source | When heard | Priority |
|---|---|---|---|
| Journey bed | Chapter / level district | Quiet continuous phrase and village air | Lowest; fades under outcome cues |
| Courier signature | Equipped courier ID | Subtle two- or three-note color on starting a route, first move after a pause, and occasional movement accents | Below game feedback; never a constant loop |
| Outfit accent | Equipped cosmetic look | A very short timbre garnish on the courier signature, if enabled | Optional; no separate melody |
| Shadow identity | Level's `shadowSkinId` | Its own sparse motif as an active shadow approaches | Audible but below collision warnings |
| Shadow proximity | Nearest active patrol or Echo distance | Existing haunting breath grows as danger nears | Crossfades with identity |
| Lantern pressure | `state.light / cap()` | Pulses at 45%, 25%, and 10% | Clear enough to notice, quiet enough to avoid alarm fatigue |
| Game events | Step, delivery, crossing, repair, denied, collision warning | Existing short feedback at the moment of action | Above music and textures |
| Outcome | Bank/complete or failure | Short resolution, then transition | Highest for its brief duration |

The courier and shadow motifs should be distinguishable **by contour and instrument**, even if the phone speaker loses bass. Courier sounds favor warm pitched attacks (wood, bell, glass, pluck). Shadows favor breath, hollow resonance, scrape, flutter, or unstable pitch. Keep both in the same chapter key or use a controlled dissonance that resolves when the shadow retreats.

## Courier identity map

Compose **six reusable timbre families**, then give each courier a short, unique rhythm or interval. This makes 18 identities feasible without 18 full music tracks. The IDs match `design/character-variants/manifest.json`.

| Family | Courier IDs and names | Proposed signature |
|---|---|---|
| Hearth | 01 Ember Scout, 12 Dawn Baker, 15 Lantern Keeper | Soft brass/wood glow; steady rising intervals. Keeper is slower and lower, Baker has a lighter three-note answer. |
| Green path | 02 Moss Ranger, 09 Willow Guide, 13 Foxglove Courier | Dry leaf/wood plucks with open fifths; Willow has a longer tail, Foxglove a quick skip. |
| Water route | 03 Canal Pilot, 10 Harbor Skipper, 17 Mooncap Wanderer | Rounded glass or water-drop notes; Pilot is clipped, Harbor sways, Mooncap has a delayed echo. |
| Bell and clock | 04 Bell Messenger, 08 Clockwork Porter, 11 Ash Cartographer | Small bell, clock tick, or muted metal; distinct two-tap rhythms, never a full beat under every step. |
| Fleet | 06 Patchwork Runner, 07 Rooftop Finch, 14 Bluebird Runner, 16 Market Sprinter | Short airy/wood attacks; each uses a different spacing or pitch leap. Avoid fast repeated ticks while moving. |
| Cold and dusk | 05 Winter Warden, 18 Sunset Relayer | Soft frosted glass versus warm low chime; similar restraint, different color. |

**First implementation target:** audition 01 Ember Scout, 03 Canal Pilot, 07 Rooftop Finch, and 15 Lantern Keeper, the character chat's strongest visual candidates. If those four read clearly alongside the chapter bed, expand the remaining families. Selection should change the signature at the next route start; changing outfits during a run should wait until the next level to avoid an abrupt music switch.

The five holiday outfits per courier are visual concepts. If outfit audio is added, use one optional accent per theme (Dussehra ember crackle, Halloween hollow air, Diwali tiny light sparkle, Christmas soft snow chime, New Year star glint) layered onto the courier identity. Limit it to one short accent at a route start or delivery, with the same loudness regardless of shop price. No paid look should grant a stronger warning or gameplay advantage.

## Shadow identity map

The 19 looks in `design/shadow-variants/manifest.json` can share **five base textures** with varied attack shapes. A level chooses one look for its patrols and Echo; Echo is a quieter, delayed variation of that look. Multiple patrols of the same look should never create multiple full-volume loops.

| Family | Shadow IDs | Identity cue |
|---|---|---|
| Wisp and seasonal | 01–06 | Wavering airy tone; seasonal looks change a restrained texture, not the danger meaning. |
| District haze | 07 Canal Mist, 08 Old City Cinder | Hollow water breath or dry cinder grit. |
| Hollow and veil | 09 Bell Hollow, 10 Ribbon Wraith, 11 Moth Veil, 19 Hourglass Shade | Resonant bell cavity, thin ribbon glide, soft wing flutter, or falling sand hiss. |
| Broken and crawling | 13 Shard Mask, 14 Ink Puddle, 15 Thorn Crown, 17 Veil Hand | Brittle shard tap, low smear, thorn scrape, or airy finger-like tremor; no sound should imply a new attack. |
| Orb and curve | 12 Crescent Lurker, 16 Eclipse Orb, 18 Serpent Coil | Bent overtone, circular pulse, or coiled pitch slide. |

The visual handoff recommends 01 as a default and notes 09, 11, 12, 13, 16, and 18 as readable candidates. Start audio comparisons with those. If a skin is unavailable or unapproved, use 01's neutral shadow identity. A seasonal override, if used, resolves when the level loads and stays fixed for that run.

## State and transition rules

1. On level load, resolve `chapter`, equipped `courierId`, optional `outfitId`, and `shadowSkinId`. Crossfade the journey palette over about two seconds. Play one quiet courier signature after audio is unlocked and the route begins.
2. Before the first delivery, patrol shadows are asleep in the current game. Their identity and proximity layers remain silent. When they wake, fade them in over about a second; do not use a sudden scare cue.
3. Each move updates the **minimum distance to an active shadow**. One shared proximity gain rises within four tiles and releases as distance increases. The chosen shadow texture rides that gain. If Echo and patrol are both close, use the nearer distance for urgency, with a faint secondary Echo tail at most.
4. Lantern pressure uses remaining percentage, not an absolute count. At 45% add a sparse pulse; at 25% shorten its spacing; at 10% add a slightly stronger pulse. A house refill releases the prior intensity smoothly. Low light must not mask the legal-move or collision feedback.
5. On a safe delivery, briefly duck music and shadow texture (about 2–3 dB) for the existing house cue, then restore them. On completion or banking, duck the layers further, play the outcome cue, then crossfade to the next chapter/level. On failure, play the failure cue and let the ambience settle before restart.
6. Mute cuts the whole mix including cues. Master volume applies to all buses. Gentle mix reduces shadow and low-light peaks and slows the critical pulse. Resume only after a user gesture when browser audio is suspended; pause continuous layers when the page is hidden.

## Example mixes to review

| Scenario | What plays together | What should dominate |
|---|---|---|
| Level 1, Ember Scout, Night Wisp asleep, full lantern | First Deliveries bed + occasional Ember signature + normal step/delivery sounds | Clear movement and house feedback |
| Canal Pilot, Canal Mist, shadow three tiles away | Waterline bed + sparse Pilot drops + quiet mist texture + proximity breath | Shadow presence without a warning alarm |
| Rooftop Finch, Eclipse Orb adjacent, 22% light | Chapter bed ducked slightly + Finch identity only at phrase gaps + orb tone and proximity breath + measured lantern pulse | Dangerous state, while legal tile cues remain distinct |
| Lantern Keeper reaches depot with 7% light | Low-light pulse and shadow fade out; completion cue takes focus | Relief and resolution |
| Any courier fails in Blackout | Shadow and pulse recede; falling failure cue; brief silence before retry | Unambiguous failure without a prolonged sting |

## Review and production gates

Use the layered listening page to shortlist identities at phone volume and compare the scenarios above. Confirm each chosen identity can be recognized without drowning the existing gameplay cues. The page simulates one nearest-shadow layer; a real two-shadow plus Echo level still needs an in-game mix test. Then refine the selected sounds, integrate them behind the existing sound toggle, and test on a physical phone in the three visual modes, with mute, gentle mode, background/resume, headphones, and small speakers. Until those checks pass, every identity in this document is a proposal rather than integrated game audio.
