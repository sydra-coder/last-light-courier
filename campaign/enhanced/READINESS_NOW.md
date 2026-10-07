# Last Light Courier: current 2,000-level readiness

Updated 2026-10-07 (India time). **Status: playable candidate, not final for review.**

## Directly testable now

- Open `Start-2000-Level-Playtest.bat` from the workspace root, or open `design/campaign-2000-preview/index.html`. All 2,000 levels are selectable.
- The filterable, 14-column workbook is `outputs/01a1112f-b897-7c03-a6b3-f25018e9f557/Last_Light_Courier_2000_Level_Playtest_Status.xlsx`. Its `Review state` and `No-power shortest?` columns distinguish recorded completions from proven minima.
- `audit_all_current_defaults.cjs` replays one current default route on every level: **2,000/2,000 complete** under the generated preview rules. This includes required free repairs and required Light Bridge uses. Completion with zero light is legal under the current rules.
- Current live checks also pass: **1,000/1,000** late assigned-power routes, **125/125** depot-signal branches, **100/100** transit rides, **1,425** event routes repeated with matching first/second-delivery states, **13,600** successive hint segments, all 2,000 workbook/preview rows, and launcher/package integrity.
- Representative revised maps have completed in a rendered 390-pixel browser viewport with no horizontal overflow or browser errors. This is a browser review check, not a physical-phone acceptance result.

## Work before final review

1. **Route quality and lantern fairness.** The workbook marks 218 default rows as exact no-power minima; 1,414 still say `No - reference only`. Four former default certificates (1,807, 1,828, 1,980, 1,994) were withdrawn when their road closures changed; their shorter signaled certificates remain where independently verified. The late default-route lantern median is two light, and 616 of 1,000 late references finish with 0–2 light. These are route-specific results, not proof that ordinary players have a fair margin. Broader actor-aware search and playtesting must resolve short unrecorded routes and over-tight alternatives.
2. **Choice and map-event quality.** The current `signal-choice-distinction-audit.json` compares actual route coordinates: 114 of 125 signal pairs still differ by at most two visited tiles per branch, and 111 have identical recorded steps and finishing light. None of the pairs now use the exact same tile sequence. Levels 1,805, 1,807, 1,817, 1,828, 1,980 and 1,994 now have verified detours that make signaling four to eight moves faster; 1,807, 1,828 and 1,994 retain their independently certified signaled minima. Most other signal maps still need stronger route design. Level 1,943 has a verified 88-move default shortcut that conflicts with its signaled branch under a reduced cap. Six later districts (1,001–1,500 and 1,801–1,900) remain below the current house-order variety threshold. Event replay verifies the recorded routes, not every reachable post-event state.
   - A fresh 1,801–1,900 phase search found many shorter paths in a simplified road graph, but full-rule replay completed only **4/100** default and **4/100** signaled candidates. The rest mostly collided with actors or other dynamic rules. The completed 60-move default route for level 1,804 (formerly 62, finish 16 light) is now promoted into the live hints and workbook after staged default and signaled hint replay. Both branches still take 60 moves, so its choice design remains open. See `current-phase-default-search-replay.json` and `current-phase-signal-search-replay.json`.
3. **Phone and player review.** The full set has not been played visually on a physical phone, and no human acceptance pass has judged whether the hazards, powers and repeated motifs remain readable and fun across all 2,000 levels.

The larger evidence trail is in `BUILD_STATUS.md`. No map should be called final solely because its recorded route completes or because its geometry differs from another map.
