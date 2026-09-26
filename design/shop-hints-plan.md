# Last Light Courier - Shop, items, hints and later-map redesign

Status: design plan for review. These systems are not implemented in the current HTML or APK. This plan supersedes the earlier requirement that every level must be completable without repair. Existing layouts and saved progress remain unchanged until implementation.

## 1. Map design

Later levels need more connected open ground, multiple loops and alternative house orders. A player should face route choices rather than follow one corridor through dense gray tiles. Prototype with 20-35% blocked ground; use this as a starting range, not a difficulty guarantee. Preserve two patrols plus Echo once introduced.

Give each trial map at least three meaningful junctions. Distribute houses across districts. Test different delivery orders against lantern use, gate timing and patrol positions. Keep clear obstacle types and visible rules. Complexity should come from choosing and timing routes, not from hiding controls or merely increasing distance.

## 2. Two categories of level

| Category | Rule | Review information |
| --- | --- | --- |
| Standard | At least one verified solution needs no items or purchases | Minimum moves without terrain change, and best route after an upgrade |
| Repair required | A damaged crossing separates mandatory objectives; no legal completion exists before it is repaired | Show "Repair required" instead of a numerical no-repair minimum |

Trial candidates for repair-required levels: 30, 60, 90, 120, 150, 180 and 200. These are proposed assignments, not changes already made. Introduce the repair lesson before the first required level. Do not turn every late map into an item gate.

A required damaged bridge or gate is distinct from ordinary gray rubble. Tunnel boring removes rubble; it cannot rebuild a missing bridge or replace a required gate repair. This makes "repair required" a real rule rather than a label players can bypass by drilling a nearby wall.

Give a level-bound free repair voucher before entering every mandatory-repair level. Reserve that voucher for its required obstacle, so spending other inventory cannot strand the player. A player can always reach the required obstacle using free movement. Using the voucher is still a deliberate map action: approach the right place, choose the crossing and time the route after opening it.

All purchased/opened terrain stays changed for that level across retries. Losing or restarting never charges the same repair or tunnel a second time. The reviewer should check both original and modified layouts.

## 3. Gems are the only purchase currency

All shop purchases and direct paid repairs use gems. Points become performance score only; they cannot buy repairs. Do not convert the old large point wallet directly into gems, because that would preserve the overfunding problem.

Initial balancing proposal: 120 starter gems; 10 gems for the first completion of a unique level; up to 5 additional gems for performance. Repeat runs do not repeatedly pay the same reward. This first version uses earnable in-game gems. Real-money gem packs would be a separate design and store-integration decision.

Existing purchased permanent repairs should be honored. Hint records, gem balance, item inventory and milestone claims must persist locally with a one-time migration. Existing completed levels must not grant duplicate rewards on reload.

## 4. Proposed shop catalogue

| Item | Trial price | What it does | Inventory limit |
| --- | --- | --- | --- |
| Hint | 30 gems | Shows one route demonstration for the current state | 5 |
| Repair voucher | 50 gems | Pays for one marked repair; cannot remove an arbitrary wall | 5 general vouchers |
| Tunnel boring token | 40 gems | Removes one adjacent ordinary gray rubble tile permanently on that level | 5 |

These prices are initial tuning values, not implemented prices. Direct repair prices can rise by chapter, but must be displayed in gems before spending. The player can choose a matching free voucher instead of gems. Level-bound required vouchers are separate from the general voucher inventory cap.

Only ordinary rubble can be drilled. Houses, depot, patrol routes, required bridges/gates, switch tiles and other special terrain retain their rules. Selecting an unsupported tile or canceling costs nothing. Drilling cannot remove a shadow. Show the selected tile and token/gem deduction clearly.

Item selection and explanation screens pause the action. Applying a terrain upgrade costs its item or gems, but does not secretly spend a movement turn or lantern light. Resume with the current shadow phase and recomputed legal moves. Terrain changes are permanent per level, not global changes to other maps.

## 5. Free items and collection

