# Region shadow art plan — 2,000-level campaign

Open [region-shadow-review.html](region-shadow-review.html) for the visual comparison, [region-shadow-art-contact-sheet.png](region-shadow-art-contact-sheet.png) for the full contact sheet, and [region-shadow-map.json](region-shadow-map.json) for the complete district assignments. Twenty new, individually named transparent district PNGs are included alongside the 19 earlier silhouette studies. These are generated concept assets; there are no gameplay or rule changes.

## Decision proposed for review

- Assign one shadow appearance by district. District `floor((levelNumber - 1) / 100) + 1` covers each 100-level span; resolve appearance when the level starts. The player does not choose or buy shadow appearances.
- Apply the district appearance to both patrols and the Echo. Echo uses the same silhouette at lower opacity and a cooler, paler edge. Keep the current indicator of unsafe movement and avoid making Echo disappear against the dark board.
- Keep the approved deep-navy storybook night-village palette, amber lantern and window light, raised roads, and violet hazard language. Each new sprite has a deliberate district-specific treatment. The scenery and accents in the JSON are design proposals, not approved final environment art.
- Keep seasonal shadow treatments separate from the campaign mapping. A holiday does not silently override a level's region identity.

## District map

| District / levels | Shadow | Reason | Tile-size review |
|---|---|---|---|
| 1 Ember Road / 1–100 | 01 Night Wisp | Familiar starting form, returns in finale | Strong |
| 2 Dimming Crossroads / 101–200 | 12 Crescent Lurker | Forked negative space | Strong |
| 3 Veiled Hamlet / 201–300 | 11 Moth Veil | Misty folded silhouette | Strong |
| 4 Lantern District / 301–400 | 09 Bell Hollow | Broad silhouette beside lamps | Strong |
| 5 Broken Causeways / 401–500 | 14 Ink Puddle | Low crossing shape | Check floor separation |
| 6 Hunting Dark / 501–600 | 18 Serpent Coil | Watchful coil | Strong; no new ability |
| 7 The Shadowworks / 601–700 | 13 Shard Mask | Constructed facets | Strong |
| 8 River of Glass / 701–800 | 07 Canal Mist | Cool watery edge | Check reflective floor |
| 9 Quake Frontier / 801–900 | 15 Thorn Crown | Fractured outline | Check fine tips |
| 10 Faultline City / 901–1000 | 08 Old City Cinder | Damaged city ash | Same wisp outline as 01; consider 13 if too similar |
| 11 Storm March / 1001–1100 | 10 Ribbon Wraith | Wind-torn ribbons | Check thin profile |
| 12 The Long Night / 1101–1200 | 16 Eclipse Orb | Bold dark disk | Strong |
| 13 Breachlands / 1201–1300 | 17 Veil Hand | Ruptured reaching edge | Check readability; no grab |
| 14 The Lumen Engine / 1301–1400 | 13 Shard Mask | Machine-like facets | Reuse with restrained cool rim proposed |
| 15 Keeper's Arsenal / 1401–1500 | 19 Hourglass Shade | Pinched armored form | Check narrow profile |
| 16 Convergence / 1501–1600 | 12 Crescent Lurker | Intentional returning form | Reuse with darker core proposed |
| 17 The Moving Kingdom / 1601–1700 | 18 Serpent Coil | Clear mobile silhouette | Reuse with no motion-rule implication |
| 18 Last Provinces / 1701–1800 | 09 Bell Hollow | Familiar form near last homes | Reuse with softer edge proposed |
| 19 Black Horizon / 1801–1900 | 16 Eclipse Orb | Round outline at skyline | Reuse with minimal halo proposed |
| 20 The Last Light / 1901–2000 | 01 Night Wisp | First shadow returns as bookend | Reuse with subtle lighter rim proposed |

## Environment approval still needed

The **overall** home/navigation reference is approved: [five-screen-concept.png](../home-navigation/five-screen-concept.png). It does not establish final environment assets for any of the 20 districts. The campaign supplies the district names and map mechanics, while this plan infers scenery from those names. Before production art, approve the road/building/water/sky treatment for each district, especially Broken Causeways, River of Glass, The Lumen Engine, The Moving Kingdom, Black Horizon, and the finale. Keep the same phone-scale hazard contrast across all three board views.

## Visual QA before implementation

Review the assignments on actual gameplay boards at normal phone size, including bright lantern tiles and the Night view. The generated art has more fine detail than the earlier silhouette studies. Specifically inspect district art 03, 07–11, and 13–15, whose outer edges and small details compress most in the phone-tile samples. Test 05 against dark floors and 08 against water reflections. The review HTML only places concepts on representative tiles; it does not prove normal-play readability. Confirm patrol and Echo can be distinguished while retaining the existing danger cues. If a candidate fails, simplify its outer shape or use its assigned earlier silhouette study.

## Art generation status

All 20 district PNGs were generated as separate transparent raster concepts with the built-in image generation tool. The prompts share the production intent: isolated dark-violet hazard, pale eyes, vivid violet edge, centered sprite, 48 px readability, and no scenery or new ability. Each prompt then specifies its district's silhouette and material accent. The exact source filename for each concept is recorded in `region-shadow-map.json`. The contact sheet was visually inspected at both art and tile scale. Animation, final sprite cleanup, and normal-play contrast remain unverified.
