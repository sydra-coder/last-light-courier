# Regression Arena

Open `game/regression.html` in a browser. The arena uses the current game renderer, controls, power tray, repair flow, shadows, and completion rules. It is a separate 12×12 level and has its own browser save data. It does not replace or modify the 2,000 campaign levels.

For the Level 500 review, open `game/level-500-test.html`. It is a **12×12 test remix**, not the campaign's existing 20×20 Level 500. It has five houses, requires four deliveries, and contains every current power plus the same selectable hazard setups. Its save is separate from both the campaign and the Regression Arena. The depot now uses a blue compass beacon silhouette in all three board views so it reads differently from delivery houses.

The fifth house in this remix stays hidden until the other four are lit; its access road opens at the same time. Reveal Pulse remains an optional early reveal for testing. House number circles are hidden across the game so the house and depot artwork remains visible. The campaign's 100 existing Beacon maps still use their authored reveal timing until their routes are revalidated against this new rule.

Use the **Hazards** selector to keep the same board and switch between **All hazards**, **Roads & crossings**, **Weather & light**, **Shadow pressure**, and **Circuit & travel**. **Replay fresh** resets position, deliveries, power uses, repair spending, and arena progress while keeping the selected setup. Each of the nine implemented powers begins with ten charges; the wallet begins with at least 10,000 points. A power can be used once per run. Long press an icon for its explanation; tap to apply it.

On the compact phone view, the bulb opens a route hint, `ⓘ` opens or closes the latest map message, `?` explains map symbols, and the nine powers appear in a two-row labeled tray. The full 12×12 board is visible, so the camera jump controls are omitted from these two test pages.

The map has four houses. Deliver to any three and return to the blue depot. The marked outer route is a reliable completion route, so each setup remains replayable even if a test changes a side road. The fourth house and side routes allow interaction tests.

## Feature coverage

| Setup | Features on the fixed board |
| --- | --- |
| Roads & crossings | Repairable boulder, fading road, ice, dark road, switch and gate, collapsing road, light bridge, hidden road and house, one-way road, first-delivery closure, route signal choice |
| Weather & light | Aftershock, flood, wind shift, quake, nightfall and fog, day/night road |
| Shadow pressure | Three patrol routes, spawner, merge/split, 2×2 influence, sentinel, hunter, shadow door and lock |
| Circuit & travel | Recharge house, shadow leech, lumen relay, light transfer, overload gate, transit link, second-delivery chain event |
| All hazards | The above features combined; use the focused setups when isolating a behavior |

Powers: Anchor Trap, Decoy Light, Reveal Pulse, Lumen Flask, Road Repair, Light Bridge, Map Stabilizer, Freeze Seal, and Rewind. The retired Echo Shadow is excluded from the current game rules. The arena exercises live mechanics, but it is not a proof of every possible interaction between them.

## Rebuild and smoke test

From the repository root:

```powershell
node game/build.cjs
node game/build-regression.cjs
node game/regression-smoke.cjs
```

The smoke test checks both review builds for the 12×12 layout, tester inventory, browser errors, power use and fresh replay, and a valid completion route in every setup. `game/regression-all-hazards-review.png` and `game/level-500-test-review.png` are mobile-size captures.
