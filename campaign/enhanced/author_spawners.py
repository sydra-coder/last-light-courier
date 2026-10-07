"""Author growing 2x2 shadow-spawner zones for Breachlands 1201–1300."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/spawners-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[200:300]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[200:300]
authored=[];evidence=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=[tuple(s['p']) for s in proof['route']]
    trigger=proof['triggerStep']
    after=set(route[trigger+1:]);before=set(route[:trigger+1])
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    walls=set(level['walls']); choices=[]
    for x in range(level['grid']-1):
      for y in range(level['grid']-1):
        zone={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
        if zone&after or zone&special:continue
        open_zone=[p for p in zone if f'{p[0]},{p[1]}' not in walls]
        if len(open_zone)<4:continue
        adjacency=sum(any(abs(p[0]-q[0])+abs(p[1]-q[1])==1 for p in zone) for q in route[trigger+1:])
        if adjacency<2:continue
        # A road walked before delivery becoming dangerous after delivery is
        # particularly legible; otherwise choose a busy side branch.
        score=(len(zone&before)>0,adjacency,len(open_zone),-abs(x-level['grid']/2)-abs(y-level['grid']/2))
        choices.append((score,(x,y),zone,open_zone))
    assert choices,level['n']
    score,origin,zone,open_zone=max(choices,key=lambda c:c[0])
    # Progressive stages: one cell at delivery, a second after three moves,
    # the full 2x2 after six. Order always starts on open streets.
    ordered=sorted(open_zone,key=lambda p:(p not in before,p[1],p[0]))
    ordered+=sorted(zone-set(open_zone),key=lambda p:(p[1],p[0]))
    item=dict(level)
    item['shadowSpawner']={'trigger':'first_delivery','origin':list(origin),'stages':[list(p) for p in ordered],
                           'growthTurns':[0,3,6],'influence':'2x2'}
    item['brief']=level['brief']+' A shadow nest wakes at the first delivery, then fills a 2×2 side street over six turns.'
    authored.append(item)
    evidence.append({'level':level['n'],'triggerStep':trigger,'origin':list(origin),'stageCells':[list(p) for p in ordered],
                     'adjacentRouteSteps':score[1],'routeUsesZoneBeforeSpawn':bool(zone&before),
                     'postEventSteps':proof['steps'],'finishLight':proof['finishLight']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
print(f'Authored {len(authored)} expanding spawners; {sum(e["routeUsesZoneBeforeSpawn"] for e in evidence)} routes traverse zone before spawn')
