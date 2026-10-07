# Detailed screen mockups

Open [screen-mockups.html](screen-mockups.html) to review the five interactive phone screens: Map, Shop, Play, Courier, and Trophies. Settings opens from the top-right button. Direct links can start on a screen with `?screen=map`, `shop`, `play`, `courier`, or `trophies`.

This follows the approved [five-screen concept](five-screen-concept.png): night village, warm windows and lantern, navy panels, amber controls, and a prominent center Play tab. The village scene is used as a cropped visual reference in Play and Map; the controls and other panels are HTML/CSS mockups.

The Map shows ten levels per chapter across the 2,000-level plan. Levels 1–200 link to the current playable `index.html`; later stops are labelled as archive or planning. A selected stop previews a shadow from the 19 visual concepts. The assignment is illustrative metadata for this mockup; shadows gain no ability from their shape, and Echo stays a paler version of the selected design.

The Courier screen previews all 18 base character cutouts and all five existing outfit looks for each courier. Ember Scout uses individual PNGs; the remaining 17 couriers show the selected section of their transparent five-look sheets. This changes the visible clothes in the mockup, while final per-character sprite extraction and animation remain production work. Theme selection and prices are mockup state only. Shop purchase rules, gem earning, and ownership have not been approved. Existing banked points remain separate and retain their level-repair use.

## Proposed character names

These are display names for review; the role names and PNG filenames stay as they are.

| Character | Existing role | Character | Existing role |
| --- | --- | --- | --- |
| Asha Emberlane | Ember Scout | Tavi Mossbrook | Moss Ranger |
| Nila Lockwater | Canal Pilot | Rohan Bellwright | Bell Messenger |
| Eira Frostmere | Winter Warden | Pip Patchwell | Patchwork Runner |
| Fenn Rooftop | Rooftop Finch | Bram Gearford | Clockwork Porter |
| Lina Willowfen | Willow Guide | Kavi Seabright | Harbor Skipper |
| Sable Ashdown | Ash Cartographer | Mara Daybreak | Dawn Baker |
| Orin Foxglove | Foxglove Courier | Skye Bluecrest | Bluebird Runner |
| Iris Lamplight | Lantern Keeper | Zuri Marketwind | Market Sprinter |
| Noor Moonmere | Mooncap Wanderer | Sol Sunward | Sunset Relayer |

## Expandable wardrobe

The theme list is data-driven inside the mockup. Its five paid looks use the existing outfit concepts with broader names: **Marigold Trail**, **Hollowmoon**, **Gilded Lantern**, **Hearthbound**, and **Starwake**. The free base look is **Roadworn**. Each selectable look changes the courier's visible clothes. **Rainkeeper**, **Petalbound**, and **Copperfall** are future ideas without art or prices; they appear in Shop but are not selectable until an outfit exists. Themes can be everyday, seasonal, or celebratory; they are not tied to a release date. The existing concept catalogue and trial prices have not been renamed or changed.

Trophies and progress read the current `last-light-courier-campaign-v1` save if one exists in the same browser origin. This file never writes that save. It has no purchase or equip action. None of the current game rules, controls, art assignment, or economy were changed.

Visual checks: browser screenshots of all five pages were inspected at 390 × 844 phone size. The source artwork and character/shadow images load locally from the adjacent design folders. Final game integration still needs sprite extraction, directional animation, three-view readability checks, exact shadow assignment rules, and approved shop and trophy behavior.
