# Last Light Courier — Mechanic Lab

Open [`index.html`](index.html) to play 16 separate experimental levels. Select any trial in the left/top list. Tap highlighted adjacent tiles, use the D-pad, or use keyboard arrows. Space waits one turn; R retries. Action buttons appear when the courier approaches a relevant feature. The guide button gives a short clue.

Each trial asks the courier to light all houses, test its mechanic, and return to a depot. The alternate-depot trial specifically ends at the east depot. These are small rule prototypes, not edits to the 200-level game or the 1,000-map catalogue. No game saves, purchases, gems, or hint inventory are read or changed. The stage powers are free one-use samples for design review; their final names, costs, and earn rules are undecided.

The sixteen trials correspond to the sixteen ideas in the early-mechanics shortlist: house-triggered route, shadow trap, signal bell, 3×3 ward, hidden houses, repair fork, tunnel, flood, storm, earthquake, rotating junction, nightfall, one-use bridge, shadow-route switch, alternate depot, and stage-earned powers.

Trial 1 now has two valid orders. House 2 can be reached before House 1 by taking the longer south road. Delivering to House 1 opens an east gate shortcut to House 2. The route test found completions in both orders (20 turns when House 1 opens the gate first; 24 turns when House 2 is visited first). These are example completion routes for the lab, not a claim about production-level minimums.

In Trial 2, the player has one shadow trap in inventory. Approach the marked patrol tile and use **Lay shadow trap**. When the moving patrol enters that tile, it becomes immobile for the rest of the run. Its occupied tile remains dangerous to enter. The trap is consumed when laid and can be restored by retrying the trial. The delivery only counts after the patrol has actually been caught.

`test-lab.cjs` explores the deterministic state space and found a completion route for every level. It also verifies both repair bridges and Flare, Anchor, and Sense on the power trial. This proves reachability in the prototype engine; phone-size readability, fun, balance, and production-game parity still need hands-on review. The lab intentionally uses compact maps and generous light so the new rule is the focus.
