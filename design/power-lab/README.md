# Power Lab — nine playable power samples

Open `index.html` locally. Select a power on the left, use the free charge, light the house, and return to the depot. These are isolated design tests; the 200-level playable campaign and the archived 1,000 maps are unchanged.

| Sample | Proposed campaign milestone | Demonstrates |
| --- | ---: | --- |
| Anchor Trap | 111 | Player lays a trap; a shadow entering it cannot move for the rest of the run. |
| Decoy Light | 131 | A false light draws the shadow off the crossing for four turns. |
| Reveal Pulse | 211 | Reveals and opens a hidden short crossing. |
| Lumen Flask | 311 | Restores six light, limited by lantern capacity. |
| Road Repair | 411 | Permanently opens a broken road for that run. |
| Freeze Seal | 511 | Freezes a shadow in place for four moves. |
| Light Bridge | 711 | Opens a gap for fourteen moves, including the return. |
| Map Stabilizer | 811 | Cancels the scheduled quake before it closes the return road. |
| Rewind | 1411 | Undoes the last move, restoring light and map/shadow state. This is a recovery sample, so the untouched route also wins. |

Every sample gives one free charge. The event timeline is fixed; no random map changes occur. The sample solver in `test.cjs` searches the available move, wait and power actions to confirm a completion. It also checks whether a run with no power can complete; only Rewind intentionally allows that. The tests establish rule-level reachability, not visual acceptance or campaign balance.

The Excel plan remains a proposal. Unlock levels and power rules can be changed after hands-on review. A campaign map needs a full state solver and human playtest before any of these powers is integrated.
