# Last Light Courier — Final Design Handover

## Project Goal

Design an enhanced version of **Last Light Courier** while preserving the older game as a separate baseline.

The long-term enhanced campaign target is **2,000 levels**. The game should not become 2,000 increasingly large mazes. It should evolve from simple route planning into a system-driven puzzle game where the player eventually manipulates shadows, light, houses, roads, and the world itself.

---

## Core Design Principles

- The player is a courier carrying limited light and must reach required houses before the light runs out.
- Some levels should be forgiving, but there must also be intentionally **tight**, **near-exact**, and **exact-light** puzzles where one unnecessary action can cause failure.
- Shadows should appear **very early**, so the opening establishes the game’s identity quickly.
- Powers/tools are **earned by completing milestone stages**, become permanently unlocked, and are then used judiciously.
- The shop may replenish consumable charges using in-game currency, but must **never sell campaign progression**.
- If a level fundamentally requires a tool, that dependency must be guaranteed through progression or a supplied charge.
- Larger maps should use a **D-pad with hold-to-move**.
- On sufficiently large/known maps, safe auto-travel between already understood locations may be considered.
- The board should sit inside a changing illustrated world rather than looking like a detached dashboard.
- Backgrounds/scenes should evolve when major mechanics are introduced.
- APK/Android packaging should be deferred until the game and level design are stable.

---

# 2,000-Level Progression

| Levels | Region / Phase | Main progression |
|---|---|---|
| **1–100** | **Ember Road** | Movement, light, very early shadows, multiple houses, route efficiency, tight-light puzzles |
| **101–200** | **Dimming Crossroads** | Basic shadow control, traps, decoys, switches, more complex timing |
| **201–300** | **Veiled Hamlet** | Hidden houses, hidden routes, houses revealing/unlocking other objectives |
| **301–400** | **Lantern District** | Functional houses: recharge, beacon, safe, switch, cursed |
| **401–500** | **Broken Causeways** | Fragile roads, one-way routes, collapsing paths, temporary roads |
| **501–600** | **Hunting Dark** | Advanced shadow behaviour, expanded shadow threat, 3×3 influence |
| **601–700** | **The Shadowworks** | Shadow locks, Shadow Doors, deliberate shadow herding/manipulation |
| **701–800** | **River of Glass** | Light deposits, powered roads, temporary/light bridges |
| **801–900** | **Quake Frontier** | First major world transformations, especially earthquakes |
| **901–1000** | **Faultline City** | Triggered earthquakes, aftershocks, rotating/changing districts |
| **1001–1100** | **Storm March** | Wind, storms, movable blockers, flooding |
| **1101–1200** | **The Long Night** | Fog, hidden terrain, day/night rule changes |
| **1201–1300** | **Breachlands** | Spawner, Echo, merge/split and advanced shadow behaviours |
| **1301–1400** | **The Lumen Engine** | Light networks, split light, overload, advanced power routing |
| **1401–1500** | **Keeper’s Arsenal** | Advanced player tools, stabilisation and map-control powers |
| **1501–1600** | **Convergence** | Previously learned systems begin interacting heavily |
| **1601–1700** | **The Moving Kingdom** | Chained transformations and multi-state maps |
| **1701–1800** | **Last Provinces** | Large-region strategy, fast traversal and long-term route planning |
| **1801–1900** | **Black Horizon** | Multi-phase scenarios where early actions affect later states |
| **1901–2000** | **The Last Light** | Bespoke mastery levels using the full game language |

Mechanics should not disappear after their introduction. Once learned, they can return later in new combinations.

Difficulty should not simply mean “more mechanics at once.” A clever three-system puzzle is preferable to a level containing eight unrelated systems.

---

# Opening Progression

The first shadow should appear roughly around **Level 8–10**.

| Levels | Experience |
|---|---|
| **1–5** | Learn movement, light and reaching houses |
| **6–10** | Route choices and first shadow |
| **11–20** | Understand shadow timing/range |
| **21–40** | Multiple houses and route planning around darkness |
| **41–50** | Tight / near-exact light puzzles |
| **51–75** | Multiple shadows and more serious timing |
| **76–100** | Combine the opening mechanics into proper chapter puzzles |

The first 100 levels should already feel like **Last Light Courier**, not like a long tutorial before the real game begins.

---

# Core Shadow Progression

Shadows should evolve in behaviour rather than simply becoming statistically stronger.

Basic progression:

**Basic shadow → multiple shadows → larger influence → specialised shadow types → shadows become manipulable puzzle pieces**

Important shadow systems:

