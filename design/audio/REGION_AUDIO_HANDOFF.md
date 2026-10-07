# Region audio pass — review and integration handoff

**Review artifact:** [region-mix-review.html](region-mix-review.html). Press **Start journey mix**, choose a region and courier, then audition solo phrases, scenarios, event buttons and powers. This is procedural concept audio. It is not in the playable campaign.

## Current game facts

- `game/index.html` contains 2,000 levels and 20 named regions, each covering 100 levels. The region index is `Math.floor((level.n - 1) / 100)`, clamped to 0–19.
- `game/region-shadows.js` assigns one shadow look per region. The review page uses that same sequence, and the names match `design/shadow-variants/region-shadow-map.json`. The courier selection is saved by `game/shell.js` in `llc-appearance-v1`.
- `game/ambient.js` already plays background phrases using 20 root pitches but only five recurring phrase shapes. `game/shell.js` feeds it region, light, capacity, music on/off and music volume. This explains why the region change can be hard to hear.
- `campaign/feedback.js` already has event sounds for step, shadow near, house, repair, denied, complete, failure and crossing. `game/index.html` calls those events. The nine powers and several named hazards do not have distinct live audio calls yet.

## Review direction

The new prototype gives each region its own melodic contour, rhythm, root and instrument color. Notes have short tails and gaps. There is **no continuous drone or hum**. Regional motifs stay soft enough for taps, safe moves and deliveries to read above them. The courier plays a brief signature on route start and every other phrase. The assigned shadow enters with a sparse, slightly unstable phrase when the nearest active shadow is within four tiles. Low light adds measured pulses at 45%, 25% and 10%; it never becomes a siren. A quiet or mute setting is available.

The 20 regions are all represented, including Ember Road, River of Glass, Storm March, The Long Night, Black Horizon and The Last Light. The main comparison set for listening should be **Ember Road → River of Glass → The Shadowworks → Storm March → The Long Night → The Last Light**. Those span warmth, water, machinery, wind, emptiness and resolution. Listen again with Ember Scout, Canal Pilot, Rooftop Finch and Lantern Keeper. Test the region's assigned shadow at distance 1, then move it back to 6 to check release.

The courier phrases use six restrained instrument families. They are recognizable by short rhythm and pitch contours rather than a full personal music track. Holiday outfits do not alter audio in this pass. The shadow phrase is tied to the region's assigned art; a recurring look can retain a familiar motif while the region music changes around it. Patrol and Echo should share the region identity, with Echo at lower gain and a delayed tail, never as another full-volume loop.

## Proposed runtime buses

| Bus | Normal target relative to event bus | Routing |
|---|---:|---|
| Region music | 0.35–0.5 | `musicOn`, `musicVolume`; crossfade at a 100-level region boundary or level selection |
| Courier signature | 0.25–0.4 | chosen courier; start, after idle, then at sparse phrase intervals |
| Shadow identity and proximity | 0–0.4 | nearest *active* shadow distance; gentle mode halves peak |
| Low-light pressure | 0–0.3 | `state.light / cap()` with 45/25/10% stages |
| Events and powers | 1.0 | `soundOn`, `effectVolume`; clear over the background |
| Completion/failure | 1.0 | momentarily duck region and shadow buses, then return or stop |

These are starting ratios for phone listening, not mastered values. Limit the final summed output with a gentle compressor or conservative gain, and verify at low device volume and through small speakers. Avoid boosting bass to compensate for tiny speakers; the important motif notes should remain in the midrange.

## Exact trigger plan

| Game event/state | Review cue | Integration note |
|---|---|---|
| User taps a legal grid cell | `tap`, then `move` | `move(p)` currently emits `step`; replace or adapt that event once to avoid double playback. Tap and motion should feel like one action. |
| User taps a blocked adjacent cell | `blocked` | Emit only for an intentional tap, with a cooldown; disabled UI tiles may not currently receive clicks. No cue for casual pointer travel. |
| New house lit | `delivery` | Adapt current `house` event; music ducks briefly. Do not play both old and new cues. |
| Fading crossing / thin ice closes | `crossing` / `ice` | Use the actual closing transition. Existing `crossing` handles a combined case; distinguish feature at the source. |
| Dark street entered / gate opens / quake occurs | `dark` / `gate` / `quake` | Emit on the confirmed state change, not preview or unavailable action. |
| Repair purchase succeeds | `repair` | Keep purchase confirmation and current `repair` event; replace its timbre after review. Denied purchases keep a separate, softer denied cue. |
| Power charge consumed and effect applied | nine `data-power` cues | Use `consumePowerCharge(power)` success plus an effect-complete hook. Anchor Trap and Decoy Light should play on **placement**, not merely arming the tile selector. Rewind plays after state restoration. |
| Shadow becomes active / approaches / recedes | region shadow phrase + proximity | Before activation, silent. Use nearest actual patrol/Echo tile after movement; do not preview future positions. Rise within four tiles, release over roughly one second. Suppress repeated old `shadowNear` stings if they double the texture. |
| Light decreases or refills | low-light pulse | Use percentage of current capacity so beacon repair and other capacity changes remain consistent; smooth stage changes. |
| Depot banking / full completion / failure | result cues | Duck all continuous layers for the short outcome cue. Stop scheduling after a finished run until a new route starts. |

Keep `musicOn/musicVolume` and `soundOn/effectVolume` as separate controls. Courier and shadow signatures are musical layers under the **music** control; tap, hazard, power and result cues use **effects**. Mute applies to both. AudioContext must unlock on a user gesture and pause on hidden/background state. Any future comfort option should lower tension/low-light peaks without hiding essential legal-move information.

## Status and verification

`node design/audio/validate-region-mix.cjs` parses and runs the review script with a mock Web Audio context, checks the 20 region and 18 courier names against manifests, checks all nine power buttons, and confirms starting the mix, delivery and a power schedule sound. It does **not** establish sound quality or real-device playback. Listening approval, phone-speaker balance, and normal-play testing remain outstanding. The playable game audio files are unchanged.
