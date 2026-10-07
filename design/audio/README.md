# Last Light Courier audio review

## Current region pass

Open [region-mix-review.html](region-mix-review.html) for the latest directly listenable concept. It follows the 2,000-level game's 20 region names and assigned shadow sequence, and includes selectable couriers, low-light/shadow scenarios, grid and hazard cues, repair, all nine powers, and result cues. The music uses short phrases with gaps and no sustained hum. The [integration handoff](REGION_AUDIO_HANDOFF.md) lists the source hooks and review limits. No playable game audio was changed in this pass.

## New layered listening demo

Open [layered-audio-review.html](layered-audio-review.html) to audition the chapter bed, courier signature, shadow identity, proximity tension, low-light pulse, and outcome cues together. It includes all 18 courier names and all 19 shadow names from the design manifests. Use **Hear courier alone** and **Hear shadow alone** to identify their motifs, then **Start full mix** and choose a scenario. Courier motifs are short phrases rather than a constant character loop; the shadow motif becomes part of the mix only when an active shadow approaches.

These are procedural concept sounds. The 18 couriers share six instrument families with different pitch and rhythm; the 19 shadows share five texture families with different intervals and motion. The selected holiday outfits do not have their own accent yet. There are no exported production audio files and no integration into the playable game.

Open [audio-review.html](audio-review.html) in a modern browser and press **Start audio**. Browser audio begins only after that tap. The page is self-contained and works offline. Use the chapter selector, shadow distance and lantern sliders, four scene presets, and the completion/failure buttons to compare states. Start at a comfortable volume, especially with headphones.

## Direction and proposed routing

- **Journey motif:** an eight-second, sparse two-note phrase with a low lantern foundation. Change the palette at chapter boundaries (currently every ten playable levels). Six representative palettes are selectable here: First Deliveries, Broken Crossings, Waterline, Echo District, Blackout, and Last Journey. The other chapters need individual review before production mapping.
- **Shadow:** close, wavering minor-second notes with a faint filtered breath. The layer is silent when the nearest active shadow is at least five Manhattan tiles away, then rises continuously toward adjacency. It releases over roughly a second when distance increases. An inactive patrol should send a far/asleep value. It does not announce a legal move or future shadow position.
- **Low light:** a short lantern pulse appears at 45% of capacity, quickens at 25%, and reaches its fastest rate at 10%. A refill raises the percentage and drops the layer smoothly. Use `state.light / cap()` rather than absolute light count so beacon repairs and different levels behave consistently.
- **Completion:** a short, rising warm four-note resolution. **Failure:** a falling three-note phrase with a brief ambient dip. These are new listening directions; they do not replace current cues yet.

The prototype has a master volume, mute, gentle mix, and automatic pause when the page goes into the background. The important tone frequencies are above typical tiny-speaker bass rolloff, while the very low foundation is optional color. No constant alarm, high-pitched siren, or vibration loop is used.

## Integration boundary

**Review prototype only.** `index.html` and `campaign/feedback.js` are unchanged. The live campaign currently plays procedural step, shadow-near, house, repair, denied, complete, failure, and crossing events, with separate haptics. A production pass should mix this ambience beneath those events, avoid doubling the existing shadow-near cue, preserve the current sound toggle, and test actual phone-speaker balance. Chapter mapping and exact gain targets should be approved by listening first.

## Verification

Both review pages passed `node --check`; the new page was also checked against both manifests to confirm that all 18 courier and 19 shadow names appear. Automated audible playback was not confirmed: the available in-app browser refused a local `file:` URL under its URL policy. Open the HTML directly in a normal browser for listening review and test phone-speaker balance before approval.
