"""Screen quake maps for direct geometric tours that may bypass winding routes.

This ignores light, shadows and timed map events. It is a design diagnostic,
never an in-game shortest-route claim.
"""
from collections import deque
from pathlib import Path
import argparse
import json
import os
import statistics
import random

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--wall-overrides',type=Path)
parser.add_argument('--output',type=Path,default=root/'campaign/enhanced/static-shortcut-audit-901-1000.json')
parser.add_argument('--shadow-field-candidates',type=Path)
parser.add_argument('--candidate-output',type=Path)
parser.add_argument('--start',type=int,default=901)
parser.add_argument('--end',type=int,default=1000)
parser.add_argument('--neighbor-order',choices=['EWSN','ENWS','WSEN','NESW','SWNE'],default='EWSN')
parser.add_argument('--house-order-variant',choices=['best','reverse','rotate','swap_first','swap_middle','swap_last','random'],default='best')
parser.add_argument('--house-order-seed',type=int,default=1)
args=parser.parse_args()
assert 201<=args.start<=args.end<=2000
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])[args.start-1:args.end]
if args.wall_overrides:
    overrides=json.loads(args.wall_overrides.read_text(encoding='utf-8'))
    for level in levels:
        level['walls']=[*level['walls'],*overrides.get(str(level['n']),[])]
