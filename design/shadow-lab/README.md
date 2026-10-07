# Shadow Lab — five adverse shadow samples

Open `index.html` locally. Each sample is a small deterministic level with a delivery and return. The lab is separate from the playable 200-level baseline and the archived 1,000-map data.

| Shadow | Planned introduction | Rule in this sample |
| --- | ---: | --- |
| Hunter | 501 | Moves one tile toward the courier on even turns. |
| Leech | 521 | Extinguishes a lit recharge house on turn six; the courier must relight it. Delivery credit persists. |
| Sentinel | 551 | Does not move; controls a visible 3×3 area. |
| Spawner | 1201 | Produces a smaller shadow at turn five unless its nest is sealed. |
| Merge / Split | 1251 | Two shadows merge into a dangerous center form on turns four to six, then split. |

`test.cjs` explores each sample's deterministic state space and finds a completion route. These are rule prototypes for feedback, not integrated campaign levels or final difficulty tuning.
