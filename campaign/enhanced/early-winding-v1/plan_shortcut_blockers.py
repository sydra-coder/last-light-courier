"""Find optional street cells that can interrupt straight shortest routes."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
exact = json.loads((Path(__file__).parent/'shortest_routes.json').read_text(encoding='utf-8'))
archive = json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
plans = []
for proof in exact:
    n = proof['level']
    game = archive[n-1]['map']
    ref = {tuple(step['p']) for step in archive[n-1]['solutions'][0]['route']}
    points = [tuple(step['p']) for step in proof['route']]
    directions = [(b[0]-a[0], b[1]-a[1]) for a, b in zip(points, points[1:])]
    protected = ref | {tuple(game['depot'])} | {tuple(h['p']) for h in game['homes']}
    for key in ('fade', 'ice', 'dark', 'switch', 'gate'):
        if game.get(key): protected.add(tuple(game[key]))
    for key in ('patrol', 'patrol2'):
        protected.update(tuple(p) for p in game.get(key) or [])
    if game.get('repair'):protected.add(tuple(game['repair']['tile']))
    runs = []
    start = 0
    for i in range(1, len(directions)+1):
        if i < len(directions) and directions[i] == directions[start]:continue
        length = i-start
        if length > 12:
            cells = points[start+1:i]
            candidates = [p for p in cells if p not in protected]
            runs.append({'startStep':start,'length':length,'candidates':[list(p) for p in candidates]})
        start = i
    if runs:plans.append({'level':n,'runs':runs})
summary={'levels':len(plans),'runs':sum(len(p['runs']) for p in plans),
         'runsWithSafeBlocker':sum(bool(r['candidates']) for p in plans for r in p['runs']),
         'noSafeBlocker':[p['level'] for p in plans if any(not r['candidates'] for r in p['runs'])]}
(Path(__file__).parent/'shortcut_blocker_plan.json').write_text(json.dumps({'summary':summary,'plans':plans},indent=2),encoding='utf-8')
print(summary)