proof_sources=[
    root/'campaign/enhanced/quakes-v1/post_event_routes.json',
    root/'campaign/enhanced/road-events-v1/post_event_routes.json',
]
proof_lookup={item['level']:item for source in proof_sources for item in json.loads(source.read_text(encoding='utf-8'))}
if args.start<=800:
    archive=json.loads((root/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
    proof_lookup.update({item['level']:{'level':item['level'],'route':item['solutions'][0]['route']}
                         for item in archive[args.start-1:min(args.end,800)]})
    spur_path=root/'campaign/enhanced/bridge-spurs-v1/routes.json'
    if spur_path.exists():
        for number,points in json.loads(spur_path.read_text(encoding='utf-8')).items():
            if args.start<=int(number)<=args.end:
                proof_lookup[int(number)]={'level':int(number),'route':[{'p':p} for p in points]}
proofs=[proof_lookup[n] for n in range(args.start,args.end+1)]
assert len(levels)==len(proofs)==args.end-args.start+1

def distances(level, start, block_depot=False):
    size=level['grid']; walls=set(level['walls'])
    if level.get('repairRequired') and level.get('repair'):
        tile=level['repair']['tile'];walls.discard(f'{tile[0]},{tile[1]}')
    queue=deque([tuple(start)]);found={tuple(start):0};parents={}
    while queue:
        x,y=queue.popleft()
        directions={'E':(1,0),'W':(-1,0),'N':(0,-1),'S':(0,1)}
        for dx,dy in (directions[letter] for letter in args.neighbor_order):
            neighbor=(x+dx,y+dy)
            a,b=neighbor
            if block_depot and neighbor==tuple(level['depot']):continue
            if 0<=a<size and 0<=b<size and f'{a},{b}' not in walls and neighbor not in found:
                found[neighbor]=found[(x,y)]+1;parents[neighbor]=(x,y);queue.append(neighbor)
    return found,parents

def tour(level):
    points=[tuple(level['depot'])]+[tuple(h['p']) for h in level['homes']]
    n=len(points)-1
    graphs=[distances(level,p) for p in points]
    no_depot={i:distances(level,points[i],True) for i in range(1,n+1)}
    if any(points[j] not in (graphs[i][0] if i==0 or j==0 else no_depot[i][0])
           for i in range(n+1) for j in range(n+1)):return None
    d=[[(graphs[i][0] if i==0 or j==0 else no_depot[i][0])[p]
        for j,p in enumerate(points)] for i in range(n+1)]
    full=(1<<n)-1
    dp=[{} for _ in range(full+1)]
    parents={}
    for j in range(n):dp[1<<j][j]=d[0][j+1];parents[(1<<j,j)]=-1
    for mask in range(1,full+1):
        for j,cost in tuple(dp[mask].items()):
            remaining=full^mask
            while remaining:
                bit=remaining&-remaining;remaining-=bit;k=bit.bit_length()-1
                nxt=mask|bit;candidate=cost+d[j+1][k+1]
                if candidate<dp[nxt].get(k,10**9):
                    dp[nxt][k]=candidate;parents[(nxt,k)]=j
    last=min(dp[full],key=lambda j:dp[full][j]+d[j+1][0])
    steps=dp[full][last]+d[last+1][0]
    order=[];mask=full;j=last
    while j>=0:
        order.append(j+1);previous=parents[(mask,j)];mask^=1<<j;j=previous
    houses=list(reversed(order))
    if args.house_order_variant=='reverse':houses.reverse()
    elif args.house_order_variant=='rotate':houses=houses[1:]+houses[:1]
    elif args.house_order_variant.startswith('swap_') and len(houses)>1:
        index={'swap_first':0,'swap_middle':max(0,len(houses)//2-1),'swap_last':len(houses)-2}[args.house_order_variant]
        houses[index],houses[index+1]=houses[index+1],houses[index]
    elif args.house_order_variant=='random':
        random.Random(level['n']*1000003+args.house_order_seed).shuffle(houses)
    order=[0]+houses+[0]
    steps=sum(d[a][b] for a,b in zip(order,order[1:]))
    route=[points[0]]
    for a,b in zip(order,order[1:]):
        ancestry=(graphs[a][1] if a==0 or b==0 else no_depot[a][1])
        segment=[points[b]]
        while segment[-1]!=points[a]:segment.append(ancestry[segment[-1]])
        route.extend(reversed(segment[:-1]))
    assert len(route)-1==steps
    return steps,route

rows=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    static=tour(level)
    steps=len(proof['route'])-1
    rows.append({'level':level['n'],'grid':level['grid'],'houses':len(level['homes']),
                 'verifiedRouteSteps':steps,'staticTourSteps':static[0] if static else None,
                 'staticCandidateRoute':[list(p) for p in static[1]] if static else None,
                 'routeToStaticRatio':round(steps/static[0],2) if static else None,
                 'freeRepairRequired':bool(level.get('repairRequired'))})
measured=[r for r in rows if r['staticTourSteps']]
report={'scope':'Static open-road tour only; ignores shadows, light, quake and aftershock state. A high ratio flags maps to playtest, not a proven shortcut.',
        'levels':len(rows),'measured':len(measured),
        'medianRouteToStaticRatio':statistics.median(r['routeToStaticRatio'] for r in measured),
        'over1_5':sum(r['routeToStaticRatio']>1.5 for r in measured),
        'over2_0':sum(r['routeToStaticRatio']>2 for r in measured),
        'top20':sorted(measured,key=lambda r:-r['routeToStaticRatio'])[:20],
        'rows':rows}
args.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
print({k:v for k,v in report.items() if k not in ('rows','top20')})
print('top five',[(r['level'],r['verifiedRouteSteps'],r['staticTourSteps']) for r in report['top20'][:5]])
if args.shadow_field_candidates:
    assert args.candidate_output
    options=json.loads(args.shadow_field_candidates.read_text(encoding='utf-8'))
    candidate_rows=[]
    for option in options:
        base=levels[option['level']-args.start]
        for choice in option['top']:
            altered={**base,'walls':[*base['walls'],*(f'{x},{y}' for x,y in choice['cells'])]}
            found=tour(altered)
            candidate_rows.append({'level':option['level'],'field':choice,
                                   'staticSteps':found[0] if found else None,
                                   'route':[list(p) for p in found[1]] if found else None})
    args.candidate_output.write_text(json.dumps(candidate_rows),encoding='utf-8')
    print('screened field candidates',len(candidate_rows))
