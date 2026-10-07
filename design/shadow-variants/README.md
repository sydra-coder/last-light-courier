# Shadow visual concepts

Open [shadow-review.html](shadow-review.html) to switch the tile preview among Isometric, Storybook, and Night. [contact-sheet-all.png](contact-sheet-all.png) shows all 19 designs; [new-shapes-review.html](new-shapes-review.html) and [new-shapes-contact-sheet.png](new-shapes-contact-sheet.png) focus on the eight new silhouettes. The individually named PNGs are transparent concepts.

The current game draws regular patrol shadows and the Echo Shadow from the same purple shape in `campaign/isometric-scene.js`; the Echo is fainter. These concepts preserve that visual distinction. The Echo examples in the review page use the same PNG at lower opacity. No collision, patrol, Echo trail, or movement rule has changed.

## Set

| ID | Design | Proposed use |
|---|---|---|
| 01 | Night Wisp | All-season default |
| 02 | Dussehra Ember | Seasonal look |
| 03 | Halloween Hush | Seasonal look |
| 04 | Diwali Afterglow | Seasonal look |
| 05 | Winter Frost | Christmas/winter look |
| 06 | New Year Stardrift | Seasonal look |
| 07 | Canal Mist | Waterline/canal districts |
| 08 | Old City Cinder | Old City districts |
| 09 | Bell Hollow | Broad alternate silhouette |
| 10 | Ribbon Wraith | Tall alternate silhouette |
| 11 | Moth Veil | Wide alternate silhouette |
| 12 | Crescent Lurker | Open crescent silhouette |
| 13 | Shard Mask | Angular broken-mask silhouette |
| 14 | Ink Puddle | Low horizontal silhouette |
| 15 | Thorn Crown | Jagged crown silhouette |
| 16 | Eclipse Orb | Compact circular silhouette |
| 17 | Veil Hand | Five-fingered silhouette |
| 18 | Serpent Coil | Coiled spiral silhouette |
| 19 | Hourglass Shade | Pinched hourglass silhouette |

## Selection proposal

- Let the player choose an owned courier and outfit independently of the level. Keep cosmetic ownership separate from gameplay purchases until the shop design is approved.
- Give each level an explicit `shadowSkinId`, defaulting to `night-wisp` when absent. Existing patrols and Echo in the level use that appearance; Echo remains paler. This makes the level's shadow appearance predictable and avoids changing it during a run.
- Use a seasonal look only when assigned to that level or when a separately reviewed seasonal override is active. If a seasonal override is used, resolve it when the level starts and hold it for the whole run.
- Treat all 19 as **visual skins**. A different outline, costume effect, or seasonal accent must not imply a new shadow ability. In particular, Veil Hand does not grab and Serpent Coil does not constrict. New hazards would need their own approved mechanics and distinct warning art.

The strongest shape options from the tile preview are **01 Night Wisp** as the default, **09 Bell Hollow** for a broad clear silhouette, and **11 Moth Veil** for later districts. **10 Ribbon Wraith** is very thin at tile size and needs in-game readability testing before selection. For seasonal accents, **05 Winter Frost** and **07 Canal Mist** remain distinct from the courier's warm lantern; the orange effects in 02–04 need extra contrast review in Night mode.

The new set adds genuinely different outlines. **12 Crescent Lurker**, **13 Shard Mask**, **16 Eclipse Orb**, and **18 Serpent Coil** read most clearly at the small tile preview size. **14 Ink Puddle** is especially different, but its low profile needs a normal-play check against floor art. **15 Thorn Crown** has many fine tips, **17 Veil Hand** could suggest an unimplemented grab, and **19 Hourglass Shade** is narrow; use those only after an in-game readability check.

## Asset status and verification

The 19 PNGs were generated with the built-in imagegen tool. The shared prompt required one isolated dark-violet hovering hazard, pale eyes, a vivid violet rim, transparent alpha, and readability at 48–64 px. Seasonal images edited 01 while preserving silhouette and eye placement; 09–19 explored alternate shapes with the same hazard cues. All 19 files exist. The full and new-shapes contact sheets were rendered and visually inspected. These are single-frame concepts, not animation-ready runtime sprites; actual visibility in normal play across all three views remains untested.
