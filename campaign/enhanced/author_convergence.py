"""Combine two proven systems on each Convergence map, 1501–1600."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/convergence-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[500:600]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[500:600]
authored=[];evidence=[];failed=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=[tuple(s['p']) for s in proof['route']];trigger=proof['triggerStep']
    before=set(route[:trigger+1]);after=set(route[trigger+1:]);all_route=set(route)
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    walls=set(level['walls']);item=dict(level)
    if level['n']<=1550:
        wind=[]
        for i in range(trigger+2,len(route)-2):
            src=route[i]
            if src in before or src in special:continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                dst=(src[0]+dx,src[1]+dy)
                if not(0<=dst[0]<level['grid'] and 0<=dst[1]<level['grid']):continue
                if dst in all_route or dst in special or f'{dst[0]},{dst[1]}' in walls:continue
                wind.append((abs(i-len(route)//2),i,src,dst))
        if not wind:failed.append(level['n']);continue
        _,wind_step,src,dst=min(wind)
        avoid=special|{src,dst}
        count={p:route[trigger+1:].count(p) for p in after}
        dusk=[(abs(i-len(route)*.65),i,p) for i,p in enumerate(route)
              if i>trigger+2 and p not in before and p not in avoid and count[p]==1]
        if not dusk:failed.append(level['n']);continue
        _,dusk_step,tile=min(dusk)
        paid=proof['finishLight']>=1
        if not paid:
            free=[(abs(x-tile[0])+abs(y-tile[1]),(x,y)) for x in range(level['grid']) for y in range(level['grid'])
                  if (x,y) not in all_route and (x,y) not in avoid and f'{x},{y}' not in walls]
            if not free:failed.append(level['n']);continue
            _,tile=min(free)
        item['stormWind']={'trigger':'first_delivery','from':list(src),'to':list(dst)}
        item['nightfall']={'trigger':'first_delivery','tile':list(tile),'extraLight':1,'fogRadius':3}
        item['brief']=level['brief']+' First delivery shifts a wind blocker, closes a road, and brings fog with one costly dusk street.'
        evidence.append({'level':level['n'],'pair':'wind+nightfall','triggerStep':trigger,'windFrom':list(src),
                         'windTo':list(dst),'windRouteStep':wind_step,'duskTile':list(tile),
                         'duskRouteStep':dusk_step if paid else None,'finishLightAfterDusk':proof['finishLight']-int(paid)})
    else:
        zones=[]
        for x in range(level['grid']-1):
          for y in range(level['grid']-1):
            zone={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
            if zone&after or zone&special or any(f'{p[0]},{p[1]}' in walls for p in zone):continue
            adj=sum(any(abs(p[0]-q[0])+abs(p[1]-q[1])==1 for p in zone) for q in route[trigger+1:])
            if adj<2:continue
            zones.append(((bool(zone&before),adj), (x,y),zone))
        if not zones:failed.append(level['n']);continue
        _,origin,zone=max(zones,key=lambda z:z[0])
        stages=sorted(zone,key=lambda p:(p not in before,p[1],p[0]))
        source_idx=next(i for i,h in enumerate(level['homes']) if tuple(h['p'])==route[trigger])
        relay=[(abs(i-(trigger+6)),i,p) for i,p in enumerate(route) if i>trigger+1 and p not in before
               and p not in special and route[trigger+1:].count(p)==1]
        if not relay:failed.append(level['n']);continue
        _,relay_step,tile=min(relay)
        item['shadowSpawner']={'trigger':'first_delivery','origin':list(origin),'stages':[list(p) for p in stages],
                               'growthTurns':[0,3,6],'influence':'2x2'}
        item['lumenNetwork']={'sourceHouseIndex':source_idx,'relayTile':list(tile),'charge':2,'sealedUntilSource':True}
        item['brief']=level['brief']+' First delivery wakes a growing 2×2 shadow nest and powers a sealed light relay.'
        evidence.append({'level':level['n'],'pair':'spawner+relay','triggerStep':trigger,'spawnerOrigin':list(origin),
                         'stageCells':[list(p) for p in stages],'sourceHouseIndex':source_idx,
                         'relayTile':list(tile),'relayStep':relay_step,'finishLightFloor':proof['finishLight']})
    authored.append(item)
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed},indent=2),encoding='utf-8')
print(f'Convergence combinations {len(authored)}/100; failed={failed}')
