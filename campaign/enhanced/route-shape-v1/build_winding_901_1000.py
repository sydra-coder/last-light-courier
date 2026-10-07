"""Generate a versioned winding alternative to the 901-1000 legacy band."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "campaign" / "expansion"))
from build_1000 import build, metrics, replay

OUT = Path(__file__).resolve().parent

def longest(route):
    points = [tuple(s["p"]) for s in route]
    directions = [(b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])]
    best = current = 0
    previous = None
    for direction in directions:
        current = current + 1 if direction == previous else 1
        best = max(best, current)
        previous = direction
    return best

old = json.loads((ROOT / "design" / "map-solutions-1000.json").read_text(encoding="utf-8"))["levels"]
results = []
failures = []
for number in range(901, 1001):
    generated = build(number, winding=True)
    if generated is None:
        failures.append(number)
        continue
    game_map, states = generated
    old_route = old[number - 1]["solutions"][0]["route"]
    before, after = longest(old_route), longest(states)
    assert replay(game_map, [s["p"] for s in states], game_map["repairRequired"])[-1]["light"] >= 0
    assert metrics(game_map, game_map["repairRequired"])["components"] == 1
    results.append({"level": number, "map": game_map, "route": states,
                    "beforeStraight": before, "afterStraight": after,
                    "beforeSteps": len(old_route) - 1, "afterSteps": len(states) - 1})

payload = {"description": "Versioned proposed replacements; not integrated into campaign",
           "results": results, "failures": failures}
(OUT / "winding_901_1000_candidates.json").write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
summary = {"generated": len(results), "failed": failures,
           "oldOver12": sum(x["beforeStraight"] > 12 for x in results),
           "newOver12": sum(x["afterStraight"] > 12 for x in results),
           "maxNewStraight": max((x["afterStraight"] for x in results), default=None)}
(OUT / "winding_901_1000_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(summary)
