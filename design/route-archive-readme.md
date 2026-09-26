# Route archive and hints

`map-solutions-200.json` stores 341 shortest completion routes for the current 200 maps. Every route was replayed through the actual game movement logic; light, house mask, both patrol phases, crossing timers and activation matched every recorded step. There is one no-repair route per map and a purchased-repair variant for 141 maps. Completion means required houses plus depot; other valid routes exist.

`map-route-archive-200.pdf` gives each route its own numbered map, arrows and move/light table. JSON coordinates are zero-based; PDF coordinates are one-based. Starting state is step zero.

## Rebuild after expansion

1. Generate updated map data with `python campaign/build_levels.py`.
2. Run `node campaign/archive_routes.cjs <output-directory>` to solve and archive all generated maps. This also updates the archive in `design/`.
3. Run `python campaign/export_routes_pdf.py --catalog <catalog.json> --output <routes.pdf>` to create its matching PDF. The PDF exporter currently embeds Windows Arial fonts.
4. Replay each route against the actual movement logic before releasing it. Archive fingerprints detect map/rule changes; fingerprints are version markers, not proof of validity.

## Player-state hints

`route-solver.js` is a pure solver. `window.__campaign.hintRoute()` exposes a continuation from the current state in the browser preview. It returns `solved` with ordered positions and state snapshots, `no_solution`, `restart_needed`, or `complete`. Calling it does not move the player or spend light, items or hints. Verified mid-run continuations finished successfully both with and without the map repair. An insufficient-light case returned no solution without changing its input.

The Hint button now requests the shortest safe next-house route and asks for approval before spending inventory. Numbered animated arrows remain visible while the player follows that route; stepping elsewhere clears them. Three hints are supplied initially, one claimable reward is earned per ten unique completions, and held inventory is capped at five. Gem purchases and the ghost-courier demonstration remain in the shop/hints implementation plan. When integrating them, calculate a continuation from actual remaining light, house mask, patrol phases, Echo trail, crossing timers and terrain. Run larger future searches in a worker so the interface stays responsive. Never substitute a stored starting route for an invalid current-state continuation, and do not charge a hint when the search cannot produce a valid route.

Current routes assume fixed purchased terrain: no mid-route buying/drilling actions. When token drilling or required repairs are implemented, add those actions, available inventory and modified terrain to the solver state. Regenerate this archive for the new rules, and mark no-repair variants as impossible where appropriate rather than inventing a route.
