"""Find one static wall per phase map that blocks every saved signal shortcut."""
from collections import deque
from pathlib import Path
import json
import os

root=Path(__file__).resolve().parent
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root.parent.parent/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
screen_dir=root/'house-order-screen-v1'
shortcuts=json.loads((screen_dir/'signal-tour-screen.json').read_text())['shorterRoutes']
for found in json.loads((screen_dir/'known-tour-replay.json').read_text())['shorterRoutes']:
    source=json.loads((screen_dir/found['source']).read_text())['rows']
    route=next(x['staticCandidateRoute'] for x in source if x['level']==found['level'])
    shortcuts.append({**found,'route':route})
for source in filter(None,os.environ.get('LLC_EXTRA_SHORTCUT_REPORTS','').split(';')):
    shortcuts.extend(json.loads(Path(source).read_text(encoding='utf-8'))['completedRoutes'])
default={x['level']:x for x in json.loads((root/'road-events-v1/post_event_routes.json').read_text())}
signal={x['level']:x for x in json.loads((root/'candidates-v3/ROUTES_1001_2000_BASELINE.json').read_text())}

def points(value):
    if isinstance(value,list):
        if len(value)==2 and all(isinstance(x,int) for x in value):yield tuple(value)
        else:
            for item in value:yield from points(item)
    elif isinstance(value,dict):
        for name,item in value.items():
            if name not in ('walls','spine','route'):yield from points(item)

def distances(level,source,walls,close=None):
    q=deque([source]);seen={source:0};size=level['grid']
    while q:
        x,y=q.popleft()
        for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p!=close and p not in seen:
                seen[p]=seen[(x,y)]+1;q.append(p)
    return seen

report=[]
for n in sorted({x['level'] for x in shortcuts}):
    level=levels[n-1]
    routes=[{tuple(p) for p in x['route']} for x in shortcuts if x['level']==n]
    reference={tuple(s['p']) for s in default[n]['route']}
    reference.update(tuple(s['p']) for s in signal[n]['solutions'][0]['route'])
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    if level.get('repair',{}).get('effect')=='open':walls.discard(tuple(level['repair']['tile']))
    for event_name in ('quakeEvent','chainEvent'):
        for opened in level.get(event_name,{}).get('open',[]):walls.discard(tuple(opened))
    eligible=set.intersection(*routes)-reference-walls-set(points(level))
    first=tuple(next(s['p'] for s in default[n]['route'] if s['mask']))
    targets=[tuple(h['p']) for h in level['homes'] if tuple(h['p'])!=first]
    targets.append(tuple(level['depot']))
    candidates=[]
    for tile in eligible:
        candidate_walls=walls|{tile}
        open_dist=distances(level,first,candidate_walls)
        if not all(t in open_dist for t in targets):continue
        effects={}
        phase=level.get('phaseChoice')
        closures=[('default',tuple(phase['defaultClose'] if phase else level['authoredEvent']['tile']))]
        if phase:closures.append(('alternate',tuple(phase['alternateClose'])))
        for side,close in closures:
            closed=distances(level,first,candidate_walls,close)
            effects[side]=sum(open_dist[t]!=closed.get(t) for t in targets)
        forward=sum((first[0]+dx,first[1]+dy) not in candidate_walls and
                    (first[0]+dx,first[1]+dy)!=tuple(phase['defaultClose'] if phase else level['authoredEvent']['tile'])
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
        candidates.append({'tile':list(tile),'defaultAffectedTargets':effects['default'],
                           'alternateAffectedTargets':effects.get('alternate',0),
                           'manhattanToFirst':abs(tile[0]-first[0])+abs(tile[1]-first[1]),
                           'firstDeliveryNeighbors':forward})
    candidates.sort(key=lambda x:(-int(x['alternateAffectedTargets']>0),
                                  -int(x['defaultAffectedTargets']>0),
                                  -x['alternateAffectedTargets'],
                                  -x['defaultAffectedTargets'],
                                  -x['firstDeliveryNeighbors'],
                                  abs(x['tile'][0]-first[0])+abs(x['tile'][1]-first[1])))
    report.append({'level':n,'shortcuts':len(routes),'candidates':candidates})
output=root/'house-order-screen-v1/signal-shortcut-wall-search.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps([{'level':x['level'],'candidates':len(x['candidates']),
                   'best':x['candidates'][:2]} for x in report]))
