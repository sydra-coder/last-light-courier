# START HERE — Last Light Courier Codex Handover

There are **two separate branches** in this handover. Do not collapse them into one dataset.

## A. `LEGACY_2026-09-27/`
This is the recovered pre-redesign baseline.

What is authentic:
- Sep 27 1,000-level summary XLSX.
- Normalized 1–1000 CSV/JSON derived directly from that workbook.
- Original progression metadata.

What is missing:
- `1000-Map-Solutions.json`
- original old engine code
- exact map geometry and route sequences

The included JS is explicitly a reconstruction adapter.

## B. `TODAY_2026-10-05_EXPERIMENTAL/`
This contains October 5 feature work and generated level experiments.

Useful:
- UI
- D-pad
- shop/inventory ideas
- visual journey concept
- dynamic mechanics concepts
- validators / build scripts

Not approved:
- generated Levels 001–300 as final campaign maps

## Recommended Codex workflow

1. Initialize git.
2. Commit `LEGACY_2026-09-27` as `legacy-baseline`.
3. Commit `TODAY_2026-10-05_EXPERIMENTAL` on `enhanced-experimental`.
4. Build a shared deterministic engine without changing legacy data.
5. Search user-provided archives/repo for `1000-Map-Solutions.json`.
6. Reconcile the engine against recovered legacy metadata.
7. Cherry-pick only approved feature systems from the experimental branch.
8. Redesign levels in small reviewed batches; do not mass-generate until the runtime solver and human quality bar agree.
9. Keep APK packaging for the end.
