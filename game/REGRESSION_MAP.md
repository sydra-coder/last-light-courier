# Regression Arena

Open `game/regression.html` in a browser. The arena uses the current game renderer, controls, power tray, repair flow, shadows, and completion rules. It is a separate 12×12 level and has its own browser save data. It does not replace or modify the 2,000 campaign levels.

Use the **Hazards** selector to keep the same board and switch between **All hazards**, **Roads & crossings**, **Weather & light**, **Shadow pressure**, and **Circuit & travel**. **Replay fresh** resets position, deliveries, power uses, repair spending, and arena progress while keeping the selected setup. Each of the nine implemented powers begins with ten charges; the wallet begins with at least 10,000 points. A power can be used once per run. Long press an icon for its explanation; tap to apply it.

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

The smoke test checks the 12×12 layout, tester inventory, browser errors, power use and fresh replay, and a valid completion route in every setup. `game/regression-all-hazards-review.png` is its mobile-size capture.
