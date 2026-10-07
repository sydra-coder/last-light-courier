"""Author deterministic road swaps for earthquake levels 801–1000."""
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'quakes-v1')
args=parser.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][800:1000]
assert [e['level'] for e in entries]==list(range(801,1001))

def side_paths(a,b,c):
    if a[0]!=c[0] and a[1]!=c[1]:
        for d in ((a[0],c[1]),(c[0],a[1])):
            if d!=b:yield [d]
    else:
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            side=[(p[0]+dx,p[1]+dy) for p in (a,b,c)]
            if b not in side:yield side

authored=[];proofs=[];failed=[]
for entry in entries:
    l=entry['map'];sol=entry['solutions'][0]
    route=[s['p'] for s in sol['route']]
    route_tuples=list(map(tuple,route))
    trigger=next(i for i,s in enumerate(sol['route']) if s['mask'])
    walls=set(l['walls'])
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l[k]}
    special.update(tuple(h['p']) for h in l['homes'])
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    candidates=[]
    for i in range(trigger+5,len(route)-5):
        a,b,c=route_tuples[i-1:i+2]
        if b in special or b in route_tuples[i+1:]:continue
        for detour in side_paths(a,b,c):
            if any(not(0<=p[0]<l['grid'] and 0<=p[1]<l['grid']) or p in special for p in detour):continue
            opening=[p for p in detour if key(p) in walls]
            if len(opening)>2:continue
            if any(p in route_tuples[:trigger+1] for p in opening):continue
            trial=route[:i]+[list(p) for p in detour]+route[i+1:]
            if b in map(tuple,trial[trigger+1:]):continue
            test=dict(l)
            test['walls']=[w for w in l['walls'] if w not in {key(p) for p in opening}]
            try:records=replay(test,trial,sol['repairPurchased'])
            except AssertionError:continue
            candidates.append((0 if opening else 1,abs(i-len(route)*.55),len(opening),i,list(b),[list(p) for p in opening],records))
        if len(candidates)>30:break
    if not candidates:
        failed.append(l['n']);continue
    _,_,_,index,closed,opened,records=min(candidates,key=lambda x:x[:6])
    item=dict(l)
    item['quakeEvent']={'trigger':'first_delivery','close':closed,'open':opened}
    item['brief']=l['brief']+' The first delivery triggers an earthquake that closes one road and may open another.'
    authored.append(item)
    proofs.append({'level':l['n'],'triggerStep':trigger,'closedRoad':closed,'openedRoads':opened,
                   'detourStartStep':index,'postEventSteps':len(records)-1,'finishLight':records[-1]['light'],
                   'route':records})

(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'post_event_routes.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':200,'authored':len(authored),'failed':failed,
    'openedRoadEvents':sum(bool(p['openedRoads']) for p in proofs)},indent=2),encoding='utf-8')
print(f'Authored {len(authored)}/200 earthquake maps; {sum(bool(p["openedRoads"]) for p in proofs)} open a new road; failed={failed[:15]}')
