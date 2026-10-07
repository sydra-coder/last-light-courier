"""Measure the live first-100 routes without changing opening maps."""
from pathlib import Path
import json
import statistics

ROOT = Path(__file__).resolve().parents[2]
archive = json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
opening = json.loads((ROOT/'campaign/enhanced/opening-v1/shortest_routes.json').read_text(encoding='utf-8'))
rows = []
for n in range(1, 101):
    route = opening[n-1]['route'] if n <= 50 else archive[n-1]['solutions'][0]['route']
    positions = [step['p'] for step in route]
    directions = [(b[0]-a[0], b[1]-a[1]) for a, b in zip(positions, positions[1:])]
    straight = run = 0
    previous = None
    for direction in directions:
        run = run+1 if direction == previous else 1
        straight = max(straight, run)
        previous = direction
    rows.append({'level': n, 'steps': len(positions)-1, 'longestStraight': straight,
                 'finishLight': route[-1]['light']})
summary = {
    'maxStraight': max(r['longestStraight'] for r in rows),
    'over12': [r['level'] for r in rows if r['longestStraight'] > 12],
    'tenLevelMedians': {f'{start}-{start+9}': statistics.median(r['steps'] for r in rows[start-1:start+9])
                       for start in range(1, 101, 10)},
    'lowFinishLight': [r['level'] for r in rows if r['finishLight'] <= 2],
}
out = ROOT/'campaign/enhanced/opening-v1/pacing_audit.json'
out.write_text(json.dumps({'summary': summary, 'levels': rows}, indent=2), encoding='utf-8')
print(summary)
