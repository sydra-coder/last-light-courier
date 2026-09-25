# Last Light Courier — complete 100-level handoff

This is the exact board-data handoff for the standalone browser campaign. Use it with [CAMPAIGN_LEVELS.json](CAMPAIGN_LEVELS.json) and [CAMPAIGN_100_LEVELS.html](CAMPAIGN_100_LEVELS.html). The JSON is the machine-readable authority; this document makes every level inspectable without running the game.

## Current status and scope

- 100 distinct 8×8 playable boards, ten chapters, one-tile tap controls, 41 repair opportunities.
- Every listed full-delivery route was checked in the browser engine with no purchase; it reaches all three homes and returns to the depot. The road-repair projects were checked to save two moves on a shortest all-house route in the static map.
- This is a first-pass generated campaign, not 100 hand-tuned production levels. The level briefs express design intent; some named scenery is currently represented by the same blocked-tile rule. The routes prove playability, but difficulty, pacing, visual identity, partial-return choices, and touch clarity still need player review.
- An Android build does not exist. The browser campaign saves its wallet, level clears, tutorials, best scores, and level-specific repairs in local storage.

## Rules implemented in the browser

1. Tap one orthogonally adjacent green tile. Ordinary entry costs 1 light; an unrepaired dark tile costs 2. The courier and each active patrol advance one turn per tap.
2. A first visit to a house adds its points to the at-risk total and refills 2 light, capped at the level start capacity. Its tile becomes **DONE**. The first delivery wakes the shadow patrols.
3. A red neighboring tile would be occupied by a shadow after the tap and is disabled. The next shadow tile is not separately marked. A completed house acts as a safe island for collision checking.
4. Echo Shadow, when present, retraces the courier trail. Its displayed position is from two moves earlier; the move the echo would occupy next is blocked.
5. A fading crossing starts at 5 on first entry; thin ice starts at 4. Each subsequent move reduces its timer. At 0 the tile closes for that run. A switch sets its gate timer to 4; a bought latch holds that gate open.
6. Returning to the depot after at least one delivery banks that run and ends it. Level 1 clears with 1 house; ordinary levels clear with at least 2; every tenth level requires 3. Banking all 3 also awards the chapter mastery bonus.
7. If light reaches zero on a non-house, non-depot move, the lantern-out card shows the at-risk points lost. Banked wallet points are never lost. Repairs are purchased before moving, use banked wallet points, and persist on that specific level.
8. All 100 levels are selectable in the design preview, even before clearing earlier levels. Production progression gating is still a design decision.

### Coordinates and map legend

Coordinates are **zero based**: (0,0) is top left; x increases right and y increases downward. Map rows are y=0–7, with x=0–7 from left to right.

`D` depot; `A/B/C` houses in point-value order; `#` blocked tile; `R` blocked repair tile; `f` fading crossing; `i` thin ice; `d` two-light dark tile; `s` switch; `g` timed gate; `.` ordinary road. A lamp, latch, or beacon repair changes the named feature rather than replacing a blocked tile. Shadow patrols are specified below each map because their positions change every turn.

A route such as `R3 D2 L1` means three right taps, two down taps, then one left tap from the depot. It is one verified **full three-house return**, not the only solution. It uses no repair.

### Points and repair bands

In chapter c (1–10), houses A/B/C award 120/180/240 + 30×(c−1) each. The all-house bonus is 100 + 25×(c−1). Small repairs cost 150 + 75×(c−1); route repairs 300 + 100×(c−1); major repairs 500 + 125×(c−1). Every entry below lists its actual price.

## Chapter index

| Chapter | Levels | Theme | Start light | Repairs |
|---:|---:|---|---:|---:|
| 1 | 1–10 | First Deliveries | 20–22 | 4 |
| 2 | 11–20 | Broken Crossings | 20–22 | 4 |
| 3 | 21–30 | Waterline | 21–28 | 4 |
| 4 | 31–40 | Switchyard | 21–28 | 4 |
| 5 | 41–50 | Echo District | 20–25 | 4 |
| 6 | 51–60 | Winter Canal | 18–23 | 4 |
| 7 | 61–70 | Shadow Market | 19–24 | 4 |
| 8 | 71–80 | Old City | 20–25 | 5 |
| 9 | 81–90 | Blackout | 18–25 | 4 |
| 10 | 91–100 | Last Light | 18–25 | 4 |

## Level-by-level boards

### 001 — First Deliveries

**Design brief:** Tutorial: one house, return, bank; then reveal the other houses.

**Goal:** bank 1 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,1), lantern 20.

**Houses:** A Lantern Row (6,3) = 120 pts; B East Watch (3,6) = 180 pts; C The Mill (1,3) = 240 pts.

```text
    01234567
0   #......#
1   #...D..#
2   ....#...
3   .C....A.
4   ..##....
5   ....#...
6   ...B....
7   ...#....
```

**Hazards:** first patrol (4,6) → (5,6) → (5,7) → (4,7); initial index 0. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `R2 D5 L5 U5 R3`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 002 — First Deliveries

**Design brief:** Choose between two nearby houses before returning.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,3), lantern 20.

**Houses:** A Lantern Row (2,6) = 120 pts; B East Watch (6,4) = 180 pts; C The Mill (4,1) = 240 pts.

```text
    01234567
0   ........
1   ....C...
2   #.......
3   .D......
4   ...##.B.
5   ..#.##.#
6   ..A.....
7   #.....##
```

**Hazards:** first patrol (5,3) → (6,3) → (6,4) → (5,4); initial index 1. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `D3 R5 U5 L5 D2`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 003 — First Deliveries

**Design brief:** First blocked street and a visible detour.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,6), lantern 22.

**Houses:** A Lantern Row (1,2) = 120 pts; B East Watch (6,1) = 180 pts; C The Mill (6,6) = 240 pts.

```text
    01234567
0   #.....##
1   ......B.
2   .A......
3   ...#....
4   ..#.....
5   ...#..R.
6   .D....C.
7   #..#.##.
```

**Hazards:** first patrol (3,1) → (4,1) → (4,2) → (3,2); initial index 0. No timed tile on this board.

**Repair:** Clear crates at (6,5); S band, **150 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U5 R5 D3 R1 D2 L6`. 22 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 004 — First Deliveries

**Design brief:** Shadow wakes after the first delivery.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,6), lantern 20.

**Houses:** A Lantern Row (5,6) = 120 pts; B East Watch (6,1) = 180 pts; C The Mill (1,1) = 240 pts.

```text
    01234567
0   ......#.
1   .C....B.
2   #.......
3   .....#..
4   ..#.....
5   ..#.....
6   #D...A..
7   ........
```

**Hazards:** first patrol (6,2) → (7,2) → (7,3) → (6,3); initial index 0. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `R5 U5 L5 D5`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 005 — First Deliveries

**Design brief:** Wait by choosing a safe side step to alter patrol timing.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,6), lantern 20.

**Houses:** A Lantern Row (1,4) = 120 pts; B East Watch (4,1) = 180 pts; C The Mill (6,4) = 240 pts.

```text
    01234567
0   ........
1   ....B...
2   .......#
3   .......#
4   .A....C.
5   ...#.#.#
6   #..D...#
7   .......#
```

**Hazards:** first patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 0. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `L2 U5 R5 D5 L3`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 006 — First Deliveries

**Design brief:** Rubble splits two possible return routes.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,3), lantern 22.

**Houses:** A Lantern Row (2,6) = 120 pts; B East Watch (6,4) = 180 pts; C The Mill (4,1) = 240 pts.

```text
    01234567
0   .......#
1   ....CR.#
2   ..#.##..
3   .D#.....
4   #....#B.
5   .......#
6   #.A.....
7   ....#...
```

**Hazards:** first patrol (6,3) → (7,3) → (7,4) → (6,4); initial index 0. No timed tile on this board.

**Repair:** Clear rubble at (5,1); S band, **150 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `D3 R5 U6 L2 D1 L3 D2`. 22 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 007 — First Deliveries

**Design brief:** Full three-house run with generous light.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,1), lantern 20.

**Houses:** A Lantern Row (6,4) = 120 pts; B East Watch (2,6) = 180 pts; C The Mill (1,2) = 240 pts.

```text
    01234567
0   .#.#....
1   .....D..
2   .C..#...
3   #.#....#
4   ..#...A.
5   ....#...
6   ..B....#
7   ..#..#..
```

**Hazards:** first patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 0. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `R1 D5 L5 U5 R4`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 008 — First Deliveries

**Design brief:** Early banking versus one more distant house.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,4), lantern 20.

**Houses:** A Lantern Row (5,1) = 120 pts; B East Watch (1,3) = 180 pts; C The Mill (3,6) = 240 pts.

```text
    01234567
0   ........
1   #....A..
2   ........
3   .B.....#
4   ...#..D.
5   ........
6   #..C....
7   #.#.#...
```

**Hazards:** first patrol (1,2) → (2,2) → (2,3) → (1,3); initial index 0. No timed tile on this board.

**Repair:** none on this board.

**Verified no-purchase full route:** `U3 L5 D5 R5 U2`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 009 — First Deliveries

**Design brief:** First 2-light dark tile; take it or go around.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,6), lantern 21.

**Houses:** A Lantern Row (1,2) = 120 pts; B East Watch (6,1) = 180 pts; C The Mill (6,6) = 240 pts.

```text
    01234567
