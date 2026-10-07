# Last Light Courier — restored working base

The active review build is [`index.html`](index.html). It is a byte-for-byte copy of the earlier playable browser campaign from `C:\Game Finder\Last Light Courier`, Git commit `6fe2ddeae329f8c0148f61de77cbbadce7198900`. No gameplay or graphics changes were made during restoration.

## What is present

- The restored HTML has **200 playable levels** embedded in it, the three visual settings (Storybook Overhead, Isometric Village, Night), safe next-move highlighting, tap movement, and its existing hint flow.
- [`CAMPAIGN_1000_LEVELS.json`](CAMPAIGN_1000_LEVELS.json) contains **1,000 map records**. Its first 200 records exactly match the embedded playable levels and [`campaign/levels_001_200.snapshot.json`](campaign/levels_001_200.snapshot.json).
- [`design/map-solutions-1000.json`](design/map-solutions-1000.json) is the corresponding route archive. The later 800 routes are verified reference completions, not proven shortest routes. The review PDFs and summary workbook are also under [`design/`](design/).
- The campaign generator, renderer, solver, and expansion scripts are under [`campaign/`](campaign/). The earlier visual samples and isometric direction are under [`references/`](references/).

## Boundary for the next iteration

Levels 201–1000 are **archived map data, not yet integrated into the playable HTML or APK**. The earlier expansion handoff also identifies 32 levels that require a reserved free repair, plus large-map navigation and hint performance work. The October handover says generated campaign layouts need design review before they become final. Keep these records editable and traceable; do not treat them as approved legacy map geometry.

The restored HTML does **not** show a D-pad. Add it alongside tile taps in the next edit, using the existing movement rules. The ten-level HTML created in this workspace earlier remains at `last-light-courier-review.html` for comparison; it is superseded as the working base. `campaign-data/` contains duplicate copies from the initial import; the root catalogue and `design/` archive keep the original source layout and are the files to edit going forward.
