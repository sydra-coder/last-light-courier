# Last Light Courier — level navigation concepts

## Recommendation: Lantern Road

A winding lane climbs through one ten-level village chapter at a time. Completed stops glow like lit houses; the next stop has a courier lantern and a warm halo; unplayed stops are numbered brass plaques. Every tenth stop is a chapter landmark, such as a depot, bridge, bell tower or repaired gate. This adapts the references' readable path and large markers to the game's night village. Keep each level number outside decorative art, with at least a 44 px touch target. The review prototype opens in this direction.

## Alternative: Repair Ledger

The same chapter path is drawn as a surveyor's route on dark parchment. Completed levels gain a stamped seal; a repair milestone gets a small bridge/gate sketch. This is more compact and useful if 100 chapter browsing needs to feel like an archive, but its paper metaphor is less atmospheric during play.

## Alternative: Shadow Watch

The journey is viewed from a watchtower at dusk: cool violet roads, occasional shadow silhouettes, and warm windows marking completed deliveries. This could emphasize danger and progression, but avoid putting shadows under level numbers or implying that a level's gameplay hazard can be predicted from the map.

## Navigation and data decisions

- 100 chapters × 10 levels; chapter number and exact level range remain visible. A chapter jump accepts 1–100, and a level jump accepts 1–1000.
- The prototype reads the active game's `last-light-courier-campaign-v1` save when both pages share an origin. It shows actual cleared levels 1–200. With no readable save, it shows no fabricated completion.
- “Current” means the first uncleared playable level. Any unplayed level 1–200 can still be selected, matching the current game's open level navigation.
- Levels 201–1000 are archived/planned map records. Selection shows their status and range, with no play button.
- Playable selection links to `../../index.html?level=N`; the active game's URL handler opens that level. This prototype does not modify the engine or save.
- The chapter page is intentionally a short segment of a much longer road. Controls jump directly rather than asking the player to scroll through all 1,000 stops.

## Reference interpretation

`winding-map-reference.png`: the S-shaped route and numbered, prominent stops are useful; avoid its bright shop/currency hierarchy. `chapter-path-reference.png`: the tall, scrollable path and landmarks are useful; replace generic stars with courier deliveries and repair imagery. Use the existing isometric-village direction for houses, bridges, depth and warm lit windows, without suggesting that the map changes gameplay rules.