0   ..#.#...
1   ......B.
2   #A.#..d.
3   ........
4   ..#.....
5   #.......
6   .D....C.
7   .#.#....
```

**Hazards:** first patrol (6,2) → (7,2) → (7,3) → (6,3); initial index 0. two-light dark tile (6,2).

**Repair:** Relight streetlamp at (6,2); S band, **150 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `U5 R5 D5 L5`. 20 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 010 — First Deliveries

**Design brief:** Finale: three houses, one shadow, safe return.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,5), lantern 22.

**Houses:** A Lantern Row (6,1) = 120 pts; B East Watch (1,2) = 180 pts; C The Mill (2,6) = 240 pts.

```text
    01234567
0   .....#..
1   ..R...A#
2   .B#.##..
3   ..#....#
4   ........
5   ..#.#.D.
6   ..C.....
7   ...#..#.
```

**Hazards:** first patrol (0,4) → (1,4) → (1,5) → (0,5); initial index 0. No timed tile on this board.

**Repair:** Clear central crates at (2,1); R band, **300 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U4 L3 U1 L2 D6 R5 U1`. 22 moves, 6 light left, 640 points banked including the 100-point mastery bonus.

### 011 — Broken Crossings

**Design brief:** Cross a bridge before its visible timer expires.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,6), lantern 20.

**Houses:** A Lantern Row (2,6) = 150 pts; B East Watch (1,1) = 210 pts; C The Mill (6,1) = 270 pts.

```text
    01234567
0   #.####..
1   #B....C.
2   ........
3   .......#
4   .......#
5   .f..#...
6   ..A...D#
7   #.......
```

**Hazards:** first patrol (3,1) → (4,1) → (4,2) → (3,2); initial index 1. fading crossing (1,5).

**Repair:** none on this board.

**Verified no-purchase full route:** `L5 U5 R5 D5`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 012 — Broken Crossings

**Design brief:** Return by a different street after crossing fades.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,1), lantern 20.

**Houses:** A Lantern Row (1,1) = 150 pts; B East Watch (2,6) = 210 pts; C The Mill (6,5) = 270 pts.

```text
    01234567
0   ........
1   #A...D..
2   ..#.....
3   .f..#..#
4   ....##..
5   ..#...C.
6   ..B.....
7   ...#...#
```

**Hazards:** first patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 0. fading crossing (1,3).

**Repair:** none on this board.

**Verified no-purchase full route:** `L4 D5 R5 U5 L1`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 013 — Broken Crossings

**Design brief:** Locked alley makes the return longer.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,6), lantern 22.

**Houses:** A Lantern Row (1,5) = 150 pts; B East Watch (3,1) = 210 pts; C The Mill (6,3) = 270 pts.

```text
    01234567
0   .##...#.
1   #..BR...
2   ...##...
3   .f....C#
4   .......#
5   .A......
6   ....D..#
7   #.......
```

**Hazards:** first patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. fading crossing (1,3).

**Repair:** Open alley gate at (4,1); R band, **400 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `L3 U5 R2 U1 R2 D1 R1 D5 L2`. 22 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 014 — Broken Crossings

**Design brief:** Shadow patrol meets bridge timing.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,1), lantern 20.

**Houses:** A Lantern Row (1,5) = 150 pts; B East Watch (6,6) = 210 pts; C The Mill (6,1) = 270 pts.

```text
    01234567
0   #.....##
1   .D....C.
2   ..#.....
3   ........
4   ........
5   #A...#..
6   #.f...B.
7   #..#...#
```

**Hazards:** first patrol (5,3) → (6,3) → (6,4) → (5,4); initial index 1. fading crossing (2,6).

**Repair:** none on this board.

**Verified no-purchase full route:** `D5 R5 U5 L5`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 015 — Broken Crossings

**Design brief:** Choose which house to visit before crossing.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,1), lantern 20.

**Houses:** A Lantern Row (6,2) = 150 pts; B East Watch (4,6) = 210 pts; C The Mill (1,4) = 270 pts.

```text
    01234567
0   #...#..#
1   ...D...#
2   #..#..A.
3   #.#.....
4   .C....f.
5   ........
6   ....B...
7   ..##..##
```

**Hazards:** first patrol (0,5) → (1,5) → (1,6) → (0,6); initial index 0. fading crossing (6,4).

**Repair:** none on this board.

**Verified no-purchase full route:** `R3 D5 L5 U5 R2`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 016 — Broken Crossings

**Design brief:** Broken footbridge hides a safer return.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,3), lantern 22.

**Houses:** A Lantern Row (4,1) = 150 pts; B East Watch (1,4) = 210 pts; C The Mill (4,6) = 270 pts.

```text
    01234567
0   ....#.#.
1   ..f.A...
2   .R####..
3   ......D.
4   .B###...
5   ........
6   ....C...
7   ........
```

**Hazards:** first patrol (0,0) → (1,0) → (1,1) → (0,1); initial index 0. fading crossing (2,1).

**Repair:** Repair footbridge at (1,2); R band, **400 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U2 L6 D2 R1 D3 R5 U3`. 22 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 017 — Broken Crossings

**Design brief:** Fading bridge with two viable lower detours.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,6), lantern 20.

**Houses:** A Lantern Row (2,6) = 150 pts; B East Watch (1,1) = 210 pts; C The Mill (6,1) = 270 pts.

```text
    01234567
0   ##.#....
1   .B....C.
2   #....#..
3   #.......
4   #.#.....
5   .f......
6   ..A...D.
7   ...#.#..
```

**Hazards:** first patrol (3,1) → (4,1) → (4,2) → (3,2); initial index 1. fading crossing (1,5).

**Repair:** none on this board.

**Verified no-purchase full route:** `L5 U5 R5 D5`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 018 — Broken Crossings

**Design brief:** One delivered house lies across a fading bridge.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,1), lantern 20.

**Houses:** A Lantern Row (1,3) = 150 pts; B East Watch (4,6) = 210 pts; C The Mill (6,3) = 270 pts.

```text
    01234567
0   ..#.....
1   #..D...#
2   #.#.....
3   .A....C#
4   ...##...
5   .f.#.#..
6   ....B...
7   ...#....
```

**Hazards:** first patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 0. fading crossing (1,5).

**Repair:** none on this board.

**Verified no-purchase full route:** `L2 D5 R5 U5 L3`. 20 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 019 — Broken Crossings

**Design brief:** Repair or take a tight shadow-timed detour.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,5), lantern 22.

**Houses:** A Lantern Row (3,6) = 150 pts; B East Watch (1,2) = 210 pts; C The Mill (5,1) = 270 pts.

```text
    01234567
0   #....#..
1   #....C.#
2   .B.##...
3   ..#.##..
4   .R#.....
5   ....##D.
6   .f.A....
7   .......#
```

**Hazards:** first patrol (1,1) → (2,1) → (2,2) → (1,2); initial index 0. fading crossing (1,6).

**Repair:** Clear rubble at (1,4); S band, **225 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `D1 L5 U1 L1 U2 R1 U2 R5 D4`. 22 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 020 — Broken Crossings

**Design brief:** Finale: three houses, bridge timer, bank at depot.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,3), lantern 22.

**Houses:** A Lantern Row (4,1) = 150 pts; B East Watch (1,4) = 210 pts; C The Mill (4,6) = 270 pts.

```text
    01234567
0   #.#.....
1   ..f.A...
2   ........
3   ..#.#.D.
4   .B.#....
5   ...##...
6   ..R.C...
7   #...#...
```

**Hazards:** first patrol (1,4) → (2,4) → (2,5) → (1,5); initial index 1. fading crossing (2,1).

**Repair:** Repair side bridge at (2,6); M band, **625 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U2 L5 D6 R2 U1 R3 U3`. 22 moves, 6 light left, 755 points banked including the 125-point mastery bonus.

### 021 — Waterline

**Design brief:** Flood divides near and far houses.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,7), lantern 23.

**Houses:** A Lantern Row (0,5) = 180 pts; B East Watch (3,1) = 240 pts; C The Mill (6,4) = 300 pts.

```text
    01234567
0   #...#..#
1   ...B...#
2   f.......
3   .#......
4   .#....C.
5   A#...#.#
6   .....#..
7   ...D....
```

**Hazards:** first patrol (2,0) → (3,0) → (3,1) → (2,1); initial index 0. fading crossing (0,2).

**Repair:** none on this board.

**Verified no-purchase full route:** `L3 U6 R6 D6 L3`. 24 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 022 — Waterline

**Design brief:** Return around a water edge while shadow loops.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,6), lantern 24.

**Houses:** A Lantern Row (6,1) = 180 pts; B East Watch (0,0) = 240 pts; C The Mill (0,6) = 300 pts.

```text
    01234567
0   B...f...
1   ...#.#A#
2   d.......
3   ...#.#.#
4   .#......
5   .#..#...
6   C.....D#
7   ........
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 1. fading crossing (4,0); two-light dark tile (0,2).

**Repair:** none on this board.

**Verified no-purchase full route:** `U6 L6 D6 R6`. 24 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 023 — Waterline

**Design brief:** Flooded road creates an appealing shortcut.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,1), lantern 22.

**Houses:** A Lantern Row (6,2) = 180 pts; B East Watch (4,6) = 240 pts; C The Mill (1,4) = 300 pts.

```text
    01234567
0   ....##.#
1   ...D....
2   #.....A.
3   ..#.....
4   .C#...f.
5   #.##.#..
6   ..RdB...
7   #.....#.
```

**Hazards:** first patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 0. fading crossing (6,4); two-light dark tile (3,6).

**Repair:** Drain road at (2,6); R band, **500 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R3 D5 L3 D1 L2 U6 R2`. 22 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 024 — Waterline

