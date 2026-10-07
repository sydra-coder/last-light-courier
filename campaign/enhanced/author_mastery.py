"""Author four combined mastery patterns for levels 1901–2000."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--candidates',type=Path,default=ROOT/'campaign/enhanced/candidates-v3')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/mastery-v1')
parser.add_argument('--stagger',action='store_true',help='Stage interleaved finale events while preserving the 25-per-archetype counts')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[900:1000]
defaults=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[900:1000]
baselines=json.loads((args.candidates/'ROUTES_1001_2000_BASELINE.json').read_text(encoding='utf-8'))[900:1000]
names=['Storm and fog','Shadow and light network','Chosen corridor','Last light gauntlet']
briefs=[
    'The first delivery shifts wind, closes a road, and brings fog. The second changes another street. Watch the dusk road.',
    'The first delivery wakes a growing shadow nest and powers a light relay. The second changes another street.',
    'Choose the first road closure at the depot. The first delivery powers a light relay; the second changes another street.',
    'The first delivery shifts wind, brings fog, wakes a shadow nest, and powers a light relay. The second changes another street.'
]
authored=[];evidence=[];failed=[]
def key(p):return f'{p[0]},{p[1]}'
def common(l):
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l.get(k)}
    special.update(tuple(h['p']) for h in l['homes'])
    special.add(tuple(l['authoredEvent']['tile']))
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    return special
for l,d,b in zip(levels,defaults,baselines):
    assert l['n']==d['level']==b['level']
    block,offset=divmod(l['n']-1901,25)
    pattern=block
    if args.stagger:
        early={3,8,14,19,23};middle={1,6,11,17,22};late={4,9,13,18,20}
        if block==0 and offset in early:pattern=1
        elif block==1 and offset in early:pattern=0
        elif block==1 and offset in middle:pattern=2
        elif block==2 and offset in middle:pattern=1
        elif block==2 and offset in late:pattern=3
        elif block==3 and offset in late:pattern=2
    records=d['route'];route=[tuple(s['p']) for s in records];first=d['triggerStep']
    second=next(i for i,s in enumerate(records) if s['mask'].bit_count()>=2)
    base=b['solutions'][0];base_route=[tuple(s['p']) for s in base['route']]
    base_second=next(i for i,s in enumerate(base['route']) if s['mask'].bit_count()>=2)
    walls=set(l['walls']);special=common(l);item=dict(l)
    other_after=set(base_route[base_second+1:]) if pattern==2 else set()
    closed_candidates=[(abs(i-(first+second)/2),i,p) for i,p in enumerate(route)
                       if first<i<second and p not in special and p not in route[second+1:] and p not in other_after]
    opened_candidates=[]
    for i in range(second+1,len(route)-1):
        p=route[i]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            q=(p[0]+dx,p[1]+dy)
            if 0<=q[0]<l['grid'] and 0<=q[1]<l['grid'] and q not in special and key(q) in walls:
                opened_candidates.append((abs(i-(second+7)),i,q))
    if not closed_candidates or not opened_candidates:failed.append(l['n']);continue
    _,close_step,chain_close=min(closed_candidates)
    _,open_near,chain_open=min(opened_candidates)
    item['chainEvent']={'trigger':'second_delivery','close':list(chain_close),'open':[list(chain_open)]}
    special|={chain_close,chain_open}
    info={'level':l['n'],'archetype':names[pattern],'firstDeliveryStep':first,'secondDeliveryStep':second,
          'chainClose':list(chain_close),'chainOpen':list(chain_open),'defaultSteps':d['steps'],
          'defaultFinishLight':d['finishLight']}
    if pattern in (0,3):
        wind=[];before=set(route[:first+1]);all_route=set(route)
        for i in range(first+2,len(route)-2):
            src=route[i]
            if src in before or src in special:continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                dst=(src[0]+dx,src[1]+dy)
                if 0<=dst[0]<l['grid'] and 0<=dst[1]<l['grid'] and dst not in all_route and dst not in special and key(dst) not in walls:
                    wind.append((abs(i-len(route)//2),i,src,dst))
        if not wind:failed.append(l['n']);continue
        _,wind_step,src,dst=min(wind)
        item['stormWind']={'trigger':'first_delivery','from':list(src),'to':list(dst)}
        special|={src,dst};info.update(windFrom=list(src),windTo=list(dst),windRouteStep=wind_step)
    if pattern in (1,3):
        before=set(route[:first+1]);after=set(route[first+1:]);zones=[]
        for x in range(l['grid']-1):
          for y in range(l['grid']-1):
            zone={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
            if zone&after or zone&special or any(key(p) in walls for p in zone):continue
            adjacent=sum(any(abs(p[0]-q[0])+abs(p[1]-q[1])==1 for p in zone) for q in route[first+1:])
            if adjacent>=2:zones.append(((bool(zone&before),adjacent),(x,y),zone))
        if not zones:failed.append(l['n']);continue
        _,origin,zone=max(zones,key=lambda v:v[0])
        stages=sorted(zone,key=lambda p:(p not in before,p[1],p[0]))
        item['shadowSpawner']={'trigger':'first_delivery','origin':list(origin),'stages':[list(p) for p in stages],
                               'growthTurns':[0,3,6],'influence':'2x2'}
        special|=zone;info.update(spawnerOrigin=list(origin),stageCells=[list(p) for p in stages])
    if pattern in (1,2,3):
        source_idx=next(i for i,h in enumerate(l['homes']) if tuple(h['p'])==route[first])
        before=set(route[:first+1]);suffix=route[first+1:]
        relay=[(abs(i-(first+6)),i,p) for i,p in enumerate(route) if i>first+1 and p not in before
               and p not in special and suffix.count(p)==1]
        if not relay:failed.append(l['n']);continue
        _,relay_step,relay_tile=min(relay)
        item['lumenNetwork']={'sourceHouseIndex':source_idx,'relayTile':list(relay_tile),'charge':2,'sealedUntilSource':True}
        special.add(relay_tile);info.update(sourceHouseIndex=source_idx,relayTile=list(relay_tile),relayStep=relay_step)
    if pattern in (0,3):
        before=set(route[:first+1]);suffix=route[first+1:]
        dusk=[(abs(i-len(route)*.65),i,p) for i,p in enumerate(route) if i>first+2 and p not in before
              and p not in special and suffix.count(p)==1]
        if not dusk:failed.append(l['n']);continue
        _,dusk_step,dusk_tile=min(dusk)
        paid=d['finishLight']>=1
        if not paid:
            off=[(abs(x-dusk_tile[0])+abs(y-dusk_tile[1]),(x,y)) for x in range(l['grid']) for y in range(l['grid'])
                 if (x,y) not in set(route) and (x,y) not in special and key((x,y)) not in walls]
            if not off:failed.append(l['n']);continue
            _,dusk_tile=min(off)
        item['nightfall']={'trigger':'first_delivery','tile':list(dusk_tile),'extraLight':1,'fogRadius':3}
        special.add(dusk_tile);info.update(duskTile=list(dusk_tile),duskOnRoute=paid,
                                           finishLightAfterDusk=d['finishLight']-int(paid))
    if pattern==2:
        all_base=set(base_route);candidates=[]
        for i,p in enumerate(route[first+1:],first+1):
            if p not in all_base and p not in special and key(p) not in walls:
                candidates.append((0,abs(i-(first+8)),p))
        if not candidates:
            for x in range(l['grid']):
              for y in range(l['grid']):
                p=(x,y)
                if p not in all_base and p not in special and key(p) not in walls:
                    distance=min(abs(x-q[0])+abs(y-q[1]) for q in base_route[first+1:])
                    if distance<=2:candidates.append((1,distance,p))
        if not candidates:failed.append(l['n']);continue
        _,_,alternate=min(candidates)
        signal_cost=int(d['steps']>base['steps'])
        if any(s['light']<=signal_cost for s in base['route'][:-1]) or base['route'][-1]['light']<signal_cost:
            failed.append(l['n']);continue
        item['phaseChoice']={'decision':'depot_signal_before_first_delivery','signalLightCost':signal_cost,
                             'defaultClose':l['authoredEvent']['tile'],'alternateClose':list(alternate)}
        info.update(alternateClose=list(alternate),signalSteps=base['steps'],signalLightCost=signal_cost,
                    signalFinishLight=base['route'][-1]['light']-signal_cost,signalSecondDeliveryStep=base_second)
    item['masteryArchetype']=names[pattern]
    item['brief']=f"Light all {l['required']} houses. {briefs[pattern]} Two patrols and an Echo Shadow watch the streets."+(" A free repair connects the districts." if l.get('repairRequired') else '')
    authored.append(item);evidence.append(info)
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
runs=[]
for item in authored:
    if runs and runs[-1][0]==item['masteryArchetype']:runs[-1][1]+=1
    else:runs.append([item['masteryArchetype'],1])
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed,
    'staggered':args.stagger,'maxConsecutiveArchetype':max(n for _,n in runs),
    'archetypes':{name:sum(e['archetype']==name for e in evidence) for name in names}},indent=2),encoding='utf-8')
print(f'Mastery maps {len(authored)}/100; failed={failed}; patterns={[sum(e["archetype"]==name for e in evidence) for name in names]}')
