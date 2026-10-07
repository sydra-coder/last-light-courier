# Last Light Courier — 2,000-level test guide

For the current readiness verdict and remaining review gates, see `campaign/enhanced/READINESS_NOW.md`.

Double-click `Start-2000-Level-Playtest.bat` or open `design/campaign-2000-preview/index.html` directly. Choose **Level map**, then type any level number in **Jump to any level**. The picker also has 20 districts with 10 chapters and 10 levels each. All 2,000 levels are selectable in this review build. The **Route book** card shows the selected map's houses, lantern light, shadows, hazards, event, and assigned test power. Type a number or hover/focus a level button to preview it, then use **Play previewed level**. Tapping a level number still starts it immediately.

Each level's assigned sample tool has one review charge on every reset, even if its earned inventory is empty. **Restart level** resets the map and its sample charge. Other earned tools use saved inventory.

If earlier preview tests left repairs or progress active, open the main menu and choose **Start fresh test (clear preview save)**. The confirmation clears only this 2,000-level review build; the older game save stays separate.

On a phone-sized window, tap **Zoom map** to inspect the larger tiles. The zoomed view follows the courier after each move; **Fit map** restores the overview. Use the direction buttons below the map for movement when tiles are small.

The workbook `outputs/01a1112f-b897-7c03-a6b3-f25018e9f557/Last_Light_Courier_2000_Level_Playtest_Status.xlsx` is the compact level index. Filter **Live map event**, **Other live hazards**, **Assigned power**, or **Review state**. **Shadow actors** counts patrols, Hunters, and Sentinels; influence fields and spawner zones appear under hazards. A blank power/alternate step cell means no such route length has been verified. Only rows marked **Yes** under **No-power shortest?** have an exact no-power minimum. Levels 125, 150, 175, and 200 need a free repair; their exact minimum is in **Power / alternate steps**.

The completion screen awards route stars only where a minimum is verified for the way you played. Later maps and optional power runs still save completion and show your personal best without claiming an unknown shortest path.

Hints on levels 201–2,000 can show the next segment of a route replayed through the game rules. They work while your current state matches that route. The hint asks for approval before using one charge; rejecting it or reaching a different state spends nothing. On Light Bridge maps, the dialogue first asks you to build the bridge with its level-provided charge, then resumes the verified route hint.

## First checks

| Test | Level | What to try |
| --- | ---: | --- |
| Movement and deliveries | 1 | Light a house, return to the depot, and compare lantern light. |
| First patrol | 8 | Deliver once, then watch the shadow's next unsafe tile. |
| Tight light | 41 | Finish with about two light on the shortest route. |
| Anchor Trap | 101 | Lay a trap on a highlighted patrol tile; the captured patrol must stop for the rest of the run. The recorded sample uses tile (5, 2). |
| Anchor Trap return route | 124 | Try trapping the second patrol on tile (11, 10) after moving near it. The map's recorded powered completion lays it after step 25; the captured shadow stays still while you finish. |
| Decoy Light | 151 | Place a decoy near a patrol after the first delivery. |
| Reveal Pulse | 201 | Reveal the hidden house and sealed road before the Beacon delivery. |
| Early 2×2 shadow field | 201 | Deliver once. The four outlined streets turn pink and block entry; the recorded completion route stays beside them. |
| Light Bridge | 701 | Build the marked bridge after the first delivery. The level supplies its charge. A required house sits beyond the crossing; leave its lane through the marked one-way road. |
| Lumen Flask | 1001 | Restore up to three lantern light. |
| Road Repair | 1002 | Reopen the marked road after the first-delivery closure. |
| Repair a broken causeway | 402 | Cross the fragile tile, then use Road Repair after it collapses. |
| Repair a quake road | 902 | After the first delivery closes the marked road, use Road Repair to reopen it. |
| Repair an aftershock | 952 | Wait for the eight-move closure, then use Road Repair on the marked road. |
| Map Stabilizer | 1003 | Keep that marked road open by using the tool before the first delivery. |
| Stabilize a quake | 901 | Use Map Stabilizer to keep the marked road open when the first delivery opens the new quake road. |
| Stabilize an aftershock | 951 | Use Map Stabilizer before or after the eight-move countdown; the marked road stays open. |
| Freeze Seal | 1401 | Hold both patrols for three courier moves. |
| Rewind | 1402 | Undo a move, including its delivery and map event if one occurred. |
| Depot signal route choice | 1805 | Try the road closure without signaling, then restart and signal at the depot. The verified default detour takes 68 moves; the signaled route takes 62. Check whether the newly closed street and six-move difference are easy to see. |
| Longer depot-signal detour | 1817 | Repeat the comparison. The default closure has a verified 70-move route and finishes with four light; signaling keeps a 62-move route that finishes with twelve. Check whether the altered crossing reads clearly before committing. |

Freeze Seal changes patrol timing. On some maps, using it immediately after the first delivery can block the recorded route; try it after a tight crossing. The assigned power was replayed to completion on every level from 1,001–2,000, with a later Freeze Seal use point on 15 maps.