**Design brief:** Two delivery orders with different light costs.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,3), lantern 21.

**Houses:** A Lantern Row (1,6) = 180 pts; B East Watch (6,4) = 240 pts; C The Mill (4,1) = 300 pts.

```text
    01234567
0   .......#
1   ....C...
2   .#.....#
3   D#......
4   ...#..B.
5   ...##...
6   .A..f...
7   ..#.....
```

**Hazards:** first patrol (6,6) → (7,6) → (7,7) → (6,7); initial index 0. fading crossing (4,6).

**Repair:** none on this board.

**Verified no-purchase full route:** `D3 R6 U5 L6 D2`. 22 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 025 — Waterline

**Design brief:** A fading crossing bypasses the flood briefly.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,4), lantern 26.

**Houses:** A Lantern Row (4,6) = 180 pts; B East Watch (0,3) = 240 pts; C The Mill (4,0) = 300 pts.

```text
    01234567
0   d...C...
1   ..#...#.
2   ........
3   B#....#.
4   ......#D
5   ...##.#.
6   .f..A...
7   ..#.....
```

**Hazards:** first patrol (0,0) → (1,0) → (1,1) → (0,1); initial index 0. fading crossing (1,6); two-light dark tile (0,0).

**Repair:** none on this board.

**Verified no-purchase full route:** `D2 L7 U6 R7 D4`. 26 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 026 — Waterline

**Design brief:** Dark lamp tile competes with a longer safe route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,7), lantern 28.

**Houses:** A Lantern Row (7,3) = 180 pts; B East Watch (2,0) = 240 pts; C The Mill (0,5) = 300 pts.

```text
    01234567
0   ..B...f.
1   d..#..#.
2   ........
3   ..##.#.A
4   ........
5   C..#..#.
6   .#....#.
7   ......D.
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. fading crossing (6,0); two-light dark tile (0,1).

**Repair:** Relight lamp at (0,1); S band, **300 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `R1 U7 L7 D7 R6`. 28 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 027 — Waterline

**Design brief:** Patrol crosses the dry edge at a fixed rhythm.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,0), lantern 23.

**Houses:** A Lantern Row (6,4) = 180 pts; B East Watch (2,7) = 240 pts; C The Mill (1,2) = 300 pts.

```text
    01234567
0   .....D..
1   ..#.#...
2   .C.##...
3   ...#...#
4   ....#.A.
5   ....##..
6   .....#.#
7   ..B...f.
```

**Hazards:** first patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 1. fading crossing (6,7).

**Repair:** none on this board.

**Verified no-purchase full route:** `R1 D7 L5 U7 R4`. 24 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 028 — Waterline

**Design brief:** Three-house attempt requires banking or tight routing.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,5), lantern 22.

**Houses:** A Lantern Row (3,7) = 180 pts; B East Watch (6,3) = 240 pts; C The Mill (3,1) = 300 pts.

```text
    01234567
0   .....#.#
1   ...C..d.
2   ...#....
3   ....#.B.
4   #.......
5   #D..#...
6   ....#...
7   ...A..f.
```

**Hazards:** first patrol (6,4) → (7,4) → (7,5) → (6,5); initial index 0. fading crossing (6,7); two-light dark tile (6,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `D2 R5 U6 L5 D4`. 22 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 029 — Waterline

**Design brief:** Collapsed tunnel offers a broad shortcut.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,1), lantern 22.

**Houses:** A Lantern Row (6,1) = 180 pts; B East Watch (5,6) = 240 pts; C The Mill (1,5) = 300 pts.

```text
    01234567
0   .#.#...#
1   #.D...A.
2   #.#.....
3   ......f.
4   ....##R.
5   .C......
6   ....dB..
7   .#...#..
```

**Hazards:** first patrol (5,5) → (6,5) → (6,6) → (5,6); initial index 0. fading crossing (6,3); two-light dark tile (4,6).

**Repair:** Reopen tunnel at (6,4); M band, **750 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R4 D2 R1 D2 L1 D1 L5 U5 R1`. 22 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 030 — Waterline

**Design brief:** Finale: flood edge, crossing, three-house loop.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,6), lantern 21.

**Houses:** A Lantern Row (6,4) = 180 pts; B East Watch (3,1) = 240 pts; C The Mill (1,4) = 300 pts.

```text
    01234567
0   #.##....
1   ...B....
2   ......f.
3   #.#...R.
4   .C...#A.
5   ........
6   ....D...
7   ......##
```

**Hazards:** first patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 1. fading crossing (6,2).

**Repair:** Drain central road at (6,3); R band, **500 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R2 U2 R1 U2 L1 U1 L5 D5 R3`. 22 moves, 5 light left, 870 points banked including the 150-point mastery bonus.

### 031 — Switchyard

**Design brief:** Step on switch, pass gate, return another way.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,6), lantern 28.

**Houses:** A Lantern Row (3,7) = 210 pts; B East Watch (0,2) = 270 pts; C The Mill (5,0) = 330 pts.

```text
    01234567
0   .d...C..
1   ...##...
2   B.###...
3   .#......
4   .#.#....
5   g#.#....
6   f#...#.D
7   .s.A....
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. fading crossing (0,6); two-light dark tile (1,0); switch (1,7); timed gate (0,5).

**Repair:** none on this board.

**Verified no-purchase full route:** `D1 L7 U7 R7 D6`. 28 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 032 — Switchyard

**Design brief:** Switch is off the shortest path.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,2), lantern 28.

**Houses:** A Lantern Row (0,7) = 210 pts; B East Watch (7,6) = 270 pts; C The Mill (6,0) = 330 pts.

```text
    01234567
0   ......C.
1   .#......
2   D..#....
3   .###.#.d
4   .....##.
5   .#......
6   ..#....B
7   A.s.fg..
```

**Hazards:** first patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 1. fading crossing (4,7); two-light dark tile (7,3); switch (2,7); timed gate (5,7).

**Repair:** none on this board.

**Verified no-purchase full route:** `D5 R7 U7 L7 D2`. 28 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 033 — Switchyard

**Design brief:** Shadow timing changes while reaching the switch.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,6), lantern 21.

**Houses:** A Lantern Row (0,2) = 210 pts; B East Watch (6,1) = 270 pts; C The Mill (6,6) = 330 pts.

```text
    01234567
0   ...#.#..
1   ..f...B.
2   A.......
3   ........
4   .....#..
5   ..#.....
6   D.....C#
7   #.##..#.
```

**Hazards:** first patrol (4,1) → (5,1) → (5,2) → (4,2); initial index 0. fading crossing (2,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `U5 R6 D5 L6`. 22 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 034 — Switchyard

**Design brief:** Gate can be latched open permanently.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,6), lantern 24.

**Houses:** A Lantern Row (6,2) = 210 pts; B East Watch (1,0) = 270 pts; C The Mill (0,5) = 330 pts.

```text
    01234567
0   .B...g..
1   d.....s#
2   ..#.##A.
3   ........
4   ..###..#
5   C.#.#...
6   .....D..
7   ......##
```

**Hazards:** first patrol (2,0) → (3,0) → (3,1) → (2,1); initial index 1. fading crossing (5,0); two-light dark tile (0,1); switch (6,1); timed gate (5,0).

**Repair:** Install latch at (5,0); R band, **600 points**; timed gate stays open after repair.

**Verified no-purchase full route:** `R1 U6 L6 D6 R5`. 24 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 035 — Switchyard

**Design brief:** Choose between switch route and longer road.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,1), lantern 24.

**Houses:** A Lantern Row (6,1) = 210 pts; B East Watch (7,7) = 270 pts; C The Mill (1,7) = 330 pts.

```text
    01234567
0   ......#.
1   .D....A.
2   ...#....
3   ..#....f
4   #..#.##.
5   #.#.#...
6   #..#....
7   #C...d.B
```

**Hazards:** first patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 0. fading crossing (7,3); two-light dark tile (5,7).

**Repair:** none on this board.

**Verified no-purchase full route:** `R6 D6 L6 U6`. 24 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 036 — Switchyard

**Design brief:** Rubble blocks a convenient approach to switch.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,4), lantern 21.

**Houses:** A Lantern Row (3,6) = 210 pts; B East Watch (6,3) = 270 pts; C The Mill (3,1) = 330 pts.

```text
    01234567
0   ........
1   ...CR..#
2   ..####..
3   ..#...B.
4   .D..#...
5   ...#....
6   ...Asfg.
7   ....#..#
```

**Hazards:** first patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 1. fading crossing (5,6); switch (4,6); timed gate (6,6).

**Repair:** Clear rubble at (4,1); S band, **375 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `D2 R5 U5 L1 U1 L2 D1 L2 D3`. 22 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 037 — Switchyard

**Design brief:** Two houses are reachable within one gate window.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,2), lantern 26.

**Houses:** A Lantern Row (7,7) = 210 pts; B East Watch (0,7) = 270 pts; C The Mill (1,1) = 330 pts.

```text
    01234567
0   #....#..
1   .C......
2   .#.#...D
3   ..##....
4   d...#.#.
5   ........
6   ..#.#.#.
7   B...f..A
```

**Hazards:** first patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 1. fading crossing (4,7); two-light dark tile (0,4).

**Repair:** none on this board.

**Verified no-purchase full route:** `D5 L7 U6 R7 D1`. 26 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 038 — Switchyard

