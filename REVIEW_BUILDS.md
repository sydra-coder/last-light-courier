# Two game builds

Run `node game/build.cjs` to generate both builds from the same 2,000-level campaign preview.

| Build | Open | Save and inventory |
| --- | --- | --- |
| Player | [game/index.html](game/index.html) | Normal milestone unlocks and earned charges. Every five newly cleared levels adds one hint automatically, up to five; overflow waits until a hint is spent. |
| Tester | [game/tester.html](game/tester.html) | Separate local save and run records. Starts with all nine implemented powers unlocked, ten charges of each, five hints, and 10,000 banked points. All 2,000 levels can be selected. |

Tester charges are seeded once. Spending them reduces inventory normally, so power use and shop restocks can be tested. The nine current powers are Anchor Trap, Decoy Light, Reveal Pulse, Lumen Flask, Road Repair, Light Bridge, Map Stabilizer, Freeze Seal, and Rewind. Some powers become usable only when the current map has their target or trigger. Earthquake and Storm are map events in this build; proposed map-wide inventory versions are still design work.

The Play board fills the available phone width. Status and counters are compact; tap a message to expand it, use `?` for map symbols, and long-press a power icon for details. Tap the same power icon again or its × button to close the details. Maps larger than 12×12 open in a scrollable view showing about 12×12 tiles at phone size. “Fit map” shows the whole layout; level geometry is unchanged.

The board now loads the original object art from `design/board-objects`. Permanent blockers vary between rocks, trees, and thorn bushes. A damaged, clearable obstacle has a yellow tile border; tapping it shows the level's repair cost. If the courier can safely enter it on the next move, **Repair & move** opens the road and spends the cost together. Distant taps, cancelled actions, and invalid moves spend nothing. Cleared tiles become plain road. Lit houses have warm windows and a green tile border. Timed switches use idle, active, and expiring artwork.

Run `node game/repair-art-smoke.cjs` and `node game/dual-build-smoke.cjs` for the repair transaction and player/tester checks. Open the HTML files with their folder structure intact so the art paths resolve.
