# Holiday wardrobe review

Open [shop-preview.html](shop-preview.html) in a browser to choose among 18 couriers and five themed looks each. The preview includes a sample 250-gem wallet and lets you buy, equip, and reset cosmetic looks. Its state is separate from the playable game.

For quick comparison, open the six contact sheets: [1](contact-sheet-1.png), [2](contact-sheet-2.png), [3](contact-sheet-3.png), [4](contact-sheet-4.png), [5](contact-sheet-5.png), [6](contact-sheet-6.png). Each shows three couriers across all five holidays.

## Themes and trial prices

| Theme | Holiday date | Visual cue | Draft gem price |
|---|---|---|---:|
| Dussehra Victory | 20 Oct 2026 | Saffron and gold trim, marigold motifs | 60 |
| Halloween Nightwatch | 31 Oct 2026 | Plum, pumpkin orange, playful lantern details | 65 |
| Diwali Lights | 8 Nov 2026 | Jewel colors, gold borders, diya-inspired light | 80 |
| Christmas Hearth | 25 Dec 2026 | Evergreen, ivory winter lining, red scarf | 70 |
| New Year Starlight | 1 Jan 2027 | Midnight blue, silver stars, gold accents | 75 |

Dates for Dussehra and Diwali were checked against the [India Post 2026 holiday list](https://www.indiapost.gov.in/holidays-list). Christmas was checked against the [ISRO URSC 2026 holiday list](https://www.ursc.gov.in/holidays.jsp). Halloween and New Year's Day fall on their fixed calendar dates.

## Shop proposal

- The base courier looks remain free. Every costume is cosmetic: movement, lantern capacity, shadows, and scoring stay the same.
- Use the existing proposed **gems** currency. Prices above are trial values for review, not final balancing or real-money prices.
- Preview before purchase, show the exact gem cost, then keep the costume permanently selectable once bought. A holiday can feature a costume without removing an owned costume afterward.
- Save ownership and equipped look per courier when this is implemented in the game. Do not use the mock shop's browser storage as game ownership.

## Asset status

There are **90 visual outfit concepts**: five for each of 18 couriers. Ember Scout has five individual transparent PNGs. The other 85 looks are in 17 transparent five-look sheets. The sheets are intact because some lanterns and capes cross a narrow crop boundary. These are concept assets; individual production cutouts, directional poses, walk frames, mobile-size readability review in Storybook, Isometric, and Night views, and real shop integration remain to be done.

The imagegen prompts used each original courier PNG as an edit reference and kept its face, body, pose, defining garment silhouette, and lantern placement. Each five-look sheet asked for the holiday treatments in the order shown above with transparent background and no text or scenery. The [generated-sources.json](generated-sources.json) file records the source output for each set; [catalog.json](catalog.json) maps the 90 concepts to the preview.

Verification: `node validate-catalog.js` passes asset coverage and the sample buy, select, equip, reset flow; all 22 PNG sources have transparent corner pixels. Six full-width sheets and the shop preview were visually inspected in a browser render. The playable game files were not edited.