**Design brief:** Bridge timer and switch timer overlap.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,0), lantern 24.

**Houses:** A Lantern Row (1,4) = 210 pts; B East Watch (5,7) = 270 pts; C The Mill (6,2) = 330 pts.

```text
    01234567
0   ..D.....
1   #..#....
2   ..#...C#
3   ..##...#
4   .A.##...
5   .s...#.#
6   ......d#
7   .g...B..
```

**Hazards:** first patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 1. fading crossing (1,7); two-light dark tile (6,6); switch (1,5); timed gate (1,7).

**Repair:** none on this board.

**Verified no-purchase full route:** `L1 D7 R5 U7 L4`. 24 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 039 — Switchyard

**Design brief:** Optional shortcut saves three light but faces patrol.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,1), lantern 21.

**Houses:** A Lantern Row (6,2) = 210 pts; B East Watch (4,6) = 270 pts; C The Mill (1,4) = 330 pts.

```text
    01234567
0   .#....##
1   ...D...#
2   ......A#
3   .......#
4   .C#...f.
5   .R.....#
6   ....B..#
7   .#....##
```

**Hazards:** first patrol (2,5) → (3,5) → (3,6) → (2,6); initial index 0. fading crossing (6,4).

**Repair:** Repair side crossing at (1,5); M band, **875 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R3 D5 L6 U2 R1 U3 R2`. 22 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 040 — Switchyard

**Design brief:** Finale: three houses and a gate you cannot linger in.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,6), lantern 22.

**Houses:** A Lantern Row (6,6) = 210 pts; B East Watch (5,0) = 270 pts; C The Mill (1,1) = 330 pts.

```text
    01234567
0   ...d.B..
1   #C......
2   ........
3   ...##.g#
4   ......s#
5   ....#...
6   #.D...A#
7   .#......
```

**Hazards:** first patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 1. fading crossing (6,3); two-light dark tile (3,0); switch (6,4); timed gate (6,3).

**Repair:** Install gate latch at (6,3); R band, **600 points**; timed gate stays open after repair.

**Verified no-purchase full route:** `R4 U6 L5 D6 R1`. 22 moves, 5 light left, 985 points banked including the 175-point mastery bonus.

### 041 — Echo District

**Design brief:** Playable Echo Shadow tutorial on an open board.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,6), lantern 23.

**Houses:** A Lantern Row (2,6) = 240 pts; B East Watch (0,1) = 300 pts; C The Mill (6,1) = 360 pts.

```text
    01234567
0   #.......
1   B.d...C.
2   ...#.##.
3   .....#..
4   .#..#...
5   f..###..
6   ..A....D
7   ..#.....
```

**Hazards:** first patrol (2,0) → (3,0) → (3,1) → (2,1); initial index 1. fading crossing (0,5); two-light dark tile (2,1); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L7 U5 R7 D5`. 24 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 042 — Echo District

**Design brief:** Make a loop, then avoid your own echo.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,4), lantern 20.

**Houses:** A Lantern Row (6,1) = 240 pts; B East Watch (1,3) = 300 pts; C The Mill (3,6) = 360 pts.

```text
    01234567
0   .#.#.#.#
1   ...gs.A.
2   ........
3   .B.##...
4   #......D
5   .....#..
6   #..C....
7   ....#..#
```

**Hazards:** first patrol (1,3) → (2,3) → (2,4) → (1,4); initial index 0. fading crossing (3,1); switch (4,1); timed gate (3,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `U3 L6 D5 R6 U2`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 043 — Echo District

**Design brief:** Choose which house wakes the echo first.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,4), lantern 25.

**Houses:** A Lantern Row (1,0) = 240 pts; B East Watch (6,2) = 300 pts; C The Mill (4,7) = 360 pts.

```text
    01234567
0   .A..f...
1   ........
2   .#..##B.
3   ....#...
4   D#.#.#..
5   ...###d.
6   .#.#...#
7   ....C...
```

**Hazards:** first patrol (6,3) → (7,3) → (7,4) → (6,4); initial index 1. fading crossing (4,0); two-light dark tile (6,5); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U4 R6 D7 L6 U3`. 26 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 044 — Echo District

**Design brief:** Echo trail and normal shadow share the board.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,3), lantern 21.

**Houses:** A Lantern Row (1,6) = 240 pts; B East Watch (6,4) = 300 pts; C The Mill (4,1) = 360 pts.

```text
    01234567
0   ......##
1   ....C...
2   .....#d#
3   D....#..
4   .....#B.
5   ..#..#..
6   .A.sg...
7   ....#.#.
```

**Hazards:** first patrol (6,4) → (7,4) → (7,5) → (6,5); initial index 0. fading crossing (4,6); two-light dark tile (6,2); switch (3,6); timed gate (4,6).

**Repair:** none on this board.

**Verified no-purchase full route:** `D3 R6 U5 L6 D2`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 045 — Echo District

**Design brief:** An alley gives a second exit from a loop.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,5), lantern 20.

**Houses:** A Lantern Row (1,1) = 240 pts; B East Watch (6,2) = 300 pts; C The Mill (5,6) = 360 pts.

```text
    01234567
0   ..#.....
1   .A.f...#
2   ..#...B.
3   .....#R.
4   ..##....
5   .D.....#
6   .....C..
7   ###.#..#
```

**Hazards:** first patrol (5,1) → (6,1) → (6,2) → (5,2); initial index 1. fading crossing (3,1); Echo Shadow active after first delivery.

**Repair:** Open alley at (6,3); R band, **700 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U4 R5 D1 R1 D2 L1 D2 L5 U1`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 046 — Echo District

**Design brief:** Fallen tower divides echo-safe routes.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,6), lantern 21.

**Houses:** A Lantern Row (6,5) = 240 pts; B East Watch (4,1) = 300 pts; C The Mill (1,3) = 360 pts.

```text
    01234567
0   ##......
1   ...dB...
2   .R###.g.
3   .C...#f.
4   #.....s#
5   ...#..A#
6   ...D....
7   ..#.....
```

**Hazards:** first patrol (5,0) → (6,0) → (6,1) → (5,1); initial index 0. fading crossing (6,3); two-light dark tile (3,1); switch (6,4); timed gate (6,2).

**Repair:** Clear tower passage at (1,2); M band, **1000 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R3 U5 L6 D2 R1 D3 R2`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 047 — Echo District

**Design brief:** Use a side step to let the echo pass.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,1), lantern 21.

**Houses:** A Lantern Row (6,1) = 240 pts; B East Watch (4,6) = 300 pts; C The Mill (0,5) = 360 pts.

```text
    01234567
0   .#.#....
1   ..D...A.
2   ..#.....
3   .#...#..
4   .##...f#
5   C#......
6   ..d.B...
7   ....##.#
```

**Hazards:** first patrol (3,5) → (4,5) → (4,6) → (3,6); initial index 0. fading crossing (6,4); two-light dark tile (2,6); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R4 D5 L6 U5 R2`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 048 — Echo District

**Design brief:** Fading crossing closes behind the echo.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,7), lantern 24.

**Houses:** A Lantern Row (7,5) = 240 pts; B East Watch (4,1) = 300 pts; C The Mill (0,4) = 360 pts.

```text
    01234567
0   #....#..
1   ....B..g
2   .#...#.f
3   ....#...
4   C..##..s
5   ..#..#.A
6   ....#...
7   ....D...
```

**Hazards:** first patrol (3,1) → (4,1) → (4,2) → (3,2); initial index 1. fading crossing (7,2); switch (7,4); timed gate (7,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `R3 U6 L7 D6 R4`. 26 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 049 — Echo District

**Design brief:** Optional lamp helps an extended detour.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,2), lantern 25.

**Houses:** A Lantern Row (7,7) = 240 pts; B East Watch (0,7) = 300 pts; C The Mill (1,1) = 360 pts.

```text
    01234567
0   .#.#....
1   .C......
2   ......#D
3   ......#.
4   d..####.
5   ......#.
6   ...#..#.
7   B...f..A
```

**Hazards:** first patrol (0,2) → (1,2) → (1,3) → (0,3); initial index 1. fading crossing (4,7); two-light dark tile (0,4); Echo Shadow active after first delivery.

**Repair:** Relight lamp at (0,4); S band, **450 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `D5 L7 U6 R7 D1`. 26 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 050 — Echo District

**Design brief:** Finale: three houses, echo loop, depot return.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,2), lantern 21.

**Houses:** A Lantern Row (3,1) = 240 pts; B East Watch (1,5) = 300 pts; C The Mill (5,6) = 360 pts.

```text
    01234567
0   .....#..
1   #fsA....
2   #g.#..D.
3   #......#
4   ..#..#..
5   #B#.....
6   .dR..C..
7   ....###.
```

**Hazards:** first patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 0. fading crossing (1,1); two-light dark tile (1,6); switch (2,1); timed gate (1,2).

**Repair:** Repair side bridge at (2,6); R band, **700 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U1 L5 D6 R2 U1 R3 U4`. 22 moves, 4 light left, 1100 points banked including the 200-point mastery bonus.

### 051 — Winter Canal

**Design brief:** Cross ice once, leave before it breaks.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,3), lantern 18.

**Houses:** A Lantern Row (5,6) = 270 pts; B East Watch (1,4) = 330 pts; C The Mill (3,1) = 390 pts.

```text
    01234567
