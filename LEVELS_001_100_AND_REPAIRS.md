# Last Light Courier — 100-level campaign and repair economy

Status: 100 playable browser levels now exist in [CAMPAIGN_100_LEVELS.html](CAMPAIGN_100_LEVELS.html). Their layouts are generated from these briefs and have automated route checks; numbers, difficulty, and visual clarity still require player playtesting.

## Player loop

1. Tap an adjacent safe tile. Each move spends 1 lantern light and advances the shadow one step.
2. Deliver light to a house. It becomes visibly **DONE**, awards points **at risk**, and refills 2 light (up to the level's cap).
3. Return to the depot to **bank** points. Being caught or running out of light loses only points still at risk.
4. Spend banked points between attempts on a *permanent repair on that level's map*. The repaired tile stays open on retries and is visible before starting.
5. Bank points from any 2 of 3 houses to clear a normal level. Deliver all 3 for a gold completion and a small mastery bonus. Levels 10, 20, …, 100 require all 3 houses as chapter finales. A player may bank one house and retry while learning; previously banked points stay in the wallet.

**No softlocks:** Every level must have a feasible two-house return route without spending. A required chapter finale must have a feasible three-house route before repairs. Repairs make safer, shorter, or higher-scoring routes possible; they never substitute for solving the shadow timing. If a player spends poorly, they can replay cleared levels for points. Show the shortest known *light cost* of a repair's new route before buying it, without exposing the hidden next-shadow tile.

## Points and rewards

- Chapter `c` is 1–10. Each level has three houses worth **120 / 180 / 240 + 30 × (c − 1)** points respectively. Thus a chapter 1 full delivery banks 540; chapter 10 banks 1,350 before bonuses.
- All three houses and a safe return award a **100 + 25 × (c − 1)** mastery bonus. This bonus is banked only on that successful return.
- A result screen separates **deliveries**, **mastery bonus**, **banked this run**, **wallet**, and **best result**. Remaining light is a medal criterion, not spendable currency; the player should never confuse it with banked points.
- Replays can earn points again, but the same house pays only once per run. This keeps a poor purchase from blocking progress. Before release, tune replay earnings against the first 20 levels to avoid farming a trivial level becoming the fastest strategy.
- Repairs are purchased only from a map preview between runs. No purchase prompt appears mid-run, and a purchase never changes a live route unexpectedly.

### Repair price rule

Prices scale by chapter so late shortcuts remain meaningful. `c` is the chapter containing the level.

| Price band | Formula | Ch. 1 | Ch. 5 | Ch. 10 |
|---|---:|---:|---:|---:|
| Small | 150 + 75 × (c − 1) | 150 | 450 | 825 |
| Route | 300 + 100 × (c − 1) | 300 | 700 | 1,200 |
| Major | 500 + 125 × (c − 1) | 500 | 1,000 | 1,625 |

The purchase card must show the exact price, the tiles affected, and a before/after route sketch. A repaired tile stays repaired on that level. Buying one repair never silently buys another. For the first pass, offer at most two purchases on any map and typically one.

## Obstacle catalogue

| Obstacle | First level | Player-visible behavior | Repair | Price band |
|---|---:|---|---|---|
| Fallen crates | 3 | One tile blocks a short street. | Clear crates; opens one shortcut tile. | Small |
| Rubble | 6 | Two adjacent tiles make a detour. | Clear one marked tile. | Small |
| Broken streetlamp | 9 | A dark tile is safe to enter but costs 2 light. | Relight it; tile returns to 1 light. | Small |
| Locked alley gate | 13 | A gate blocks a parallel route. | Open the gate permanently. | Route |
| Cracked footbridge | 16 | A crossing is unusable from the start. | Repair one bridge tile. | Route |
| Flooded road | 23 | Water forces a long edge route. | Drain one marked road tile. | Route |
| Collapsed tunnel | 29 | A two-tile tunnel is closed. | Reopen the tunnel entrance and exit as one project. | Major |
| Jammed switch gate | 34 | The gate opens only from a switch and closes after several turns. | Install a permanent manual latch; switch puzzle remains on other routes. | Route |
| Fallen tower | 46 | A three-tile obstacle divides the board. | Clear one central passage through it. | Major |
| Frozen canal | 53 | A crossing works only for a few turns after first use. | Build a stable crossing beside it. | Major |
| Shadowed arch | 68 | The shadow patrol passes through a choke point. | Repair a side arch; the shadow still patrols normally. | Route |
| Broken beacon | 89 | A district has reduced lantern capacity until restored. | Restore capacity for this level only. | Major |

**Hazards that stay:** Echo Shadow, fading crossing timers, moving shadows, and timing gates are level rules. Points may open alternative roads around them, but cannot remove the shadow or disable failure. This preserves the route-choice game.

## Difficulty design rules

- Introduce one new idea on a forgiving board, then combine it with known ideas over the next levels. Each chapter's level 10 is a recap, not a surprise mechanic.
- Increase difficulty through route branches, light margins, patrol timing, and return-path decisions. Do not just add more blocked cells.
- Keep tap choices readable on a phone: usually 8×8; at most 9×9 in the final two chapters, with cells large enough for one-thumb play.
- Show all currently safe adjacent moves. Mark an unsafe immediate shadow collision as blocked without showing a separate future-shadow marker. Distinguish a purchased shortcut, a temporary crossing, and a completed house by icon as well as color.
- A new rule gets a skippable, playable tutorial on its first level. The player can reopen it from pause. Retry returns instantly to the same board and shadow phase.
- Design targets: early 5–8 moves of light spare on a good two-house return, middle 3–5, late 1–3. These are targets to validate with a solver and playtests, not fixed promises.
- For every level, validate: a no-repair two-house route, a no-repair finale three-house route where required, all bought-repair states, shadow timing, lantern nonnegative at arrival, and a return to depot. Record shortest safe route and at least one deliberately tempting but recoverable detour.

## 100-level outline

Each row is one authored level brief. `S`, `R`, and `M` are the Small, Route, and Major prices above. A dash means no purchase. A proposed purchase opens the named shortcut; the normal route remains playable.

### Chapter 1 — First Deliveries (1–10)

Teach tapping, light, banking, one shadow, and the difference between a short unsafe path and a longer safe one. 8×8, 16–20 starting light.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 1 | Tutorial: one house, return, bank; then reveal the other houses. | — |
| 2 | Choose between two nearby houses before returning. | — |
| 3 | First blocked street and a visible detour. | Clear crates (S). |
| 4 | Shadow wakes after the first delivery. | — |
| 5 | Wait by choosing a safe side step to alter patrol timing. | — |
| 6 | Rubble splits two possible return routes. | Clear rubble (S). |
| 7 | Full three-house run with generous light. | — |
| 8 | Early banking versus one more distant house. | — |
| 9 | First 2-light dark tile; take it or go around. | Relight streetlamp (S). |
| 10 | Finale: three houses, one shadow, safe return. | Clear central crates (R). |

### Chapter 2 — Broken Crossings (11–20)

Introduce fading crossings and stable bridge purchases. 8×8, roughly 16–19 light.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 11 | Cross a bridge before its visible timer expires. | — |
| 12 | Return by a different street after crossing fades. | — |
| 13 | Locked alley makes the return longer. | Open alley gate (R). |
| 14 | Shadow patrol meets bridge timing. | — |
| 15 | Choose which house to visit before crossing. | — |
| 16 | Broken footbridge hides a safer return. | Repair footbridge (R). |
| 17 | Fading bridge with two viable lower detours. | — |
| 18 | One delivered house lies across a fading bridge. | — |
| 19 | Repair or take a tight shadow-timed detour. | Clear rubble (S). |
| 20 | Finale: three houses, bridge timer, bank at depot. | Repair side bridge (M). |

### Chapter 3 — Waterline (21–30)

Introduce flood detours and one-way-feeling routes without actual one-way controls. 8×8, 17–20 light.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 21 | Flood divides near and far houses. | — |
| 22 | Return around a water edge while shadow loops. | — |
| 23 | Flooded road creates an appealing shortcut. | Drain road (R). |
| 24 | Two delivery orders with different light costs. | — |
| 25 | A fading crossing bypasses the flood briefly. | — |
| 26 | Dark lamp tile competes with a longer safe route. | Relight lamp (S). |
| 27 | Patrol crosses the dry edge at a fixed rhythm. | — |
| 28 | Three-house attempt requires banking or tight routing. | — |
| 29 | Collapsed tunnel offers a broad shortcut. | Reopen tunnel (M). |
| 30 | Finale: flood edge, crossing, three-house loop. | Drain central road (R). |

### Chapter 4 — Switchyard (31–40)

Introduce a switch tile that opens a gate for four moves. Its countdown is shown after activation, like the fading crossing.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 31 | Step on switch, pass gate, return another way. | — |
| 32 | Switch is off the shortest path. | — |
| 33 | Shadow timing changes while reaching the switch. | — |
| 34 | Gate can be latched open permanently. | Install latch (R). |
| 35 | Choose between switch route and longer road. | — |
| 36 | Rubble blocks a convenient approach to switch. | Clear rubble (S). |
| 37 | Two houses are reachable within one gate window. | — |
| 38 | Bridge timer and switch timer overlap. | — |
| 39 | Optional shortcut saves three light but faces patrol. | Repair side crossing (M). |
| 40 | Finale: three houses and a gate you cannot linger in. | Install gate latch (R). |

### Chapter 5 — Echo District (41–50)

Introduce Echo Shadow: after a delivery it repeats the courier's last few moves on a delayed trail. Show its current trail clearly; never hide an immediate collision.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 41 | Playable Echo Shadow tutorial on an open board. | — |
| 42 | Make a loop, then avoid your own echo. | — |
| 43 | Choose which house wakes the echo first. | — |
| 44 | Echo trail and normal shadow share the board. | — |
| 45 | An alley gives a second exit from a loop. | Open alley (R). |
| 46 | Fallen tower divides echo-safe routes. | Clear tower passage (M). |
| 47 | Use a side step to let the echo pass. | — |
| 48 | Fading crossing closes behind the echo. | — |
| 49 | Optional lamp helps an extended detour. | Relight lamp (S). |
| 50 | Finale: three houses, echo loop, depot return. | Repair side bridge (R). |

### Chapter 6 — Winter Canal (51–60)

Introduce temporary ice crossings: they are safe for a fixed number of moves after first step. Contrast them with permanent purchased bridges.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 51 | Cross ice once, leave before it breaks. | — |
| 52 | Compare ice shortcut with long land route. | — |
| 53 | Stable crossing can replace risky ice. | Build canal bridge (M). |
| 54 | Shadow reaches shore on the same turn. | — |
| 55 | House order changes which shore you finish on. | — |
| 56 | Rubble adds two moves to the winter return. | Clear rubble (S). |
| 57 | Echo trail follows the ice entry. | — |
| 58 | Switch gate gives a second way off the canal. | — |
| 59 | Route shortcut costs points but saves light. | Open shore gate (R). |
| 60 | Finale: three houses split across two shores. | Build side bridge (M). |

### Chapter 7 — Shadow Market (61–70)

Introduce two distinct patrol lanes, never two indistinguishable shadow markers. A purchase opens an escape route but does not remove either patrol.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 61 | Second shadow introduced on a separate lane. | — |
| 62 | Cross between patrol lanes safely. | — |
| 63 | Two houses are close but their exits differ. | — |
| 64 | Narrow shortcut bypasses one patrol lane. | Open gate (R). |
| 65 | Echo and second patrol activate at different houses. | — |
| 66 | Dark streetlamp consumes precious light. | Relight lamp (S). |
| 67 | Decide when to bank rather than chase house three. | — |
| 68 | Shadowed arch hides a side route. | Repair side arch (R). |
| 69 | Switch timing intersects both patrol lanes. | — |
| 70 | Finale: three houses, two patrols, one return. | Clear tower passage (M). |

### Chapter 8 — Old City (71–80)

Combine known rules on denser maps. Keep icons and safe-move outlines readable. 8×8 or 9×9 after phone testing.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 71 | Two looping streets, one closer to the depot. | — |
| 72 | Fading bridge cuts the inner loop. | — |
| 73 | Broken arch opens a third return route. | Repair arch (R). |
| 74 | Echo repeats a tempting short loop. | — |
| 75 | Time a switch while carrying two deliveries. | — |
| 76 | Flooded central tile splits the board. | Drain road (R). |
| 77 | Dark lamp penalizes the fastest geometric route. | Relight lamp (S). |
| 78 | Three-house route has several safe orders. | — |
| 79 | Collapsed tunnel creates a mastery shortcut. | Reopen tunnel (M). |
| 80 | Finale: city loops, echo, crossing, depot. | Clear central rubble (R). |

### Chapter 9 — Blackout (81–90)

Use tighter lantern caps and longer return routes. The final repair restores capacity on one map; other levels remain solvable at their starting cap.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 81 | Start with less light; deliver nearby first. | — |
| 82 | Refill timing matters at house two. | — |
| 83 | Short but shadow-timed route versus safe long route. | — |
| 84 | Streetlamp fixes a 2-light tile. | Relight lamp (S). |
| 85 | Ice crossing and low lantern cap. | — |
| 86 | Broken bridge opens a more efficient loop. | Repair bridge (R). |
| 87 | Echo trail makes an efficient route risky. | — |
| 88 | Bank two houses, then replay for mastery. | — |
| 89 | Broken beacon lowers capacity on this map. | Restore beacon (M). |
| 90 | Finale: three refills needed to return. | Open old tunnel (M). |

### Chapter 10 — Last Light (91–100)

Final synthesis: each level has a different route insight, not merely a larger maze. 8×8 or carefully tested 9×9.

| Level | Main challenge | Optional repair |
|---:|---|---|
| 91 | Choose a delivery order that preserves light. | — |
| 92 | Two shadows leave one safe timing window. | — |
| 93 | Echo crosses the apparent shortcut. | — |
| 94 | Bridge timer closes the outward route. | Repair side bridge (R). |
| 95 | Switch opens an exit but costs a detour. | — |
| 96 | Dark lamp competes with a patrol detour. | Relight lamp (S). |
| 97 | Flood and ice create two changing crossings. | — |
| 98 | Tunnel repair supports a shorter mastery route. | Reopen tunnel (M). |
| 99 | Practice board: all mechanics, generous retry. | — |
| 100 | Finale: light all three houses, evade both shadows and echo, return to depot; town fully lights up. | Restore final bridge (M). |

## Build order and validation

1. Lock the tap-to-move rules using levels 1–10; update the older route-drawing plan once tested.
2. Implement purchases and persistent per-level repairs with levels 3, 6, 9, and 10. Confirm point earning, wallet, purchase preview, save/load, and retry.
3. Build one complete chapter at a time. Author and playtest each ten-level set before producing the next, so later prices and light margins reflect real completion times.
4. Use a route solver to check every repair state and a small group of new players to check readability. If players misunderstand a rule, fix its tutorial or map language before increasing difficulty.
5. Target 3–6 minutes per normal level and 5–8 for finales. If levels become repetitive, reduce the count or add stronger route decisions rather than padding the campaign.
