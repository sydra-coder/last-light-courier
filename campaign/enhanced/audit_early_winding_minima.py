"""Compare exact early routes with the authored demonstration routes."""
from pathlib import Path
import json
import statistics

ROOT = Path(__file__).resolve().parents[2]
exact = json.loads((ROOT/'campaign/enhanced/early-winding-v1/shortest_routes.json').read_text(encoding='utf-8'))
reference = json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
assert len(exact) == 100
rows = []
for proof in exact:
    n = proof['level']
    assert 101 <= n <= 200
    points = [step['p'] for step in proof['route']]
    dirs = [(b[0]-a[0], b[1]-a[1]) for a, b in zip(points, points[1:])]
    longest = run = 0
    prev = None
    for direction in dirs:
        run = run+1 if direction == prev else 1
        longest = max(longest, run)
        prev = direction
    ref_steps = reference[n-1]['solutions'][0]['steps']
    rows.append({'level': n, 'exactSteps': proof['steps'], 'referenceSteps': ref_steps,
                 'referenceExcess': ref_steps-proof['steps'], 'exactLongestStraight': longest,
                 'freeRepairRequired': proof.get('freeRepairRequired', False)})
summary = {'levels': len(rows), 'medianReferenceExcess': statistics.median(r['referenceExcess'] for r in rows),
           'maxReferenceExcess': max(r['referenceExcess'] for r in rows),
           'exactStraightOver12': [r['level'] for r in rows if r['exactLongestStraight'] > 12],
           'maxExactStraight': max(r['exactLongestStraight'] for r in rows),
           'freeRepairRequired': [r['level'] for r in rows if r['freeRepairRequired']]}
(ROOT/'campaign/enhanced/early-winding-v1/minima_audit.json').write_text(
    json.dumps({'summary': summary, 'levels': rows}, indent=2), encoding='utf-8')
print(summary)
