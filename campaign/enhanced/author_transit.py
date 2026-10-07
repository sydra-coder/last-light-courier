"""Find optional one-turn return transit links for levels 1701–1800."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/transit-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[700:800]
proofs=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[700:800]
def key(p):return f'{p[0]},{p[1]}'
def replay(l,route,jump):
    walls=set(l['walls']);repair=l.get('repair');bought=bool(l.get('repairRequired'))
    if bought and repair and repair['effect']=='open':walls.discard(key(repair['tile']))
    cap=l['cap']+(3 if bought and repair and repair['effect']=='beacon' else 0)
    s={'p':l['depot'],'mask':0,'light':cap,'phase':l['phase'],'phase2':l['phase2'],
       'active':False,'fade':None,'ice':None,'gate':0,'trail':[]}
    for t,p in enumerate(route[1:],1):
        prev=s['p'];is_jump=t==jump
        if not is_jump and abs(p[0]-prev[0])+abs(p[1]-prev[1])!=1:return None
        if not(0<=p[0]<l['grid'] and 0<=p[1]<l['grid']) or key(p) in walls:return None
        if s['mask'] and p==l['authoredEvent']['tile']:return None
        if p==l['fade'] and s['fade']==0 or p==l['ice'] and s['ice']==0:return None
        if p==l['gate'] and s['gate']<=0 and not(bought and repair and repair['effect']=='latch'):return None
        if s['active']:
            for patrol,ph in ((l['patrol'],s['phase']),(l['patrol2'],s['phase2'])):
                if patrol and (p==patrol[ph] or p==patrol[(ph+1)%len(patrol)]):return None
            if l['echo'] and p in s['trail']:return None
        idx=next((i for i,h in enumerate(l['homes']) if h['p']==p),-1)
        fresh=idx>=0 and not s['mask']&(1<<idx)
        mask=s['mask']|(1<<idx if fresh else 0)
        home=p==l['depot'] and mask
        cost=2 if is_jump or p==l['dark'] and not(bought and repair and repair['effect']=='lamp') else 1
        light=min(cap,s['light']-cost+(2 if fresh else 0))
        if light<=0 and not(fresh or home):return None
        if home and t!=len(route)-1:return None
        s={'p':p,'mask':mask,'light':light,
           'phase':(s['phase']+1)%len(l['patrol']) if s['active'] else s['phase'],
           'phase2':(s['phase2']+1)%len(l['patrol2']) if s['active'] and l['patrol2'] else s['phase2'],
           'active':s['active'] or fresh,
           'fade':5 if p==l['fade'] and s['fade'] is None else None if s['fade'] is None else max(0,s['fade']-1),
           'ice':4 if p==l['ice'] and s['ice'] is None else None if s['ice'] is None else max(0,s['ice']-1),
           'gate':4 if p==l['switch'] else max(0,s['gate']-1),
           'trail':(s['trail'][-1:]+[prev]) if l['echo'] else []}
    if s['p']!=l['depot'] or s['mask'].bit_count()<l['required'] or s['light']<0:return None
    return s

authored=[];evidence=[];failed=[]
for l,proof in zip(levels,proofs):
    assert l['n']==proof['level']
    old=[s['p'] for s in proof['route']]
    last=max(i for i in range(1,len(proof['route'])) if proof['route'][i]['mask']!=proof['route'][i-1]['mask'])
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l.get(k)}
    special.update(tuple(h['p']) for h in l['homes'])
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    special.add(tuple(l['authoredEvent']['tile']))
    candidates=[]
    for i in range(last+1,len(old)-8):
        a=old[i]
        if tuple(a) in special:continue
        for j in range(i+8,len(old)-1):
            b=old[j]
            if tuple(b) in special or abs(a[0]-b[0])+abs(a[1]-b[1])<4:continue
            shortcut=old[:i+1]+[b]+old[j+1:]
            finish=replay(l,shortcut,i+1)
            if finish:candidates.append((j-i-1,finish['light'],i,j,a,b))
    if not candidates:failed.append(l['n']);continue
    saved,light,i,j,a,b=max(candidates,key=lambda c:(c[0],c[1],-c[2]))
    item=dict(l)
    item['transitLink']={'stops':[a,b],'rideLight':2,'unlocks':'first_delivery'}
    item['brief']=l['brief']+' After the first delivery, paired transit stops offer a one-turn ride across the region for two light.'
    authored.append(item)
    evidence.append({'level':l['n'],'boardAtStep':i,'exitAtOldStep':j,'stops':[a,b],
                     'walkingSteps':proof['steps'],'transitSteps':proof['steps']-saved,
                     'stepsSaved':saved,'transitFinishLight':light,'lastHouseStep':last})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed,
    'minStepsSaved':min((e['stepsSaved'] for e in evidence),default=None),'maxStepsSaved':max((e['stepsSaved'] for e in evidence),default=None)},indent=2),encoding='utf-8')
print(f'Transit links {len(authored)}/100; failed={failed}; saved range={min((e["stepsSaved"] for e in evidence),default=None)}–{max((e["stepsSaved"] for e in evidence),default=None)}')
