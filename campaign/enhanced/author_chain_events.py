"""Author two-stage road transformations for Moving Kingdom 1601–1700."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/chain-events-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[600:700]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[600:700]
authored=[];evidence=[];failed=[]
for level,proof in zip(levels,proofs):
    assert level['n']==proof['level']
    records=proof['route'];route=[tuple(s['p']) for s in records]
    first=proof['triggerStep'];second=next((i for i,s in enumerate(records) if s['mask'].bit_count()>=2),None)
    if second is None:failed.append(level['n']);continue
    later=set(route[second+1:])
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    close=[(abs(i-(first+second)/2),i,p) for i,p in enumerate(route) if first<i<second and p not in special and p not in later]
    walls=set(level['walls']);opening=[]
    for i in range(second+1,len(route)-1):
        p=route[i]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            tile=(p[0]+dx,p[1]+dy)
            if not(0<=tile[0]<level['grid'] and 0<=tile[1]<level['grid']):continue
            if tile in special or f'{tile[0]},{tile[1]}' not in walls:continue
            opening.append((abs(i-(second+7)),i,tile))
    if not close or not opening:
        failed.append(level['n']);continue
    _,close_step,closed=min(close)
    _,near_step,opened=min(opening)
    item=dict(level)
    item['chainEvent']={'trigger':'second_delivery','close':list(closed),'open':[list(opened)]}
    item['brief']=level['brief']+' First delivery closes the marked road. The second delivery closes an earlier street and opens a new side road.'
    authored.append(item)
    evidence.append({'level':level['n'],'firstDeliveryStep':first,'secondDeliveryStep':second,
                     'secondClose':list(closed),'lastPreEventUseStep':close_step,
                     'secondOpen':list(opened),'nearRouteStep':near_step,
                     'postEventSteps':proof['steps'],'finishLight':proof['finishLight']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed},indent=2),encoding='utf-8')
print(f'Chained two-delivery events {len(authored)}/100; failed={failed}')
