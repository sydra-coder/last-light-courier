# Player records and all-player best

## Result screen now

The third result value is **All-player best**. It shows a dash with an offline explanation until a shared results service is connected. It never substitutes the calculated route minimum for a player's record. Your steps and Personal best remain visible. A partial delivery has no all-player comparison; the public comparison is for lighting every house and returning to the depot.

The browser review build creates a guest courier ID and stores a local player profile, up to 100 recent completed runs, and the best full-delivery step count for each level in `llc-player-data-v1`. Existing campaign progress remains in its own save. The guest ID is a device identifier for local continuity, not an authenticated public identity.

## Public record rule

- Metric: fewest **steps** for a full-house delivery that returns to the depot on the same level and rules revision.
- Eligible run: no hint, purchased repair, or consumable gameplay power. A mandatory free repair built into a level may be allowed under that level's versioned rule.
- Tie: show the shared step count; retain each tied player's record. Do not make paid items improve a public rank.
- A changed level layout or scoring rule starts a new rules revision. Old records remain historical and never compete with the revised map.
- The current local save and existing calculated route minima are not proof of a public record. Existing runs should not be uploaded as verified results.

## Data to store

| Record | Fields | Where |
| --- | --- | --- |
| Player | Account ID, chosen display name, consent and privacy settings, created/updated times | Shared service after account sign-in |
| Guest profile | Random device ID, guest label, created time | This device now |
| Run | Player ID, level ID, rules revision, steps, all-house completion, aid flags, move events, completion time, validation result | Shared service for future online runs |
| Per-level best | Level ID, rules revision, best steps, tied player IDs, verified run IDs | Shared service, derived from accepted runs |
| Progress | Cleared levels, trophies, personal bests, wallet/repairs/hints with conflict rules | Local now; optional cloud save later |

## Service and app flow

1. Player can play as a guest. The result screen records the run locally, including when offline.
2. On Android, offer account sign-in before public submission. Ask the player to choose or approve the display name shown with records. Link the guest profile to the account without replacing existing local progress silently.
3. Record moves and aid use from the start of each new run. Submit the run to an authenticated service when online.
4. The service replays the moves against the exact level and rules revision, checks completion and eligibility, then updates that player's level best and the all-player best in a database. Client-supplied steps alone are not accepted as proof.
5. The game requests `GET /levels/{levelId}/best` and displays a verified step count, player name, and rules revision. On no connection or no verified run, show a clear unavailable state.
6. Add account recovery, data export/deletion, rate limits, moderation of public names, and a retention policy before public launch.

## Infrastructure and review gates

This needs an account identity provider, an authenticated API, durable database, run verifier, and monitoring. The existing `design/trophies-competition-commerce/results-server.cjs` is a localhost-only test service with anonymous players and basic payload checks. It is not suitable for public scores or player accounts.

Before enabling the All-player best value: verify two distinct accounts on two devices, offline play then sync, guest-to-account linking, ties, aid exclusion, changed map revisions, replay rejection, data deletion, and account sign-out. Check that the displayed record comes from a verified player run, never from the calculated route minimum.
