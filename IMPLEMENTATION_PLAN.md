# Last Light Courier implementation plan

Status: a standalone browser campaign preview with 100 playable levels is available; no Android game built or tested. Name provisional.

Interactive design walkthroughs: [Level 01 route-drawing study](LEVEL_01_DESIGN_PREVIEW.html) and [Level 02: The Crossing, tap to move](LEVEL_02_DESIGN_PREVIEW.html). Level 02 uses one adjacent tile tap per turn with no Go button, shows safe neighboring moves, and includes the fading crossing. The [earlier Level 02 route-drawing study](LEVEL_02_ROUTE_DRAWING_ARCHIVE.html) is retained for reference; tap to move is the selected direction. These are authored design studies, not production builds. The next playable level is not yet implemented.
The [tap-to-move control example](TAP_TO_MOVE_EXAMPLE.html) mirrors the Level 02 interaction for comparison and review.

Campaign preview: [Play all 100 levels](CAMPAIGN_100_LEVELS.html). Its generated level data is in [CAMPAIGN_LEVELS.json](CAMPAIGN_LEVELS.json), with the editable builder in `campaign/`. The [100-level plan and repair economy](LEVELS_001_100_AND_REPAIRS.md) supplies each level brief, chapter, and repair price. This reflects the later tap-to-move direction and supersedes the route-drawing and 20-light assumptions below for future design work, pending prototype playtests.

## Shared assumptions

- Android first, portrait orientation, offline single player, one-finger controls, 2–10 minute rounds.
- Small team and simple 2D art: flat colors, geometric shapes, icons, short particles, and clear sound cues.
- Use a pinned stable Godot 4 release with GDScript if starting fresh. Confirm engine/export requirements at implementation time. Build an Android test APK during the first prototype week, then test on a real phone throughout.
- Estimates assume one focused developer at roughly 25–35 hours per week. They are planning ranges, not delivery promises.
- Each game gets its own project and test build. Start production on only one after both paper designs and a small prototype review.

## 1. Last Light Courier

### Player promise

Deliver light to stranded houses, then get home before your lantern dies. Each delivery makes the map more dangerous and valuable. A round should last 3–6 minutes.

### The differentiating rule

The player draws a route **one segment at a time** on a compact grid. Light is both the travel budget and the safe area: each move consumes one unit, while lit houses create temporary safe islands. The player can end a route at any delivered house to bank its value, but must reach the depot to bank the whole chain. This needs testing; it is a proposed identity, not a claim of market novelty.

### First playable rules

1. Start at the depot with 20 light units on an 8x8 grid. Show the light cost of a proposed route before commitment.
2. Tap adjacent cells to extend the route; tap the previous cell to undo the uncommitted segment. Tap **Go** to execute the visible route. The courier moves automatically; the player may stop at each house.
3. Deliver to 3 houses. Each house gives points and a small light refill. After each delivery, one telegraphed hazard activates on the map.
4. Return to the depot to bank all points. If the light reaches zero, the round ends and only previously banked points count.
5. Keep hazard behavior deterministic for a given seed. Hazards must be visible before the player commits a route.
6. Show a collision forecast, but let the player commit a warned route. The courier can be caught when the shadow and courier enter the same tile on the same step; route choice changes that outcome.

The first prototype uses only one hazard: a moving shadow that advances one cell whenever the courier moves. Do not add combat, inventory, or a story campaign until the route-and-return decision is fun.

### Controls and feedback

- Large cells and a reachable bottom action button; no precise drag gesture required.
- Drawn route shows expected light use, destination value, and shadow collision in distinct colors and symbols.
- Start each level preview with a short, skippable visual intro for the route, light budget, banking, and shadow. Show the shadow and courier entering the same tile in a before-and-after diagram; allow the intro to be reopened at the decision point.
- A short animation shows each move and delivery; allow speed-up after the tutorial.
- Failure card explains exactly why the run ended and offers instant retry with the same seed.

### Technical slices

| Slice | Deliverable | Acceptance check |
|---|---|---|
| A. Board | Fixed grid, depot, houses, route input, undo, route preview | Route cost is correct and impossible routes cannot execute. |
| B. Run loop | Light meter, delivery, refill, bank/fail, restart | A complete round can be played with plain shapes in 3–6 minutes. |
| C. Hazard | One deterministic moving shadow and its preview | Players can predict its next move without guessing. |
| D. Variety | Seeded layouts, 2 more hazard types only if needed | 10 consecutive rounds produce meaningful route choices. |
| E. Phone polish | Android build, safe areas, sound, haptics, accessibility, save best score | One-hand use is comfortable on a real phone; no clipped UI. |

### Art and content budget

One 8x8 board style, depot, 3 house icons, courier marker, shadow marker, 5 UI icons, 4 short effects, and about 6 sounds. Grid colors and icon shapes must remain readable without color vision. Use generated layouts only after a validator confirms reachable houses and a feasible return path; include a few authored tutorial boards.

### Risks and test gates

- **Too much calculation:** If players spend most of the round studying numbers, shorten the board or add a clearer route preview.
- **Too little agency:** If the correct route is obvious, add a second delivery choice or a visible optional reward before adding hazards.
- **Unfair loss:** Simulate hazards along the entire previewed route, not just at its endpoint.
- **Go/no-go after prototype:** In 5–8 fresh-player tests, most players should understand delivery and return after one tutorial round, and at least several should choose an immediate retry without prompting. Record actual round times and confusion points rather than assuming the target is met.

### Level 02 difficulty study

The Crossing tests a tighter light budget: 16 starting light, +2 per delivery, six blocked streets, and the same one-shadow rule. A three-house route is possible with only two light left if the player changes the shadow timing at the gate and returns by the lower road. Early return banks a smaller score. These values are design experiments, not locked production rules.

### Schedule estimate

Plain-shape phone prototype: 1–2 weeks. Tuning and content: 2–3 weeks. Polish, device testing, and release preparation: 2–3 weeks. Total: roughly 5–8 weeks if the first prototype passes its gate.