0   #....###
1   #i.C...#
2   .....#..
3   #...#.D.
4   .B.#...#
5   ..#.#...
6   ...f.A..
7   .......#
```

**Hazards:** first patrol (1,6) → (2,6) → (2,7) → (1,7); initial index 1. fading crossing (3,6); thin ice (1,1); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `D3 L5 U5 R5 D2`. 20 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 052 — Winter Canal

**Design brief:** Compare ice shortcut with long land route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,2), lantern 23.

**Houses:** A Lantern Row (2,1) = 270 pts; B East Watch (0,6) = 330 pts; C The Mill (5,7) = 390 pts.

```text
    01234567
0   ##.#.#..
1   .sA.....
2   g.....D.
3   ...#...#
4   ...#.#..
5   .....#..
6   B.......
7   .d...C.#
```

**Hazards:** first patrol (1,6) → (2,6) → (2,7) → (1,7); initial index 1. fading crossing (0,2); two-light dark tile (1,7); switch (1,1); timed gate (0,2).

**Repair:** none on this board.

**Verified no-purchase full route:** `U1 L6 D6 R6 U5`. 24 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 053 — Winter Canal

**Design brief:** Stable crossing can replace risky ice.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,6), lantern 21.

**Houses:** A Lantern Row (1,6) = 270 pts; B East Watch (2,1) = 330 pts; C The Mill (6,2) = 390 pts.

```text
    01234567
0   ##......
1   ..Bd.i..
2   ......C#
3   .......#
4   .f#.#...
5   .R#.#...
6   .A...D..
7   ....#...
```

**Hazards:** first patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 0. fading crossing (1,4); two-light dark tile (3,1); thin ice (5,1); Echo Shadow active after first delivery.

**Repair:** Build canal bridge at (1,5); M band, **1125 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `L5 U2 R1 U3 R5 D5 L1`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 054 — Winter Canal

**Design brief:** Shadow reaches shore on the same turn.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,1), lantern 22.

**Houses:** A Lantern Row (1,1) = 270 pts; B East Watch (0,7) = 330 pts; C The Mill (6,7) = 390 pts.

```text
    01234567
0   ..#...#.
1   sA....D.
2   ...#.#..
3   g#...#..
4   ...##...
5   ....##..
6   .#......
7   B.....C.
```

**Hazards:** first patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 1. fading crossing (0,3); switch (0,1); timed gate (0,3).

**Repair:** none on this board.

**Verified no-purchase full route:** `L6 D6 R6 U6`. 24 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 055 — Winter Canal

**Design brief:** House order changes which shore you finish on.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,1), lantern 21.

**Houses:** A Lantern Row (7,1) = 270 pts; B East Watch (5,6) = 330 pts; C The Mill (1,5) = 390 pts.

```text
    01234567
0   ...#.#..
1   ...D...A
2   ..#.#...
3   ...#.#..
4   #......f
5   .C..#.#.
6   ..id.B..
7   #..##.##
```

**Hazards:** first patrol (2,5) → (3,5) → (3,6) → (2,6); initial index 0. fading crossing (7,4); two-light dark tile (3,6); thin ice (2,6); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R4 D5 L6 U5 R2`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 056 — Winter Canal

**Design brief:** Rubble adds two moves to the winter return.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,5), lantern 21.

**Houses:** A Lantern Row (6,1) = 270 pts; B East Watch (1,2) = 330 pts; C The Mill (2,6) = 390 pts.

```text
    01234567
0   .....#..
1   ..RgfsA.
2   .B#....#
3   .d.#...#
4   #...#...
5   #..#..D.
6   ..C.....
7   .#......
```

**Hazards:** first patrol (1,3) → (2,3) → (2,4) → (1,4); initial index 0. fading crossing (4,1); two-light dark tile (1,3); switch (5,1); timed gate (3,1).

**Repair:** Clear rubble at (2,1); S band, **525 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U4 L3 U1 L2 D6 R5 U1`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 057 — Winter Canal

**Design brief:** Echo trail follows the ice entry.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,4), lantern 20.

**Houses:** A Lantern Row (2,1) = 270 pts; B East Watch (7,3) = 330 pts; C The Mill (5,6) = 390 pts.

```text
    01234567
0   ##......
1   ..A..f..
2   #...#.#.
3   ...#.##B
4   .D..#.#.
5   ........
6   .....C.i
7   #...#...
```

**Hazards:** first patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 1. fading crossing (5,1); thin ice (7,6); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U3 R6 D5 L6 U2`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 058 — Winter Canal

**Design brief:** Switch gate gives a second way off the canal.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,1), lantern 23.

**Houses:** A Lantern Row (2,0) = 270 pts; B East Watch (0,5) = 330 pts; C The Mill (5,6) = 390 pts.

```text
    01234567
0   .sA....#
1   g##...D.
2   ..#.#...
3   ..#..#..
4   ........
5   B.#..#..
6   .d...C..
7   .#.##...
```

**Hazards:** first patrol (0,3) → (1,3) → (1,4) → (0,4); initial index 0. fading crossing (0,1); two-light dark tile (1,6); switch (1,0); timed gate (0,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `U1 L6 D6 R6 U5`. 24 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 059 — Winter Canal

**Design brief:** Route shortcut costs points but saves light.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,1), lantern 21.

**Houses:** A Lantern Row (6,3) = 270 pts; B East Watch (3,6) = 330 pts; C The Mill (1,3) = 390 pts.

```text
    01234567
0   ##......
1   ....D...
2   #.####..
3   .C#.#.A#
4   .R#.....
5   .i..##f.
6   ..dB...#
7   #.......
```

**Hazards:** first patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 0. fading crossing (6,5); two-light dark tile (2,6); thin ice (1,5); Echo Shadow active after first delivery.

**Repair:** Open shore gate at (1,4); R band, **800 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R2 D5 L5 U1 L1 U2 R1 U2 R3`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 060 — Winter Canal

**Design brief:** Finale: three houses split across two shores.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,1), lantern 20.

**Houses:** A Lantern Row (1,4) = 270 pts; B East Watch (5,6) = 330 pts; C The Mill (6,2) = 390 pts.

```text
    01234567
0   ........
1   ..D.....
2   #..#..C.
3   ..#....#
4   #A#.....
5   .s###..#
6   #fgR.B..
7   .......#
```

**Hazards:** first patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. fading crossing (1,6); switch (1,5); timed gate (2,6).

**Repair:** Build side bridge at (3,6); M band, **1125 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `L1 D5 R1 D1 R2 U1 R2 U5 L4`. 22 moves, 4 light left, 1215 points banked including the 225-point mastery bonus.

### 061 — Shadow Market

**Design brief:** Second shadow introduced on a separate lane.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,7), lantern 24.

**Houses:** A Lantern Row (0,6) = 300 pts; B East Watch (2,1) = 360 pts; C The Mill (7,3) = 420 pts.

```text
    01234567
0   ........
1   ..B..d.i
2   ........
3   f.##...C
4   ...###..
5   ....##..
6   A####...
7   ....D...
```

**Hazards:** first patrol (6,1) → (7,1) → (7,2) → (6,2); initial index 0. Second patrol (3,1) → (4,1) → (4,2) → (3,2); initial index 1. fading crossing (0,3); two-light dark tile (5,1); thin ice (7,1); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L4 U6 R7 D6 L3`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 062 — Shadow Market

**Design brief:** Cross between patrol lanes safely.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (3,0), lantern 24.

**Houses:** A Lantern Row (0,2) = 300 pts; B East Watch (3,6) = 360 pts; C The Mill (7,3) = 420 pts.

```text
    01234567
0   ...D....
1   .##..#..
2   A#......
3   s#..#.#C
4   ..#.#...
5   f.......
6   g..B..d.
7   .......#
```

**Hazards:** first patrol (4,6) → (5,6) → (5,7) → (4,7); initial index 1. Second patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 1. fading crossing (0,5); two-light dark tile (6,6); switch (0,3); timed gate (0,6); second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L3 D6 R7 U6 L4`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 063 — Shadow Market

**Design brief:** Two houses are close but their exits differ.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,7), lantern 19.

**Houses:** A Lantern Row (1,6) = 300 pts; B East Watch (3,1) = 360 pts; C The Mill (6,3) = 420 pts.

```text
    01234567
0   ..#...##
1   #..B..i.
2   ...#...#
3   .f#...C.
4   ..#.....
5   ...#.#..
6   .A.....#
7   #...D..#
```

**Hazards:** first patrol (1,1) → (2,1) → (2,2) → (1,2); initial index 0. Second patrol (4,1) → (5,1) → (5,2) → (4,2); initial index 1. fading crossing (1,3); thin ice (6,1); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L3 U6 R5 D6 L2`. 22 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 064 — Shadow Market

**Design brief:** Narrow shortcut bypasses one patrol lane.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,6), lantern 20.

**Houses:** A Lantern Row (6,6) = 300 pts; B East Watch (5,1) = 360 pts; C The Mill (1,2) = 420 pts.

```text
    01234567
0   .#.#....
1   ....dB..
2   .C.#.#R.
3   #.....g.
4   ......f.
5   #..##.s.
6   #.D...A#
7   ..#....#
```

**Hazards:** first patrol (5,0) → (6,0) → (6,1) → (5,1); initial index 0. fading crossing (6,4); two-light dark tile (4,1); switch (6,5); timed gate (6,3).

**Repair:** Open gate at (6,2); R band, **900 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R4 U3 R1 U2 L6 D5 R1`. 22 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 065 — Shadow Market

**Design brief:** Echo and second patrol activate at different houses.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,4), lantern 24.

**Houses:** A Lantern Row (5,7) = 300 pts; B East Watch (1,4) = 360 pts; C The Mill (4,0) = 420 pts.

```text
    01234567
