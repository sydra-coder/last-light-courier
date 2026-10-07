# CODEX MASTER PROMPT — Last Light Courier

You are receiving two branches in one handover.

## Goal
Recover and stabilize Last Light Courier without losing the Sep 27 baseline, while preserving useful October 5 enhancements as an isolated R&D branch.

## Non-negotiable facts
- The Sep 27 workbook is the recovered legacy source of truth for 1,000 level metadata records.
- It references `1000-Map-Solutions.json`, which is currently missing.
- October 5 generated Levels 001–300 are rejected as final level design.
- Do not silently blend those maps into the legacy campaign.
- APK packaging is deferred until game/level design is stable.

## Phase 1 — Repository setup
Create:
- `branches/legacy-baseline/`
- `branches/enhanced-experimental/`
- `shared/engine/`
- `shared/solver/`
- `shared/tests/`
- `docs/`

Preserve source files unchanged under `archive/`.

## Phase 2 — Legacy recovery
Parse `LEGACY_2026-09-27/DATA/legacy_level_summary_1_1000.json`.
Create typed schemas and regression tests for all recovered fields.
Search any newly supplied repo/archive for `1000-Map-Solutions.json`.

Never fabricate missing legacy maps without labeling them reconstructed.

## Phase 3 — Engine
Make runtime transitions pure/deterministic and reusable by solver:
- move
- wait
- light spend
- house completion
- Patrol shadow
- Echo shadow
- repair/shortcut
Then add enhanced mechanics one at a time.

## Phase 4 — Enhanced features
Cherry-pick only feature ideas, not the rejected generated layouts:
- D-pad/hold movement
- journey/background state changes
- inventory/shop
- stage-earned tools
- hidden houses
- house-triggered route unlocks
- shadow-house interactions
- traps
- 3×3 influence
- deterministic earthquake/storm/flood/night/rotation

## Phase 5 — Level redesign
Do not generate thousands yet.
First produce a representative approved block with:
- exact runtime/solver parity
- minimum solution cost
- alternate route count
- no softlock
- no unintended trivial route
- event state validation
- shadow timing validation
- human-readable solution trace

Only scale after review.

## Product direction
The user wants a visually rich journey map whose background/world evolves when mechanics change. Large maps need D-pad hold-to-move. Powers are earned at stage milestones and replenished in a shop. Some levels should be intentionally extremely tight on light.

Read both branch handovers before modifying code.
