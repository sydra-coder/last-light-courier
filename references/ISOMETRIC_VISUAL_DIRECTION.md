# Last Light Courier — Isometric Visual Direction

## Decision

Use **Sample 2: Isometric Village** from `THREE_MOVEMENT_SAMPLES.html` as the default visual reference. Players can also select **Storybook Overhead** or **Night Pursuit** from the main menu or while playing. The choice changes the board presentation only and is saved on the device.

## Keep the established game rules

Retain the current tap-to-move gameplay, legal move highlighting, shadow behavior and collision rules, lights, points, banking, obstacles, tutorials, and level layouts. The sample's echo-shadow behavior is a demonstration inside the comparison page; it is **not** a requested rule change. Do not copy its simplified 5 × 5 map or movement logic into the campaign.

The Night Pursuit sample's chasing shadow is also a demonstration. The campaign uses its existing patrol and Echo Shadow rules in all three views. Switching views during a run keeps the courier's tile, shadow phase, light, points, and completed houses.

## Visual treatment

- Show each logical tile as a raised diamond, so the route reads as a small isometric village.
- Keep walkable tiles, houses, and each obstacle type visually distinct at phone size. Use a consistent top-left light source, visible side faces, and soft ground shadows to give the board depth.
- Place the courier and shadow on the same tile centers as the current game. Draw them above the tile art and sort their visual depth by screen position so they do not appear to pass through buildings.
- Animate a courier move as a clear journey from one tile center to the next, with a brief walking cycle and a steady lantern glow. The character should rest between moves, without constant bobbing.
- Animate the shadow's move along the path dictated by the **existing** shadow rules. A violet trail or soft edge can make that move legible, but must not reveal future positions or safe moves that the rules currently hide.
- Show delivery through warm windows, doorstep light, and a persistent completed-house marker. Keep the existing delivery and scoring behavior.
- Give crates, rubble, broken bridges, and gates recognizable silhouettes. When an obstacle is opened or repaired, animate its visual change while preserving the existing cost and unlock rules.
- Preserve the current safe-move and unavailable-move feedback. Adapt their outlines to the diamond tiles without changing which tiles are selectable.

## Reference and scope

Open `THREE_MOVEMENT_SAMPLES.html` to compare the three visual directions. The comparison page is a concept preview; the full game's board size, content, user interface, and behavior remain governed by the current campaign implementation and design documents.

This is a design handoff. No gameplay or shadow logic change is authorized by this decision.
