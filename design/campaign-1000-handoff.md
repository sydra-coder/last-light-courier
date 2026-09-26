# Last Light Courier - 1,000-map expansion handoff

## Delivered scope

- 1,000 actual map records, numbered 001-1000. Original maps 001-200 are preserved from the current campaign snapshot.
- 800 new seeded layouts with usable branching streets, distributed delivery houses, loops, two permanent patrols and Echo. Patrol and Echo behavior remains unchanged.
- Eight progression bands: 201-300 and 301-400 use 18 x 18 grids and eight houses; 401-500 and 501-600 use 20 x 20 and nine houses; 601-700 and 701-800 use 22 x 22 and ten houses; 801-900 and 901-1000 use 24 x 24 and eleven houses.
- Wall density generally decreases as the campaign advances, creating more route choices. Every new map's open ground is connected after any mandatory repair. Light is budgeted against a verified route after a local shortcut search, with smaller reference margins in later bands.
- 32 repair-required maps: every 25th level from 225 through 1000. Before repair, mandatory houses lie in disconnected districts. Every such map specifies its own reserved free repair. After repair, a verified completion exists.
- Every map has a verified reference route with per-move position, remaining light, delivered-house mask, patrol phases, Echo trail and crossing timers. The archive contains 1,141 routes including the original repair variants.

## Files

- `CAMPAIGN_1000_LEVELS.json`: complete map catalogue.
- `design/map-solutions-1000.json`: complete solution archive. Original 200-map routes retain their archived shortest-route status. The 800 new-map routes are valid reference completions, **not globally shortest solutions**.
- `campaign/levels_001_200.snapshot.json`: preserved baseline.
- `campaign/expansion/build_1000.py`: deterministic generation and independent rules replay.
- `campaign/expansion/validate_live.py`: archive replay against the existing production game's movement code, with rendering suppressed for speed. This checks logic and state agreement, not phone visual acceptance.
- `campaign/expansion/export_review.py`: full level review and numbered route-table PDFs.

User deliverables are copied to the project `outputs` folder. The level review has one page per map plus its introduction and progression table. The route archive paginates long routes rather than shrinking their move tables.

## Status and integration boundary

This delivery is a map/data/review package. It does not replace the active 200-map HTML or APK, and does not overwrite the other chat's hint implementation. The new maps can be integrated from the catalogue without regenerating the original 200 layouts.

For 201-1000, `repairGemPrice`, `repairRequired` and `reservedFreeRepair` are design/integration metadata. `repair.cost` matches the proposed gem amount; it must not be fed directly into the legacy points-based purchase UI. Points remain score in the planned economy. Required maps must receive their reserved free repair action before release, so they cannot become a paid progression lock.

Integration should expand level navigation and chapter labels to 100 chapters, retain existing completion records, and provide the reserved repair action. Treat `routeStatus` as reference-route information; do not display its length as a global minimum. The current exhaustive hint/minimum search needs performance work for larger open maps, more houses and multiple delivery orders.

## Verification and remaining review

Generator checks cover unique new layouts, contiguous movement, houses, depot completion, lantern consumption, all shadow phases and Echo restrictions, gate timing, fading crossings and ice. A separate production-code replay checks every stored route and its light/mask/patrol state. Disconnected-house checks prove the required repairs are genuinely necessary.

The difficulty rise is structural and arranged in bands, with variation within each band. These are seeded map families, not 800 individually playtested puzzles. Global route optimization, alternate house-order balance, optional repair value, phone readability and player difficulty still require focused playtesting. Valid routes alone do not establish those outcomes.

## Rebuild

From the repository root:

```powershell
python campaign/expansion/build_1000.py
python campaign/expansion/validate_live.py
python campaign/expansion/export_review.py
```

Regenerate routes and PDFs after any map or movement-rule change. Keep state-aware hints tied to the current live game state; a stored starting route is not a replacement for recalculating after the player takes a different path.
