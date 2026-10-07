# Home and bottom navigation review

## Selected visual direction — 6 October 2026

The five-screen [concept artwork](five-screen-concept.png) is the approved theme for the home and navigation screens. Use its deep navy night village, warm lantern and window light, detailed storybook isometric setting, brass and amber controls, framed dark panels, blue-cloaked courier, and consistent five-icon tab bar. Keep Play large and central. Maintain phone-size legibility when translating the artwork into actual screens; decorative lettering and small captions in the concept are not final UI copy.

The Shop screen establishes the visual style only. Its catalogue, prices, currencies, and actions remain to be defined. The current playable build's banked points and marked level repairs retain their existing meaning until a separate economy decision is made. Treat the artwork as concept/reference imagery, not as implemented UI or a game asset export.

Open [index.html](index.html) at phone width. The concept selector changes the visual treatment. The five bottom destinations are interactive: **Map, Shop, Play, Courier, Trophies**. Settings is the top-right button. The mockup reads the existing `last-light-courier-campaign-v1` save when it shares the game's origin and never writes it. Play and map stops open the restored game.

## Three visual concepts

1. **Lantern Village — recommended.** The courier and glowing houses anchor a night village. A large amber Play button sits below visible campaign progress. This follows the reference's strong central Play hierarchy and five-option navigation without copying its toy chest or art.
2. **Courier Ledger.** Parchment and slate tones give the same layout an archival feel. This suits a long chapter map, though it is quieter on the home screen.
3. **Shadow Watch.** A cooler violet palette and more prominent shadow emphasize danger. This is atmospheric but less welcoming and slightly less readable.

The village is CSS concept art. Production art should follow the selected isometric village direction: raised diamond lanes, grounded courier, steady lantern, warm delivery windows, and readable shadows. It must not suggest a different movement or shadow rule.

## Five destinations

| Tab | Player purpose | Current support and boundary |
| --- | --- | --- |
| Map | Browse ten-level chapters and open any of Levels 1–200. | Reads saved clears. Levels 201–1000 are archived map data under review, not playable here. |
| Shop | See the current point balance and preview future hint, repair voucher, and tunnel item categories. | Existing points pay for marked level repairs in the playable build. Gem prices, inventory, and purchasing are proposed and disabled in this mockup. |
| Play | Resume the first uncleared level, see journey progress, or replay after 200 clears. | Reads `cleared` and `wallet`; links to the restored game. This is the visually emphasized center tab. |
| Courier | See carried hints, pending milestone hints, delivery record, and proposed keepsakes. | Reads `hints`, `pendingHintRewards`, `cleared`, and `mastered`. Claiming and hint use remain in the playable game. Keepsakes have no current inventory. |
| Trophies | See unique clears, mastery count, and ten-clear milestone progress. | These are summaries of saved records. Named achievements and badge rewards are proposed, not awarded. |

Settings and the legend are accessed from the top-right settings route or the playable game. They do not consume a bottom slot.

## Current game versus expansion

The restored HTML has 200 playable levels, banked points, points-funded level repairs, hints, milestone claims, mastery records, and three view choices. Its current bottom sections differ from this proposed navigation. The 1,000-map catalogue is a review archive. The expansion's gems, stage-earned powers, shop replenishment, and required free repairs still need integration and approval. Banked points must not silently convert to gems or imply purchases.

## Open product decisions

1. Should the future campaign retain free selection of all available levels, as the current 200-level build does?
2. Should Courier become the place to claim existing milestone hints, or remain a read-only satchel until the flow is integrated?
3. Which keepsakes, if any, are worth collecting? Do not present them as earned until a rule exists.
4. What exact shop catalogue and gem earn rates should be approved before activating purchases? No real-money flow is assumed.
5. Should Trophies eventually award anything, or simply summarize progress and mastery?

This is a design mockup. It does not modify `index.html`, the save, rules, or purchase state.
