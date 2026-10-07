"""Author sealed, one-use charging relays for Lumen Engine levels 1301–1400."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/light-networks-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[300:400]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[300:400]
authored=[];evidence=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    route=[tuple(s['p']) for s in proof['route']]
    trigger=proof['triggerStep']
    source=route[trigger]
    source_idx=next(i for i,h in enumerate(level['homes']) if tuple(h['p'])==source)
    before=set(route[:trigger+1])
    after=route[trigger+1:]
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    choices=[]
    for i,p in enumerate(route):
        if i<=trigger+1 or p in before or p in special or after.count(p)!=1:continue
        choices.append((abs(i-(trigger+6)),i,p))
    assert choices,level['n']
    _,index,tile=min(choices)
    item=dict(level)
    item['lumenNetwork']={'sourceHouseIndex':source_idx,'relayTile':list(tile),'charge':2,'sealedUntilSource':True}
    item['brief']=level['brief']+' The first house powers a sealed relay road; its first crossing restores two lantern light.'
    authored.append(item)
    evidence.append({'level':level['n'],'triggerStep':trigger,'sourceHouseIndex':source_idx,
                     'relayTile':list(tile),'firstCrossingStep':index,'postEventSteps':proof['steps'],
                     'baseFinishLight':proof['finishLight']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
print(f'Authored {len(authored)} first-delivery light networks')