## Map-change checkpoints

| Levels | Event to inspect |
| ---: | --- |
| 201, 301, 401, 501 | Early 2×2 shadow field, Leech recharge, causeway, then Sentinel and Hunter. |
| 601, 801, 951 | Shadow Door timing, earthquake road swap, then an eight-move aftershock. |
| 899, 943, 953, 960, 974, 982 | The six repaired quake maps have a marked 2×2 shadow field. After delivery, check that it blocks the short straight path while a winding route remains usable. Level 974's field wakes after the second delivery. |
| 1101, 1201, 1301 | Night/day moon road, growing Shadow Spawner, then split-light relay and voltage gate. |
| 1001, 1101, 1203, 1301, 1410, 1502, 1609, 1701, 1811 | One revised street map from each later district. Check whether side streets offer useful choices while the map event still matters. |
| 1006, 1010, 1011, 1013, 1016, 1017, 1018, 1020, 1045, 1046, 1047, 1055 | Storm district maps revised after alternate direct-route checks. Check whether the wind and road closure remain meaningful. |
| 1103, 1204, 1304, 1412, 1506, 1602, 1703, 1800, 1802 | Later maps revised after several direct-route choices were tested. Levels 1204, 1800, and 1802 have tighter streets; check route choice and readability. |
| 1113 | A marked one-way road now blocks the known 102-step direct route. Enter the tile from its arrow side, then check whether the nightfall route choice and arrow remain clear at phone size. |
| 315, 338, 399, 406, 430, 500, 525, 557, 630, 664 | Revised middle-band shortcuts. Check the new street wall on each map; 406, 557, 630, and 664 also gain a timed 2×2 field. Level 525 moves its existing Hunter den; check whether that chase is readable. |
| 819, 865, 866, 891, 940 | Newly added 2×2 shadow fields block five legal direct routes found by alternate route choices. Check field timing and whether the detour remains readable. |
| 1516, 1709 | Two especially tight revised street maps. Check route readability and whether the path feels too constrained. |
| 1501, 1601, 1701 | Paired events, second-delivery road change, then optional transit. |
| 1801, 1901, 2000 | Player-selected closure, combined mastery pattern, and final campaign map. |
| 1901, 1926, 1951, 1976, 2000 | Sample each of the four final event combinations, then the last map. On 1951, try both depot-signal choices. |
| 1902, 1904, 1939, 1959, 1963 | Finale maps with added 2×2 shadow fields. Check the timing and whether alternate routes remain clear. On 1959 and 1963, try both depot signals. |
| 1905, 1910, 1916, 1926 | Finale maps with revised branching streets. Look for meaningful route choices and note if any fast path feels too straight or bypasses the event. |
| 1901, 1904, 1909, 1914, 1917, 1923, 1934, 1941, 1953, 1954, 1962, 1965, 1966, 1974, 1997 | Finale street revisions after alternate direct-route checks. Level 1901 is the tightest; check that each remains readable and offers useful choices. |

The four finale combinations now recur in a staggered order, with at most five consecutive maps of the same type. Level 2000 is the full gauntlet. Please note if the street shapes still feel too similar despite the changing events.

Map changes use authored timing. The depot signal in selected later levels is a player choice. No random map event is used in this build. A repeat replay of 1,425 event routes, including 125 signal choices, produced identical first-delivery, second-delivery, and finish states after reset. This checks those routes; other player choices can still lead to a losing state.

**Bridge dependency review:** Earlier versions of 26 maps in 701–800 had verified routes around the bridge. Those known bypasses now have one additional wall each; all 26 powered reference routes still finish. The prior bypass routes and 1,148 fresh detour candidates fail in the revised preview. This finite screen does not prove that building the bridge is mandatory. The workbook leaves no-power route steps blank until a completing route or a rigorous dependency proof exists. Check the revised streets and bridge payoff on levels 702, 703, 706, 750, and other maps in the band.

## What has been checked

The generated preview's movement rules complete one current recorded route on every level (2,000/2,000), and all 125 recorded depot-signal alternate routes complete. Each of the nine tools has one completed sample route. These checks run the game rules without rendering the browser interface.

Representative maps have been checked in a rendered 390-pixel browser viewport. Physical-phone play, unusual player routes, later powered minima, and individual polish still need review. The 33 straight shortcuts found in levels 101–200 were revised; all 100 exact routes in that band now have no straight run over 12 tiles. Direct-route audits prompted street revisions on 83 maps in levels 1001–1900, 12 additional Storm maps, 79 additional later maps, and 15 finale maps. Level 1113 adds a one-way road to block the remaining known direct tour. Their known direct tours and screened recalculated tours now fail under the game rules. These screens do not prove global shortest routes. Please note the level number, the move just before the problem, the selected tool or signal, and whether the map was reset when reporting an issue.
On a phone, use **Zoom map** to enlarge dense grids; it follows the courier as you move. **Fit map** restores the full overview. The Zoom and appearance controls now have larger tap targets, but the isometric map still needs actual phone-size visual and touch testing.
