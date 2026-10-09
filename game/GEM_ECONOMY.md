# Gem shop review rules

The browser game keeps earned points as the play score. Repairs and optional power restocks spend gems. Players can select multiple **2,000 earned points → 20 gems** batches in the Shop and exchange them in one transaction. The +/− controls never spend points; Exchange applies the total. A paid pack preview never adds gems. The tester build starts with 200 test gems; its save is separate from the player build.

The Shop sells power charges and displays gem packs. It does not list a level-specific repair: the player inspects the marked tile on the map and sees its cost before choosing whether to repair it.

Shop prices use four visible gem tiers. Existing repair prices in level data determine the tier without changing the levels: old cost 1–1,000 points = 10 gems; 1,001–2,000 = 15; 2,001–5,000 = 20; above 5,000 = 50. A zero-cost repair remains free. Milestone unlocks and level-provided power charges remain available.

| Power restock | Gems |
| --- | ---: |
| Anchor Trap, Decoy Light | 10 |
| Reveal Pulse, Lumen Flask | 15 |
| Road Repair, Light Bridge, Map Stabilizer | 20 |
| Freeze Seal, Rewind | 50 |

The 50-gem tier is reserved for powers with strong whole-map or recovery effects. These review prices can be tuned after playtesting.

| Product ID | Gems | Proposed US price |
| --- | ---: | ---: |
| `llc_gems_050` | 50 | $0.99 |
| `llc_gems_150` | 150 | $2.99 |
| `llc_gems_300` | 300 | $4.99 |
| `llc_gems_650` | 650 | $9.99 |
| `llc_gems_1400` | 1,400 | $19.99 |
| `llc_gems_3000` | 3,000 | $39.99 |

These are catalog proposals, not active offers. An Android app, matching one-time products in Play Console, localized prices returned by Google Play Billing, purchase verification, and consumption of fulfilled purchases are needed before charging money or crediting paid gems. Browser local storage is suitable only for gameplay review; verified purchases need a durable entitlement ledger.

Review with `node game/gem-shop-smoke.cjs` and `node game/repair-art-smoke.cjs`.