0   #.i.C...
1   .d#.....
2   .....#..
3   ..##..#.
4   #B..#.#D
5   ...#.#..
6   ...#....
7   ..f..A..
```

**Hazards:** first patrol (1,5) → (2,5) → (2,6) → (1,6); initial index 0. Second patrol (1,4) → (2,4) → (2,5) → (1,5); initial index 0. fading crossing (2,7); two-light dark tile (1,1); thin ice (2,0); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `D3 L6 U7 R6 D4`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 066 — Shadow Market

**Design brief:** Dark streetlamp consumes precious light.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,5), lantern 24.

**Houses:** A Lantern Row (3,7) = 300 pts; B East Watch (7,4) = 360 pts; C The Mill (3,1) = 420 pts.

```text
    01234567
0   #.......
1   ...C...d
2   ...#....
3   .#..#...
4   ..##..#B
5   D.#.....
6   .##..##.
7   ...As.fg
```

**Hazards:** first patrol (6,1) → (7,1) → (7,2) → (6,2); initial index 0. Second patrol (4,1) → (5,1) → (5,2) → (4,2); initial index 0. fading crossing (6,7); two-light dark tile (7,1); switch (4,7); timed gate (7,7); second patrol active after first delivery.

**Repair:** Relight lamp at (7,1); S band, **600 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `D2 R7 U6 L7 D4`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 067 — Shadow Market

**Design brief:** Decide when to bank rather than chase house three.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,2), lantern 24.

**Houses:** A Lantern Row (3,0) = 300 pts; B East Watch (6,4) = 360 pts; C The Mill (2,7) = 420 pts.

```text
    01234567
0   ...A..f.
1   ..##...#
2   D....#.#
3   .......#
4   .#....B#
5   ..#.....
6   ...###.#
7   ..C.i.d#
```

**Hazards:** first patrol (5,3) → (6,3) → (6,4) → (5,4); initial index 0. fading crossing (6,0); two-light dark tile (6,7); thin ice (4,7); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U2 R6 D7 L6 U5`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 068 — Shadow Market

**Design brief:** Shadowed arch hides a side route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,2), lantern 20.

**Houses:** A Lantern Row (3,1) = 300 pts; B East Watch (1,5) = 360 pts; C The Mill (5,6) = 420 pts.

```text
    01234567
0   ...##.#.
1   .fsA....
2   #g#...D.
3   ..#.#..#
4   ........
5   .B#.....
6   .dR..C..
7   ......#.
```

**Hazards:** first patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 0. Second patrol (0,3) → (1,3) → (1,4) → (0,4); initial index 0. fading crossing (1,1); two-light dark tile (1,6); switch (2,1); timed gate (1,2); second patrol active after first delivery.

**Repair:** Repair side arch at (2,6); R band, **900 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U1 L5 D6 R2 U1 R3 U4`. 22 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 069 — Shadow Market

**Design brief:** Switch timing intersects both patrol lanes.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,0), lantern 23.

**Houses:** A Lantern Row (7,3) = 300 pts; B East Watch (3,6) = 360 pts; C The Mill (0,2) = 420 pts.

```text
    01234567
0   .....D..
1   ....#...
2   C..#....
3   ..###.#A
4   i##.....
5   ..##....
6   ...B...f
7   .....#..
```

**Hazards:** first patrol (0,6) → (1,6) → (1,7) → (0,7); initial index 1. Second patrol (0,5) → (1,5) → (1,6) → (0,6); initial index 0. fading crossing (7,6); thin ice (0,4); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R2 D6 L7 U6 R5`. 26 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 070 — Shadow Market

**Design brief:** Finale: three houses, two patrols, one return.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,6), lantern 20.

**Houses:** A Lantern Row (6,4) = 300 pts; B East Watch (3,1) = 360 pts; C The Mill (1,4) = 420 pts.

```text
    01234567
0   ...#...#
1   ..dB.Rg#
2   ...###f.
3   #.#..#s.
4   .C....A.
5   ...##...
6   #...D..#
7   ..##..#.
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. fading crossing (6,2); two-light dark tile (2,1); switch (6,3); timed gate (6,1).

**Repair:** Clear tower passage at (5,1); M band, **1250 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R2 U6 L2 D1 L3 D5 R3`. 22 moves, 3 light left, 1330 points banked including the 250-point mastery bonus.

### 071 — Old City

**Design brief:** Two looping streets, one closer to the depot.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,5), lantern 22.

**Houses:** A Lantern Row (1,1) = 330 pts; B East Watch (6,3) = 390 pts; C The Mill (4,7) = 450 pts.

```text
    01234567
0   #####...
1   .A..f...
2   ..#....#
3   .##..#B.
4   ........
5   D.....d.
6   .###..i#
7   ....C...
```

**Hazards:** first patrol (5,0) → (6,0) → (6,1) → (5,1); initial index 0. Second patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 0. fading crossing (4,1); two-light dark tile (6,5); thin ice (6,6); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U4 R6 D6 L6 U2`. 24 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 072 — Old City

**Design brief:** Fading bridge cuts the inner loop.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,5), lantern 25.

**Houses:** A Lantern Row (7,0) = 330 pts; B East Watch (0,1) = 390 pts; C The Mill (1,7) = 450 pts.

```text
    01234567
0   ..gf.s.A
1   B..#....
2   ...#....
3   ..#...#.
4   ..#...#.
5   .##.#..D
6   .#.#....
7   .C......
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 1. Second patrol (0,0) → (1,0) → (1,1) → (0,1); initial index 0. fading crossing (3,0); switch (5,0); timed gate (2,0); second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U5 L7 D7 R7 U2`. 28 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 073 — Old City

**Design brief:** Broken arch opens a third return route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,1), lantern 20.

**Houses:** A Lantern Row (6,3) = 330 pts; B East Watch (3,6) = 390 pts; C The Mill (1,3) = 450 pts.

```text
    01234567
0   ........
1   ....D...
2   ...###..
3   #C##.#A#
4   ..#..#..
5   .i..#.f.
6   #.dBR...
7   #.....#.
```

**Hazards:** first patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 0. fading crossing (6,5); two-light dark tile (2,6); thin ice (1,5); Echo Shadow active after first delivery.

**Repair:** Repair arch at (4,6); R band, **1000 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R2 D5 L1 D1 L2 U1 L2 U5 R3`. 22 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 074 — Old City

**Design brief:** Echo repeats a tempting short loop.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,7), lantern 24.

**Houses:** A Lantern Row (7,5) = 330 pts; B East Watch (4,1) = 390 pts; C The Mill (0,4) = 450 pts.

```text
    01234567
0   .#.####.
1   .d..B..g
2   ....#..f
3   ...##...
4   C.#....s
5   ..##..#A
6   .....#..
7   ....D...
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. Second patrol (5,1) → (6,1) → (6,2) → (5,2); initial index 1. fading crossing (7,2); two-light dark tile (1,1); switch (7,4); timed gate (7,1); second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R3 U6 L7 D6 R4`. 26 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 075 — Old City

**Design brief:** Time a switch while carrying two deliveries.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,1), lantern 25.

**Houses:** A Lantern Row (7,6) = 330 pts; B East Watch (0,7) = 390 pts; C The Mill (0,0) = 450 pts.

```text
    01234567
0   C.......
1   .###...D
2   i##.#.#.
3   ..##.#..
4   ......#.
5   ...##...
6   .....#.A
7   B...f...
```

**Hazards:** first patrol (1,6) → (2,6) → (2,7) → (1,7); initial index 1. Second patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 0. fading crossing (4,7); thin ice (0,2); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `D6 L7 U7 R7 D1`. 28 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 076 — Old City

**Design brief:** Flooded central tile splits the board.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,6), lantern 20.

**Houses:** A Lantern Row (6,6) = 330 pts; B East Watch (5,1) = 390 pts; C The Mill (1,2) = 450 pts.

```text
    01234567
0   .#......
1   ...RdB..
2   #C.#....
3   ......g#
4   #.#...f.
5   .....#s#
6   #.D...A.
7   #.#.#...
```

**Hazards:** first patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. fading crossing (6,4); two-light dark tile (4,1); switch (6,5); timed gate (6,3).

**Repair:** Drain road at (3,1); R band, **1000 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R4 U5 L2 U1 L2 D1 L1 D5 R1`. 22 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 077 — Old City

**Design brief:** Dark lamp penalizes the fastest geometric route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,2), lantern 24.

**Houses:** A Lantern Row (7,7) = 330 pts; B East Watch (1,6) = 390 pts; C The Mill (2,0) = 450 pts.

```text
    01234567
0   #.C.....
1   #i......
2   ..#.##.D
3   .d.#..#.
4   #..#....
5   #.#.#.#.
6   .B......
7   ....f..A
```

**Hazards:** first patrol (1,6) → (2,6) → (2,7) → (1,7); initial index 0. Second patrol (0,2) → (1,2) → (1,3) → (0,3); initial index 1. fading crossing (4,7); two-light dark tile (1,3); thin ice (1,1); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** Relight lamp at (1,3); S band, **675 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `D5 L6 U7 R6 D2`. 26 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 078 — Old City

**Design brief:** Three-house route has several safe orders.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,1), lantern 21.

**Houses:** A Lantern Row (0,2) = 330 pts; B East Watch (3,6) = 390 pts; C The Mill (7,4) = 450 pts.

```text
    01234567
