# Final 100 map contact sheets

`render_finale_atlas.py` renders the actual embedded preview map data and the recorded route for levels 1901–2000. Each sheet shows 25 maps. Dark tiles are walls, cyan is the recorded courier route, amber dots are houses, red marks are patrol loops, and the white dot is the depot.

## Source review

- All 100 routes visibly turn and cover different house placements. The recorded routes remain readable in this enlarged contact-sheet rendering.
- A serpentine street motif repeats within each 25-level group. This deserves normal-play feedback; the contact sheet cannot establish that every map feels distinct.
- Four mechanically different combinations are represented: storm/fog, shadow spawner/light network, chosen closure/light network, and the combined gauntlet. They are now staggered across the final 100 maps, with no more than five consecutive maps sharing one combination. Level 2000 remains a combined gauntlet. `audit_mastery.py` checks the underlying event fields and authored route proofs.

## Playtest picks

Try levels 1901, 1926, 1951, 1976, and 2000, then choose at least one map you have not seen from each 25-level group. For level 1951, try both depot-signal choices. Check whether the routes feel meaningfully different and whether any map is too long or visually hard to read on a phone.

These sheets inspect saved geometry only. Browser rendering, touch controls, event feedback, and phone readability remain open review checks.
