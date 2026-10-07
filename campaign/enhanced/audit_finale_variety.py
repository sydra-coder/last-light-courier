"""Inspect geometry and route repetition in the final 100 maps."""
from pathlib import Path
from collections import Counter
import json
import statistics
from itertools import groupby

ROOT = Path(__file__).resolve().parents[2]
maps = json.loads((ROOT/'campaign/enhanced/mastery-v1/authored_levels.json').read_text(encoding='utf-8'))
proofs = json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[900:]
assert len(maps) == len(proofs) == 100
routes = []
for level, proof in zip(maps, proofs):
    assert level['n'] == proof['level']
    positions = [step['p'] for step in proof['route']]
    routes.append(tuple((b[0]-a[0], b[1]-a[1]) for a, b in zip(positions, positions[1:])))
similarities = []
for previous, current in zip(maps, maps[1:]):
    a, b = set(previous['walls']), set(current['walls'])
    similarities.append({'levels': [previous['n'], current['n']],
                         'wallJaccard': round(len(a & b)/len(a | b), 3)})
summary = {'uniqueRouteDirections': len(set(routes)),
           'routeSteps': {'minimum': min(map(len, routes)),
                          'median': statistics.median(map(len, routes)),
                          'maximum': max(map(len, routes))},
           'archetypes': dict(Counter(level.get('masteryArchetype') for level in maps)),
           'adjacentWallSimilarity': {'median': statistics.median(x['wallJaccard'] for x in similarities),
                                      'maximum': max(x['wallJaccard'] for x in similarities)},
           'closestPairs': sorted(similarities, key=lambda x: -x['wallJaccard'])[:10],
           'maxConsecutiveArchetype': max(len(list(group)) for _,group in groupby(level.get('masteryArchetype') for level in maps)),
           'finalArchetype': maps[-1].get('masteryArchetype')}
assert summary['maxConsecutiveArchetype']<=5
assert summary['finalArchetype']=='Last light gauntlet'
out = ROOT/'campaign/enhanced/mastery-v1/variety_audit.json'
out.write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(summary)