0   #...##..
1   ....D...
2   A#...#..
3   s....##.
4   ......#C
5   g.......
6   ...B....
7   ##.###..
```

**Hazards:** first patrol (4,5) → (5,5) → (5,6) → (4,6); initial index 0. Second patrol (1,5) → (2,5) → (2,6) → (1,6); initial index 1. fading crossing (0,5); switch (0,3); timed gate (0,5); second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L4 D5 R7 U5 L3`. 24 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 079 — Old City

**Design brief:** Collapsed tunnel creates a mastery shortcut.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,1), lantern 20.

**Houses:** A Lantern Row (6,1) = 330 pts; B East Watch (5,6) = 390 pts; C The Mill (1,5) = 450 pts.

```text
    01234567
0   #....#.#
1   ..D...A.
2   #.#..#..
3   #..#.#f.
4   #.#.....
5   .C..##R.
6   ..i.dB..
7   ..#.#...
```

**Hazards:** first patrol (6,6) → (7,6) → (7,7) → (6,7); initial index 0. fading crossing (6,3); two-light dark tile (4,6); thin ice (2,6); Echo Shadow active after first delivery.

**Repair:** Reopen tunnel at (6,5); M band, **1375 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `R4 D3 R1 D2 L6 U5 R1`. 22 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 080 — Old City

**Design brief:** Finale: city loops, echo, crossing, depot.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,2), lantern 20.

**Houses:** A Lantern Row (1,6) = 330 pts; B East Watch (6,5) = 390 pts; C The Mill (5,1) = 450 pts.

```text
    01234567
0   #.......
1   .....C..
2   .D.#....
3   ......R.
4   ..#..#d.
5   ....##B.
6   .Asfg...
7   .####...
```

**Hazards:** first patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. Second patrol (5,1) → (6,1) → (6,2) → (5,2); initial index 0. fading crossing (3,6); two-light dark tile (6,4); switch (2,6); timed gate (4,6); second patrol active after first delivery.

**Repair:** Clear central rubble at (6,3); R band, **1000 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `D4 R5 U2 R1 U2 L1 U1 L5 D1`. 22 moves, 3 light left, 1445 points banked including the 275-point mastery bonus.

### 081 — Blackout

**Design brief:** Start with less light; deliver nearby first.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,7), lantern 25.

**Houses:** A Lantern Row (0,4) = 360 pts; B East Watch (4,0) = 420 pts; C The Mill (7,4) = 480 pts.

```text
    01234567
0   f...B..d
1   ........
2   ..##..#i
3   ....#...
4   A.##..#C
5   ...#....
6   .##..##.
7   ..D.....
```

**Hazards:** first patrol (6,0) → (7,0) → (7,1) → (6,1); initial index 0. Second patrol (1,0) → (2,0) → (2,1) → (1,1); initial index 0. fading crossing (0,0); two-light dark tile (7,0); thin ice (7,2); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L2 U7 R7 D7 L5`. 28 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 082 — Blackout

**Design brief:** Refill timing matters at house two.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,1), lantern 21.

**Houses:** A Lantern Row (3,0) = 360 pts; B East Watch (1,5) = 420 pts; C The Mill (6,6) = 480 pts.

```text
    01234567
0   ..sA....
1   .g...#.D
2   ........
3   ..#.#.#.
4   ..#.#...
5   .B#..#..
6   ..d...C.
7   ###..#..
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. fading crossing (1,1); two-light dark tile (2,6); switch (2,0); timed gate (1,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `U1 L6 D6 R6 U5`. 24 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 083 — Blackout

**Design brief:** Short but shadow-timed route versus safe long route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,0), lantern 21.

**Houses:** A Lantern Row (6,0) = 360 pts; B East Watch (5,6) = 420 pts; C The Mill (0,5) = 480 pts.

```text
    01234567
0   .D....A#
1   ...##..#
2   ..###...
3   ......f.
4   .#.###..
5   C..#....
6   ..id.B..
7   ...#...#
```

**Hazards:** first patrol (5,5) → (6,5) → (6,6) → (5,6); initial index 1. Second patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 0. fading crossing (6,3); two-light dark tile (3,6); thin ice (2,6); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R5 D6 L6 U6 R1`. 24 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 084 — Blackout

**Design brief:** Streetlamp fixes a 2-light tile.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,2), lantern 23.

**Houses:** A Lantern Row (1,7) = 360 pts; B East Watch (7,6) = 420 pts; C The Mill (6,0) = 480 pts.

```text
    01234567
0   ......C.
1   ...#.#..
2   .D..#...
3   ...#...d
4   #.#.....
5   ..#..#..
6   #..##..B
7   #As.fg..
```

**Hazards:** first patrol (6,2) → (7,2) → (7,3) → (6,3); initial index 1. Second patrol (6,5) → (7,5) → (7,6) → (6,6); initial index 0. fading crossing (4,7); two-light dark tile (7,3); switch (2,7); timed gate (5,7); second patrol active after first delivery.

**Repair:** Relight lamp at (7,3); S band, **750 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `D5 R6 U7 L6 D2`. 26 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 085 — Blackout

**Design brief:** Ice crossing and low lantern cap.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (0,4), lantern 25.

**Houses:** A Lantern Row (1,0) = 360 pts; B East Watch (7,2) = 420 pts; C The Mill (5,7) = 480 pts.

```text
    01234567
0   .A...f..
1   .##.#...
2   .#.....B
3   .....#..
4   D#.#....
5   .....#.d
6   ..####..
7   .....C.i
```

**Hazards:** first patrol (6,4) → (7,4) → (7,5) → (6,5); initial index 0. fading crossing (5,0); two-light dark tile (7,5); thin ice (7,7); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U4 R7 D7 L7 U3`. 28 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 086 — Blackout

**Design brief:** Broken bridge opens a more efficient loop.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,5), lantern 19.

**Houses:** A Lantern Row (6,1) = 360 pts; B East Watch (1,2) = 420 pts; C The Mill (2,6) = 480 pts.

```text
    01234567
0   ....#...
1   #.RgfsA.
2   .B.#...#
3   .d..#...
4   .....#..
5   ..#.#.D.
6   ..C.....
7   ####..#.
```

**Hazards:** first patrol (0,2) → (1,2) → (1,3) → (0,3); initial index 0. Second patrol (1,2) → (2,2) → (2,3) → (1,3); initial index 1. fading crossing (4,1); two-light dark tile (1,3); switch (5,1); timed gate (3,1); second patrol active after first delivery.

**Repair:** Repair bridge at (2,1); R band, **1100 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U4 L3 U1 L2 D6 R5 U1`. 22 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 087 — Blackout

**Design brief:** Echo trail makes an efficient route risky.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,6), lantern 20.

**Houses:** A Lantern Row (1,1) = 360 pts; B East Watch (6,1) = 420 pts; C The Mill (6,7) = 480 pts.

```text
    01234567
0   ...f....
1   .A.#.#B.
2   #..#...#
3   ...#....
4   ...#.#i#
5   ....#..#
6   #D#.....
7   #.....C.
```

**Hazards:** first patrol (6,0) → (7,0) → (7,1) → (6,1); initial index 1. Second patrol (5,2) → (6,2) → (6,3) → (5,3); initial index 0. fading crossing (3,0); thin ice (6,4); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U6 R5 D7 L5 U1`. 24 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 088 — Blackout

**Design brief:** Bank two houses, then replay for mastery.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,2), lantern 21.

**Houses:** A Lantern Row (3,1) = 360 pts; B East Watch (0,5) = 420 pts; C The Mill (5,6) = 480 pts.

```text
    01234567
0   .#..#..#
1   g.sA....
2   .###.#.D
3   ........
4   .....#..
5   B.#...#.
6   .d...C..
7   .......#
```

**Hazards:** first patrol (2,6) → (3,6) → (3,7) → (2,7); initial index 0. fading crossing (0,1); two-light dark tile (1,6); switch (2,1); timed gate (0,1).

**Repair:** none on this board.

**Verified no-purchase full route:** `U1 L7 D5 R7 U4`. 24 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 089 — Blackout

**Design brief:** Broken beacon lowers capacity on this map.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,4), lantern 21.

**Houses:** A Lantern Row (2,0) = 360 pts; B East Watch (6,3) = 420 pts; C The Mill (4,7) = 480 pts.

```text
    01234567
0   ..A..f..
1   ........
2   .......#
3   ...##.B#
4   #D.##..#
5   #...##d.
6   .....#i#
7   ....C...
```

**Hazards:** first patrol (5,2) → (6,2) → (6,3) → (5,3); initial index 0. Second patrol (5,0) → (6,0) → (6,1) → (5,1); initial index 0. fading crossing (5,0); two-light dark tile (6,5); thin ice (6,6); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** Restore beacon at (1,4); M band, **1500 points**; start capacity rises by 3 on this level.

**Verified no-purchase full route:** `U4 R5 D7 L5 U3`. 24 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 090 — Blackout

**Design brief:** Finale: three refills needed to return.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,5), lantern 18.

**Houses:** A Lantern Row (6,1) = 360 pts; B East Watch (1,2) = 420 pts; C The Mill (2,6) = 480 pts.

```text
    01234567
0   #..###..
1   ...gfsA.
2   .B.#.#.#
3   .R#.....
4   .......#
5   #....#D#
6   ..C.....
7   ...##...
```

**Hazards:** first patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. Second patrol (3,3) → (4,3) → (4,4) → (3,4); initial index 0. fading crossing (4,1); switch (5,1); timed gate (3,1); second patrol active after first delivery.

