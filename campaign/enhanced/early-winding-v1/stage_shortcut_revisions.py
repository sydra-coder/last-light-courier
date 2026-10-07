"""Stage revised 101–200 maps and exact routes without touching live sources."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
archive = json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))
original_maps = json.loads((ROOT/'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))
exact = json.loads((HERE/'shortest_routes.json').read_text(encoding='utf-8'))
revisions = json.loads((HERE/'shortcut_revisions_candidate.json').read_text(encoding='utf-8'))
assert len(archive['levels']) == len(original_maps) == 1000
assert len(exact) == len(revisions) == 100
changed=[]
for row in revisions:
    n=row['level']
    if not row['changed']:continue
    assert row['success'] and row['after']['longest'] <= 12
    game=json.loads(json.dumps(original_maps[n-1]))
    assert all(wall not in game['walls'] for wall in row['addedWalls'])
    game['walls'] += row['addedWalls']
    route=row['route']
    assert route[0]['p'] == game['depot'] and route[-1]['p'] == game['depot']
    assert len(route)-1 == row['after']['steps']
    game['spine'] = list(dict.fromkeys(tuple(step['p']) for step in route))
    game['spine'] = [list(p) for p in game['spine']]
    archive['levels'][n-1] = {
        'level':n,
        'mapFingerprint':hashlib.sha256(json.dumps(game,sort_keys=True).encode()).hexdigest(),
        'map':game,
        'solutions':[{'repairPurchased':bool(game['repairRequired']),
                      'status':'solved','steps':len(route)-1,'route':route,'optimal':True}],
    }
    original_maps[n-1] = game
    exact[n-101] = {'level':n,'freeRepairRequired':bool(game['repairRequired']),
                    'steps':len(route)-1,'finishLight':route[-1]['light'],
                    'route':route,'source':'shortcut-revised exact solver'}
    changed.append(n)
assert len(changed)==33
(HERE/'map_solutions_1000_shortcuts_candidate.json').write_text(json.dumps(archive,separators=(',',':')),encoding='utf-8')
(HERE/'campaign_1000_shortcuts_candidate.json').write_text(json.dumps(original_maps,separators=(',',':')),encoding='utf-8')
(HERE/'shortest_routes_candidate.json').write_text(json.dumps(exact,separators=(',',':')),encoding='utf-8')
print(f'Staged {len(changed)} revised maps and exact routes; original sources untouched')