- **2×2 influence** early.
- **3×3 influence** later as a meaningful mechanic reveal.
- Shadows may eventually **enter certain houses**.
- A shadow can **drain/reset the light of a recharge/light house**.
- Shadows can be trapped, redirected, frozen, merged, split or deliberately positioned.

Important shadow variants:

### Patrol
Predictable route.

### Echo
Repeats the player’s earlier movement.

### Hunter
Actively pursues the courier.

### Leech
Prefers light sources/recharge houses and can drain them.

### Sentinel
Stationary but controls a larger area.

### Spawner
Creates smaller shadows if ignored.

### Merge / Split
Shadows can combine into a larger threat or split into smaller ones.

A shadow should sometimes be useful rather than purely harmful. Examples include **Shadow Locks** and **Shadow Doors**, where the player deliberately positions a shadow on a trigger.

---

# Houses and Objectives

Houses should become more than simple endpoints.

### Normal House
Delivery objective.

### Recharge House
Restores light.

### Safe House
Shadows cannot enter or threaten the player there.

### Beacon House
Reveals hidden houses, roads or terrain.

### Switch House
Changes another part of the map when reached.

### Cursed House
Required objective that triggers a negative event such as releasing a shadow or changing terrain.

Not all houses should be visible when the level starts.

Examples:

- `Reach 3 houses → hidden House X appears`
- `Reach House A → route opens → House B becomes reachable → House B reveals House C`

This allows levels to have multiple phases rather than displaying the entire solution at the start.

---

# Roads and Map Systems

Important road/map mechanics:

- **Branching routes** — shorter versus safer versus resource-efficient.
- **One-way roads**.
- **Fragile roads** — collapse after use.
- **Temporary roads**.
- **Light-powered roads**.
- **Light bridges** — spend light to create a crossing.
- **Switches / gates**.
- **Rotating map sections**.
- **Moving blockers**.
- **Moving houses** in selected advanced puzzles.

The late-game design philosophy should evolve from:

> “Find a path through the map.”

into:

> **“Transform the map into the path you need.”**

---

# Environment / System-Level Map Events

These systems must be deterministic and solvable. They should never randomly destroy a level.

## Earthquake

An earthquake can move roadblocks, break roads, open new routes or shift sections of the board.

Some levels should require the player to **deliberately trigger the earthquake** because the original configuration is impossible.

Later variants can include a visible countdown:

**Aftershock in 8 moves**

Important rule:

> After every mandatory earthquake state, at least one valid finishing route must remain from the player’s actual position with the player’s actual remaining light/resources.

## Aftershock

A smaller secondary earthquake after the first one.

The player should know it is coming and plan what to accomplish beforehand.

## Storm / Wind

Wind has a visible direction and can move eligible objects such as blockers, shadows, fog or light objects.

The result must be deterministic rather than random.

## Flood

Low roads become unavailable after a known trigger or countdown.

The player can either finish those areas first or use higher/alternate paths.

## Day / Night Cycle

Rules change by visible phase.

### Day
- weaker/slower shadows
- certain lights recharge

### Night
- larger shadow influence
- different routes/devices become active

The player should always be able to see the current and upcoming phase.

## District / Map Rotation

A whole road section can rotate or reconnect.

This may be activated by a switch, house or earthquake.

---

# Player Powers / Tools

The core earned toolkit currently consists of:

| Power / Tool | Function |
|---|---|
| **Anchor Trap** | Place a trap that locks/freezes a shadow when it enters the tile |
| **Decoy Light** | Creates a temporary false light that attracts selected shadow types |
| **Reveal Pulse** | Reveals hidden houses/routes/terrain |
| **Lumen Flask** | Restores a limited amount of light |
| **Freeze Seal** | Freezes active shadows for several turns |
| **Light Bridge** | Creates a temporary crossing across an otherwise blocked route |
| **Road Repair** | Restores a destroyed/collapsed road tile |
| **Rewind** | Undo a recent move and associated light spend |
| **Map Stabilizer** | Prevents/cancels one earthquake or aftershock |

These are **earned through progression**, not simply available in the shop from the beginning.

After unlocking a power, the shop can sell/replenish additional charges using earned in-game currency.

Additional possible late-game powers discussed, but not yet locked as mandatory features:

- **Light Pulse**
- **Shield**
- **Teleport to a previously visited house**
- **Rotate Section**
- **Beacon Pulse**
- **Shadow Lock**
- **Light Swap**
- **Emergency Recall**

Only include these if they genuinely create puzzle decisions.

---

# Trap System

Traps should evolve too.

### Basic Trap
Freezes shadow temporarily.

### Permanent Anchor
Locks shadow for the remainder of the level.

### Destroy Trap
Destroys the shadow but may also destroy the road tile.

### Light Trap
Only functions while illuminated.

