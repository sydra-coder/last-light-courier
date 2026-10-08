# Night-village board-object concepts

Open [index.html](index.html) for the review and [contact-sheet.png](contact-sheet.png) for the contact sheet. The 15 individually named transparent PNGs are listed with generation provenance in [manifest.json](manifest.json). They were generated as original concept sprites with the built-in image generation tool, using the approved deep-navy storybook village and warm lantern direction. The advertisement reference was treated only as loose subject inspiration; no image from it is included or copied.

## Visual rules proposed for review

- Permanent blockers use full, grounded silhouettes: three different rock profiles, three different tree profiles, and a dense thorn bush. Their tile remains cool blue-grey with no yellow border.
- Repairable obstacles use separate damaged objects: ruptured rock, snapped trunk, and cut bush. The **whole tile** receives a thick yellow border and warm field. The yellow treatment is the primary small-size signal; tiny cracks alone cannot carry the meaning.
- Once cleared, the object disappears and the normal road surface is visible. The three states appear side by side at 40 px in the review. The road must remain recognizably open after the highlight disappears.
- On tap, show the repair cost in a compact overlay **above** the yellow tile. A nonadjacent or currently unsafe tile reveals the cost only. When entering the tile is a safe next move, offer a compact **Repair & move** confirmation and **Cancel**. Deduct points only after the confirmed move succeeds and the tile opens; cancelled, blocked, or abandoned actions spend nothing. The review page includes an interactive 60-point example with these states. The actual cost must come from the level's repair data; 60 is only a visual example.
- An unlit house has dark windows. A visited house has warm windows plus a bold green tile border and check marker. Green is reserved for the completed delivery state in these previews.
- A timed switch has idle, active, and expiring looks. Active uses amber light; expiring uses a stronger dashed amber ring. A production countdown may use a larger tile-edge arc, but must not rely on small printed numerals.

## Scope and QA

The 40 px tiles contain roughly 35 px art and are representative mockups. At 24 px the fine branches, rubble seams, and repair damage may need simplified production sprites; keep the yellow repair tile and green visited-house state prominent. The three generated house/switch states are separate concept images and would need alignment into one consistent production sprite set. These assets are single-frame design art, not runtime-ready animation or normal-play validation. No playable game code was changed.

The local review interaction was checked in a headless browser: distant tap, unsafe tap, and Cancel left the example balance at 120; an adjacent safe confirmation opened the road and reduced it to 60. This tests the **review mockup only**.
