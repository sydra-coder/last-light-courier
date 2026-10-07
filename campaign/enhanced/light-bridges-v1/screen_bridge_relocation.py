"""Find archived-route cells whose removal separates a required house.

Such a cell can serve as a necessary bridge while preserving the recorded route,
provided surrounding non-route streets can be closed and the full rules replay.
"""
from collections import Counter,deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']

def connected(level,streets):
    start=tuple(level['depot']);seen={start};queue=deque([start])
    while queue:
        x,y=queue.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if p in streets and p not in seen:seen.add(p);queue.append(p)
    return seen

rows=[]
for number in range(701,801):
    level=levels[number-1];states=archive[number-1]['solutions'][0]['route']
    positions=[tuple(s['p']) for s in states];counts=Counter(positions);streets=set(positions)
    homes={tuple(h['p']) for h in level['homes']};first=next(i for i,s in enumerate(states) if s['mask'])
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}|homes
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    choices=[]
    for index in range(first+2,len(states)-5):
        tile=positions[index]
        if tile in special or counts[tile]!=1 or min(s['light'] for s in states[index:])<2:continue
        isolated=homes-connected(level,streets-{tile})
        if isolated:choices.append({'tile':list(tile),'step':index,'isolatedHomes':[list(h) for h in sorted(isolated)]})
    rows.append({'level':number,'currentBridge':level['lightBridge'],'relocationCandidates':choices})
output=Path(__file__).with_name('bridge_relocation_screen.json')
output.write_text(json.dumps({'scope':'Route-union articulation candidates only. Surrounding map and full game rules still require validation.','rows':rows},indent=2),encoding='utf-8')
print('Maps with route-preserving relocation candidate:',sum(bool(r['relocationCandidates']) for r in rows),'/100')
print('First ten candidate counts:',[(r['level'],len(r['relocationCandidates'])) for r in rows[:10]])