The number of traps should often be limited so placement matters.

Later puzzles can give one trap for several shadows, forcing a strategic choice.

---

# Light Engineering

Light should eventually become more than just a move counter.

Important late-game concepts:

### Light Well
Standalone recharge location.

### Light Deposit
Leave light in a house/device.

### Light Transfer
Move stored light between locations.

### Illuminated Zone
Deposited light creates a safe region.

### Reflectors / Mirrors
Redirect beams.

### Light Beam
Activate distant devices/roads.

### Light Network
Distribute limited light through several connected systems.

### Light Overload
A device may require a particular light range rather than simply “more is better.”

This creates puzzles where the player must choose whether light is spent on:

**movement, safety, infrastructure, or objectives.**

---

# Shop / Economy

The shop is part of the game, but it must not become pay-to-win.

Core rule:

> **The player earns a tool first. The shop only replenishes it afterward.**

The shop can sell:

- consumable power charges;
- utility restocks;
- optional convenience items;
- cosmetic/world presentation items later if desired.

Campaign progress must never require a purchase.

If a puzzle explicitly requires a tool, either:

- the level provides a guaranteed use;
- or progression guarantees the player has access to it.

The economy should reward saving tools for difficult levels.

---

# Tight-Level Philosophy

Some levels should intentionally have almost no wasted movement.

### Standard
Several spare light.

### Tight
Small margin.

### Near-exact
Perhaps 1–2 unnecessary actions maximum.

### Exact
Intended route finishes at 0–1 light.

### Power-route
Exact without a clever tool, or meaningfully different if a saved tool is used.

Exact levels should feel like authored puzzles, not arbitrary punishment.

---

# Validation / Solver Requirements

A simple “there is some path” validator is not enough.

The game runtime and the solver should use the **same deterministic transition logic**.

Every final level should be tested for:

- valid completion route;
- minimum light / move cost;
- alternate winning routes;
- no unintended trivial shortcut;
- no softlock states;
- shadow timing;
- house completion state;
- tool/inventory assumptions;
- hidden-house reveal state;
- route unlock state;
- earthquake/storm/flood/night state;
- remaining light after every map transformation.

For a world-changing event, validation must start from the **actual state when the event occurs**, including:

`player position + remaining light + completed houses + inventory + shadow state + route state`

and prove that completion is still possible.

---

# Visual / Journey Direction

The game should visually resemble an illustrated journey rather than a plain grid UI.

The puzzle board remains readable in the foreground, while the world behind it evolves.

Examples:

- peaceful village/dawn;
- first-shadow dusk;
- abandoned crossroads;
- hidden/fog settlement;
- lantern district;
- broken causeways;
- dark forest/hunting region;
- quake frontier;
- storm region;
- flooded roads;
- ancient light-engine ruins;
- fractured late-game kingdom;
- black horizon/final lantern.

When an important mechanic appears, the environment should visibly communicate that change.

We do **not** need 2,000 unique background images. Use a manageable set of chapter scenes and variations.

---

# Development / Review Process

Do **not** blindly generate all 2,000 levels in one pass.

Work in **100-level review blocks**:

`1–100 → review`  
`101–200 → review`  
`201–300 → review`  
…and so on.

Within those blocks, level planning, engine support, economy, art direction and validation can progress in parallel.

However, the previous automatically generated October 5 Levels 1–300 were **rejected as final level designs**. They may only be used as technical experiments/reference.

APK/Android packaging should be left **until the game, level design and mechanics are stable**.

---

# Important Legacy Baseline

There is also a separate older **1,000-level baseline from Sep 27** that must not be overwritten.

Recovered legacy progression includes:

- Levels 1–40: **1 Patrol shadow**
- Levels 41–60: **1 Patrol + Echo**
- Levels 61–1000: **2 Patrols + Echo**
- Grid grows from **8×8 → 24×24**
- Houses grow from roughly **3 → 11**
- Earlier repair/shortcut economy used legacy Points and later proposed Gems
- Every 25 levels from roughly Level 225 onward had a reserved mandatory district-repair pattern

The old source spreadsheet survives, but the exact original `1000-Map-Solutions.json` and original game engine/map geometry were not recovered.

Therefore the new version should be treated as an **enhanced redesign informed by the legacy baseline**, not as a replacement pretending the old game never existed.

---

# Intended Evolution

**Navigate the road**  
→ **survive shadows**  
→ **choose house order**  
→ **manipulate shadows**  
→ **unlock/reveal the map**  
→ **manage light as infrastructure**  
→ **survive changing terrain**  
→ **control changing terrain**  
→ **transform the whole map into the solution**

This is the central design direction for **Last Light Courier**.