Start with one general repair voucher and one tunnel token, plus the separately specified three hints. Add one-time chapter reward packs: alternate general repair vouchers and tunnel tokens every 20 unique level completions. Exact bonus cadence can be tuned after trial play. Required level-bound vouchers remain guaranteed independently of these packs.

Rewards appear on the completion screen and in a collectable Rewards area. Never award the same milestone twice by replaying or restarting. At inventory capacity, show the reward as waiting to collect instead of silently wasting it.

## 6. Hint rules requested

- New player starts with exactly 3 hints.
- Award 1 collectable hint for every 10 unique levels completed: 10, 20, 30 and so on, up to 200.
- Hold at most 5 hints. Do not sell a hint while the inventory is full.
- A milestone hint waits to be collected when the player already holds 5. Stored hints never exceed 5; waiting rewards are separately marked unclaimed.
- Replaying levels or jumping to an unlocked preview level does not farm milestone rewards. The milestone counter measures unique completions, not the displayed level number.
- Hints can also be bought with gems at the shop.

## 7. What one hint shows

Tap Hint to request help. After a valid solution has been found, deduct one hint and open a short demonstration. Animate a ghost courier along the route; light the demonstration houses and show the shadow turns. Also offer a static arrow route, with numbered arrows where tiles are visited more than once. The real run remains paused and unchanged.

For a normal map, show a route from the player's current position, house mask, remaining light, shadow phases, timers and actual modified terrain. For a fresh repair-required map, the demonstration includes the required repair action and uses its available level-bound voucher. It must not imply a free path through a blocked bridge.

If the current run cannot be completed from its current state, explain why and offer a restart demonstration. Do not charge a hint for a nonexistent solution. A valid restart demonstration consumes a hint only when the player chooses to view it.

The purchased demonstration can be replayed freely for the same unchanged run state. Taking another move or changing terrain requires a newly calculated demonstration. Closing an explanation, pressing Hint with zero stock or buying at capacity does not consume anything. A solve failure must not spend inventory.

The route overlay is advice, not automatic movement: close it and continue tapping tiles normally. If a terrain change or restart occurs, invalidate stale arrows and recalculate. Respect sound settings and reduced-motion preferences; the arrow-only version remains available.

## 8. Mobile screens

Bottom menu proposal: Play, Levels, Shop and More. Play includes the map, tappable side obstacle icons, remaining hints and an Items button. Items opens a small inventory sheet with repair/tunnel counts. More contains the full legend, settings and Rewards. This keeps shopping and inventory out of the map's usable area.

Shop shows gem balance, item count/capacity, gem prices and a short item explanation. Preview the selected item before purchase. For the direct repair tile, retain the current instant-purchase feedback when the player has selected an available payment method. No automatic gem spending while tapping a movement tile.

## 9. Validation before release

1. Every standard trial map has a verified legal no-item solution; every repair-required trial has no legal completion before its required repair, and a valid completion afterward.
2. A required voucher cannot be accidentally spent elsewhere; its repair is reachable and a player with zero gems/general items can still finish.
3. Retry, reload and level switching do not duplicate purchases, awards, terrain changes or voucher consumption.
4. Hints start at 3, claim once each 10 unique completions, never exceed 5, and demonstrate the actual current state without changing it.
5. Tunnel usage updates movement, shortest-route scoring, hints and the reviewer table. Unsupported targets cost nothing.
6. More open maps have several meaningful choices. Compare actual player attempts and route mistakes before expanding all later levels.

## 10. Implementation order

First build the gem wallet, shop, persisted item inventory and migration. Then add required repairs with protected free vouchers and ordinary-rubble drilling. Next implement the exact route demonstration and hint rewards. Finally build ten open, branching trial maps across four-to-eight-house difficulty bands, review phone play and economy, and apply the accepted patterns to the later campaign.

The next level-wise report should add: Standard/Repair required, free voucher supplied, gem repair price, minimum moves before/after changes, and tunnel eligibility. For required maps the no-repair field must read "Not possible", not zero or an estimated path.
