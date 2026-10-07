# Power inventory and route validation

## Player control

The game inventory is global. An earned power may be used on any level where its effect is applicable and a charge remains. `reviewPower` on a level identifies the featured power for campaign review; it is not an exclusive loadout or a requirement to spend that power. Power charges, availability, and per-run use remain independent for each power.

The Play screen shows power icons. A short tap uses a ready power immediately. A hold shows its name, charges, scope, and effect without spending a charge. Anchor Trap and Decoy Light are placed on the courier's current tile; the courier must be standing on a patrol route for Anchor Trap. Lumen Flask and Rewind affect the courier; other existing powers affect their marked road or the map. An unavailable tap explains why it did not activate.

## Current route check

After a power is used, the game checks the live state. On simple early maps, the current-state solver can verify a route or report that none remains. Elsewhere, an optimistic minimum travel distance and maximum possible lantern credit can prove some runs impossible. A passing light-budget check is **not** proof that a route survives moving shadows, timed roads, or other hazards; the screen says the route is unverified in that case.

This is a deliberately one-sided check for late maps. It must not be displayed as a verified completion, because the current solver does not model every mechanic in the 2,000-map campaign. The existing reference routes and assigned-power replay audits prove selected recorded runs, not arbitrary inventory use from arbitrary player positions.

## Gate for Earthquake, Storm, and future map powers

Do not ship a map-wide terrain-changing inventory power until it uses the same pure state transition rules as gameplay. The route check must start from the actual courier position and remaining lantern, lit-house mask, patrol phases, active timers, roads and bridges, current power stock, and all remaining one-time refills. It must include the proposed board mutation and determine whether the player can complete the required deliveries and return to the depot. Cache only by a complete state and rules revision, and replay any claimed route through the runtime rules before calling it verified.

Activation should test the proposed effect on a copy of the state. Commit the map change and charge only after a finishing route is verified. If no route exists, leave the board and charge untouched and explain why. If the search times out or cannot model a rule, label it unverified and leave the charge untouched. Deterministic effect variants can be checked ahead of time for quick mobile activation. This contract applies on every eligible map, regardless of whether that power was assigned as its review power.
