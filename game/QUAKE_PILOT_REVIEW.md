# Earthquake pilot for review

Open `game/tester.html` and select Level 801, 802, or 808. The player build retains its existing fixed quake maps.

Each pilot map has five selectable quake patterns. Lighting the first house randomly chooses a pattern that closes three roads and opens three roads. The tester's **⚡ Quake log** shows the chosen pattern, the six changed tiles, and before/after light and move counts. Use its pattern picker and **Replay** button to test the same pattern again.

At the trigger, the game searches from the courier's actual position, delivered houses, shadow phases, and remaining light. It accepts a random pattern only when the solver finds a full delivery and return route within the current light. The log shows the light needed **for that verified route**, not a globally certified minimum. If random patterns cannot be verified, it tries the original and then a no-closure fallback; a final unverified fallback adds no road closures and is labeled in the log. The pilot does not claim to rescue a run that was already impossible through earlier moves.

## Review checks

| Check | Result |
| --- | --- |
| Authored random patterns | 5 per level; 15 total |
| Forced pattern completion in integrated tester | 15 / 15 |
| Reachable first-house choices, followed by verified completion | 33 / 33 |
| Slowest live route check in desktop browser audit | 711 ms in the review checkout; 1,278 ms in the GitHub checkout |
| Player build random quake behavior | Disabled |

The three maps still have generous lantern budgets. Balance and phone performance need review before expanding the pilot to more levels. The 100,000-state search cap means an unusual path can remain unresolved; the fallback avoids adding closures in that case. A verified original pattern may also be used when a random candidate is not verified quickly enough.

Run `node game/quake-feedback-smoke.cjs`, `node game/quake-pilot-smoke.cjs`, and `node game/quake-first-house-audit.cjs` to repeat the focused checks.
