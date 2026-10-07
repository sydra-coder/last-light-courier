"""Find meaningful second-delivery openings that preserve mandatory repairs."""
from collections import deque
from pathlib import Path
from itertools import combinations
import json

root=Path(__file__).resolve().parents[2]
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs={x['level']:x for x in json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())}

def coords(value):
    if isinstance(value,list):
        if len(value)==2 and all(isinstance(x,int) for x in value):yield tuple(value)
        else:
            for item in value:yield from coords(item)
    elif isinstance(value,dict):
        for name,item in value.items():
            if name not in ('walls','spine','route'):yield from coords(item)

def distances(level,start,walls):
    size=level['grid'];q=deque([start]);found={start:0}
    stops=[tuple(p) for p in level.get('transitLink',{}).get('stops',[])]
    while q:
        x,y=q.popleft();neighbors=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        if stops and (x,y) in stops:neighbors.append(stops[1] if (x,y)==stops[0] else stops[0])
        for p in neighbors:
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in found:
                found[p]=found[(x,y)]+1;q.append(p)
    return found

report=[]
for n in (1625,2000):
    level=levels[n-1];proof=proofs[n]['route'];repair=tuple(level['repair']['tile'])
    first_two=[];seen=set()
    for step in proof:
        for i,h in enumerate(level['homes']):
            if step['p']==h['p'] and i not in seen:
                first_two.append(i);seen.add(i)
        if len(first_two)==2:break
    second=tuple(level['homes'][first_two[1]]['p'])
    targets=[tuple(h['p']) for i,h in enumerate(level['homes']) if i not in first_two]
    targets.append(tuple(level['depot']))
    all_walls={tuple(map(int,s.split(','))) for s in level['walls']}
    protected=set(coords(level))|{tuple(s['p']) for s in proof}
    current_open={tuple(p) for p in level['chainEvent']['open']}
    candidates=[]
    for tile in all_walls-protected:
        base=all_walls-{repair}
        after_walls=(all_walls-{tile}-{repair})|{tuple(level['chainEvent']['close'])}
        before_maps=[distances(level,source,base|{tuple(level['chainEvent']['close'])})
                     for source in [second,*targets]]
        after_maps=[distances(level,source,after_walls) for source in [second,*targets]]
        if not all(t in after_maps[0] for t in targets):continue
        affected=sum(t in before and after[t]<before[t]
                     for before,after,source in zip(before_maps,after_maps,[second,*targets])
                     for t in targets if t!=source)
        if not affected:continue
        no_repair=distances(level,tuple(level['depot']),after_walls|{repair})
        unreachable=[i for i,h in enumerate(level['homes']) if tuple(h['p']) not in no_repair]
        if len(level['homes'])-len(unreachable)>=level['required']:continue
        candidates.append({'tile':list(tile),'affectedTargets':affected,
                           'unreachableWithoutRepair':unreachable,
                           'distanceFromSecondHouse':after_maps[0].get(tile),
                           'manhattanFromSecondHouse':abs(tile[0]-second[0])+abs(tile[1]-second[1])})
    candidates.sort(key=lambda x:(-x['affectedTargets'],x['manhattanFromSecondHouse']))
    pair_candidates=[]
    if not candidates:
        static_choices=sorted(all_walls-protected-{repair})
        for a,b in combinations(static_choices,2):
            after_walls=(all_walls-{a,b,repair})|{tuple(level['chainEvent']['close'])}
            no_repair=distances(level,tuple(level['depot']),after_walls|{repair})
            unreachable=[i for i,h in enumerate(level['homes']) if tuple(h['p']) not in no_repair]
            if len(level['homes'])-len(unreachable)>=level['required']:continue
            after_maps=[distances(level,source,after_walls) for source in [second,*targets]]
            if not all(t in after_maps[0] for t in targets):continue
            before_maps=[distances(level,source,(all_walls-{repair})|{tuple(level['chainEvent']['close'])})
                         for source in [second,*targets]]
            affected=sum(t in after and (t not in before or after[t]<before[t])
                         for before,after,source in zip(before_maps,after_maps,[second,*targets])
                         for t in targets if t!=source)
            if not affected:continue
            pair_candidates.append({'tiles':[list(a),list(b)],'affectedTargets':affected,
                                    'unreachableWithoutRepair':unreachable,
                                    'manhattanFromSecondHouse':min(abs(p[0]-second[0])+abs(p[1]-second[1]) for p in (a,b))})
        pair_candidates.sort(key=lambda x:(-x['affectedTargets'],x['manhattanFromSecondHouse']))
    report.append({'level':n,'secondHouseIndex':first_two[1],'oldOpen':[list(p) for p in current_open],
                   'candidates':candidates,'pairCandidates':pair_candidates})
output=root/'campaign/enhanced/repair-chain-open-search.json'
output.write_text(json.dumps(report,indent=2))
print(json.dumps([{'level':x['level'],'candidates':len(x['candidates']),
                   'best':x['candidates'][:5],
                   'pairs':len(x['pairCandidates']),'bestPairs':x['pairCandidates'][:5]} for x in report]))
