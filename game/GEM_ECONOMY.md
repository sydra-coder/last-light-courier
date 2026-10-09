# Gem shop review rules

The browser game keeps earned points as the play score. Repairs and optional power restocks spend gems. Players may confirm a repeatable exchange of **2,000 earned points for 20 gems**. A paid pack preview never adds gems. The tester build starts with 200 test gems; its save is separate from the player build.

Existing repair prices in level data convert at 100 points of the old price to one gem, rounded up. A zero-cost repair remains free. Power restocks cost 6–12 gems depending on the power; milestone unlocks and level-provided charges remain available. The conversion is a review balance and can be tuned before release.

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