**Repair:** Open old tunnel at (1,3); M band, **1500 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U4 L5 D1 L1 D2 R1 D2 R5 U1`. 22 moves, 2 light left, 1560 points banked including the 300-point mastery bonus.

### 091 — Last Light

**Design brief:** Choose a delivery order that preserves light.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,0), lantern 23.

**Houses:** A Lantern Row (6,1) = 390 pts; B East Watch (5,7) = 450 pts; C The Mill (0,5) = 510 pts.

```text
    01234567
0   ..D....#
1   ..#.##A.
2   .###.#..
3   ..#.....
4   .#.#..f.
5   C.#.#...
6   ..#.....
7   i.d..B.#
```

**Hazards:** first patrol (5,6) → (6,6) → (6,7) → (5,7); initial index 1. fading crossing (6,4); two-light dark tile (2,7); thin ice (0,7); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R4 D7 L6 U7 R2`. 26 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 092 — Last Light

**Design brief:** Two shadows leave one safe timing window.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,6), lantern 21.

**Houses:** A Lantern Row (7,1) = 390 pts; B East Watch (0,1) = 450 pts; C The Mill (1,6) = 510 pts.

```text
    01234567
0   .....##.
1   B...g.sA
2   ......#.
3   d.....#.
4   ...##...
5   ..##..#.
6   .C.....D
7   #....#.#
```

**Hazards:** first patrol (2,1) → (3,1) → (3,2) → (2,2); initial index 0. Second patrol (3,0) → (4,0) → (4,1) → (3,1); initial index 0. fading crossing (4,1); two-light dark tile (0,3); switch (6,1); timed gate (4,1); second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `U5 L7 D5 R7`. 24 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 093 — Last Light

**Design brief:** Echo crosses the apparent shortcut.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (2,7), lantern 18.

**Houses:** A Lantern Row (1,4) = 390 pts; B East Watch (5,1) = 450 pts; C The Mill (6,5) = 510 pts.

```text
    01234567
0   .#....##
1   .f...B..
2   #.#.#...
3   ..#...i#
4   .A.#....
5   ....#.C#
6   ..##....
7   ..D....#
```

**Hazards:** first patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 0. Second patrol (4,0) → (5,0) → (5,1) → (4,1); initial index 0. fading crossing (1,1); thin ice (6,3); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L1 U6 R5 D6 L4`. 22 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 094 — Last Light

**Design brief:** Bridge timer closes the outward route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (6,6), lantern 19.

**Houses:** A Lantern Row (6,2) = 390 pts; B East Watch (1,1) = 450 pts; C The Mill (1,6) = 510 pts.

```text
    01234567
0   ........
1   .BR.gfs.
2   .d..#.A.
3   ...#...#
4   ..#.##.#
5   #.#.##..
6   .C....D.
7   ......#.
```

**Hazards:** first patrol (0,1) → (1,1) → (1,2) → (0,2); initial index 0. fading crossing (5,1); two-light dark tile (1,2); switch (6,1); timed gate (4,1).

**Repair:** Repair side bridge at (2,1); R band, **1200 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `U5 L3 U1 L2 D6 R5`. 22 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 095 — Last Light

**Design brief:** Switch opens an exit but costs a detour.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,0), lantern 23.

**Houses:** A Lantern Row (6,3) = 390 pts; B East Watch (3,7) = 450 pts; C The Mill (0,3) = 510 pts.

```text
    01234567
0   ....D...
1   .....#.#
2   ....#..#
3   C.#.##A.
4   ..#.#...
5   i.##.#..
6   ....#.f#
7   d..B....
```

**Hazards:** first patrol (1,6) → (2,6) → (2,7) → (1,7); initial index 0. Second patrol (0,5) → (1,5) → (1,6) → (0,6); initial index 1. fading crossing (6,6); two-light dark tile (0,7); thin ice (0,5); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `R2 D7 L6 U7 R4`. 26 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 096 — Last Light

**Design brief:** Dark lamp competes with a patrol detour.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,0), lantern 25.

**Houses:** A Lantern Row (0,0) = 390 pts; B East Watch (1,7) = 450 pts; C The Mill (7,6) = 510 pts.

```text
    01234567
0   A....D..
1   ..#..#..
2   s...##..
3   ....#.#.
4   f#..#...
5   g.##....
6   .##....C
7   .B..d...
```

**Hazards:** first patrol (3,6) → (4,6) → (4,7) → (3,7); initial index 0. Second patrol (4,6) → (5,6) → (5,7) → (4,7); initial index 1. fading crossing (0,4); two-light dark tile (4,7); switch (0,2); timed gate (0,5); second patrol active after first delivery.

**Repair:** Relight lamp at (4,7); S band, **825 points**; dark tile costs 1 light after repair.

**Verified no-purchase full route:** `L5 D7 R7 U7 L2`. 28 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 097 — Last Light

**Design brief:** Flood and ice create two changing crossings.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (7,4), lantern 23.

**Houses:** A Lantern Row (4,6) = 390 pts; B East Watch (0,3) = 450 pts; C The Mill (4,0) = 510 pts.

```text
    01234567
0   d.i.C...
1   .#..#.#.
2   ...#....
3   B#..#...
4   .#..#..D
5   ......#.
6   .f..A...
7   .#..#.##
```

**Hazards:** first patrol (0,5) → (1,5) → (1,6) → (0,6); initial index 0. fading crossing (1,6); two-light dark tile (0,0); thin ice (2,0); Echo Shadow active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `D2 L7 U6 R7 D4`. 26 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 098 — Last Light

**Design brief:** Tunnel repair supports a shorter mastery route.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (1,1), lantern 19.

**Houses:** A Lantern Row (1,5) = 390 pts; B East Watch (6,6) = 450 pts; C The Mill (6,1) = 510 pts.

```text
    01234567
0   ##...###
1   #D....C.
2   ....#.R.
3   .....#..
4   #.......
5   #A..#.d.
6   .sfg..B.
7   .....##.
```

**Hazards:** first patrol (5,5) → (6,5) → (6,6) → (5,6); initial index 1. Second patrol (6,3) → (7,3) → (7,4) → (6,4); initial index 0. fading crossing (2,6); two-light dark tile (6,5); switch (1,6); timed gate (3,6); second patrol active after first delivery.

**Repair:** Reopen tunnel at (6,2); M band, **1625 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `D5 R5 U3 R1 U2 L6`. 22 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 099 — Last Light

**Design brief:** Practice board: all mechanics, generous retry.

**Goal:** bank 2 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (5,7), lantern 24.

**Houses:** A Lantern Row (0,7) = 390 pts; B East Watch (1,0) = 450 pts; C The Mill (7,1) = 510 pts.

```text
    01234567
0   .B....i.
1   .......C
2   ..###...
3   f#.#....
4   .###.##.
5   ..##....
6   .#.#..#.
7   A....D..
```

**Hazards:** first patrol (2,0) → (3,0) → (3,1) → (2,1); initial index 0. Second patrol (3,0) → (4,0) → (4,1) → (3,1); initial index 0. fading crossing (0,3); thin ice (6,0); Echo Shadow active after first delivery; second patrol active after first delivery.

**Repair:** none on this board.

**Verified no-purchase full route:** `L5 U7 R7 D7 L2`. 28 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

### 100 — Last Light

**Design brief:** Finale: light all three houses, evade both shadows and echo, return to depot; town fully lights up.

**Goal:** bank 3 of 3 houses to clear; bank all 3 for mastery. **Start:** depot (4,1), lantern 19.

**Houses:** A Lantern Row (1,2) = 390 pts; B East Watch (3,6) = 450 pts; C The Mill (6,4) = 510 pts.

```text
    01234567
0   ...#....
1   #...D...
2   .A.#....
3   #s.#....
4   #f.#.#C.
5   #g.#.#..
6   #..BdR.#
7   .#......
```

**Hazards:** first patrol (3,6) → (4,6) → (4,7) → (3,7); initial index 0. fading crossing (1,4); two-light dark tile (4,6); switch (1,3); timed gate (1,5).

**Repair:** Restore final bridge at (5,6); M band, **1625 points**; opens the R tile; verified 2-move static all-house shortcut.

**Verified no-purchase full route:** `L3 D5 R3 D1 R2 U6 L2`. 22 moves, 2 light left, 1675 points banked including the 325-point mastery bonus.

## Notes for the design review chat

- Treat the coordinates, prices, and timing above as the **current playable baseline**. Preserve the clear, immediate tap interaction and visible DONE status when reviewing art or tutorials.
- Level 1 currently shows all three houses immediately, although its brief says to reveal the later houses after the first return. Treat that reveal as an unimplemented tutorial detail.
- The generator varies rectangular route geometry and blocked cells. Many levels still share an outer-loop structure; review whether chapters feel distinct enough in play. The full-route proof does not prove that an exact two-house return is feasible or interesting on every ordinary level.
- Flood, rubble, crates, tunnel, tower, and bridge repair names currently share a blocked-tile implementation. Their final art and any distinct rules still need design decisions. Buying a road repair does demonstrably shorten the static all-house route by two moves.
- The tested full routes prove mechanical solvability, not a finished difficulty curve. Validate intended route choices, reward pacing, repair usefulness against the moving shadows, first-time comprehension, and real-phone tap targets with people before calling these production-ready.
- Do not copy the old route-drawing/Go-button rules into this campaign. The selected interaction is direct tap-to-move with every currently safe adjacent option highlighted.
