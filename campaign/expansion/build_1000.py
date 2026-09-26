"""Deterministic expansion; preserves 001-200 and verifies reference routes under live rules."""
from pathlib import Path
from collections import deque, Counter
import random, json, hashlib, csv
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(r'C:\Users\rahul\Documents\Codex\2026-09-25\last-light-courier\outputs')
key=lambda p: ','.join(map(str,p))
def adjacent(p):
    x,y=p
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
def replay(l,route,bought=False):
    walls=set(l['walls'])
    r=l['repair']
    if bought and r and r['effect']=='open': walls.discard(key(r['tile']))
    cap=l['cap']+(3 if bought and r and r['effect']=='beacon' else 0)
    s=dict(p=l['depot'],mask=0,light=cap,phase=l['phase'],phase2=l['phase2'],active=False,fade=None,ice=None,gate=0,trail=[])
    records=[dict(s)]
    for t,p in enumerate(route[1:],1):
        assert tuple(p) in adjacent(s['p']), (l['n'],t,'not adjacent')
        assert 0<=p[0]<l.get('grid',8) and 0<=p[1]<l.get('grid',8) and key(p) not in walls,(l['n'],t,'wall')
        assert not (p==l['fade'] and s['fade']==0 or p==l['ice'] and s['ice']==0),(l['n'],t,'crossing')
        assert p!=l['gate'] or s['gate']>0 or bought and r['effect']=='latch',(l['n'],t,'gate')
        if s['active']:
            for patrol,ph in [(l['patrol'],s['phase']),(l['patrol2'],s['phase2'])]:
                if patrol: assert p not in [patrol[ph],patrol[(ph+1)%len(patrol)]],(l['n'],t,'patrol')
            assert not l['echo'] or p not in s['trail'],(l['n'],t,'echo')
        idx=next((i for i,h in enumerate(l['homes']) if h['p']==p),-1)
        fresh=idx>=0 and not s['mask']&(1<<idx)
        mask=s['mask']|(1<<idx if idx>=0 else 0)
        home=p==l['depot'] and mask
        light=min(cap,s['light']-(2 if p==l['dark'] and not(bought and r and r['effect']=='lamp') else 1)+(2 if fresh else 0))
        assert light>0 or fresh or home,(l['n'],t,'lantern')
        assert not home or t==len(route)-1,(l['n'],t,'early bank')
        s=dict(p=p,mask=mask,light=light,phase=(s['phase']+1)%len(l['patrol']) if s['active'] else s['phase'],phase2=(s['phase2']+1)%len(l['patrol2']) if s['active'] and l['patrol2'] else s['phase2'],active=s['active'] or fresh,
            fade=5 if p==l['fade'] and s['fade'] is None else None if s['fade'] is None else max(0,s['fade']-1),ice=4 if p==l['ice'] and s['ice'] is None else None if s['ice'] is None else max(0,s['ice']-1),gate=4 if p==l['switch'] else max(0,s['gate']-1),trail=(s['trail'][-1:]+[s['p']]) if l['echo'] else [])
        records.append(dict(s))
    assert s['p']==l['depot'] and s['mask'].bit_count()>=l['required'] and s['light']>=0,(l['n'],'not complete')
    return records
def metrics(l,repaired=False):
    size=l.get('grid',8);walls=set(l['walls'])
    if repaired and l['repair'] and l['repair']['effect']=='open': walls.discard(key(l['repair']['tile']))
    opened={(x,y) for y in range(size) for x in range(size) if key((x,y)) not in walls}
    degree={p:sum(q in opened for q in adjacent(p)) for p in opened}
    components=0;seen=set()
    for p in opened:
        if p in seen:continue
        components+=1;todo=[p];seen.add(p)
        while todo:
            for q in adjacent(todo.pop()):
                if q in opened and q not in seen:seen.add(q);todo.append(q)
    return dict(openTiles=len(opened),blockedPercent=round(100*len(walls)/size**2,1),junctions=sum(d>=3 for d in degree.values()),loops=sum(degree.values())//2-len(opened)+components,components=components)
def reachable(l,bought):
    walls=set(l['walls'])
    if bought:walls.discard(key(l['repair']['tile']))
    size=l['grid'];seen={tuple(l['depot'])};todo=list(seen)
    while todo:
        for q in adjacent(todo.pop()):
            if 0<=q[0]<size and 0<=q[1]<size and key(q) not in walls and q not in seen:seen.add(q);todo.append(q)
    return sum(tuple(h['p']) in seen for h in l['homes'])
def tighten_reference(l,route,bought,rng):
    """Find legal local shortcuts, then budget light against that improved route."""
    walls=set(l['walls'])
    if bought:walls.discard(key(l['repair']['tile']))
    protected={tuple(l['depot']),*map(lambda h:tuple(h['p']),l['homes'])}
    protected.update(tuple(l[f]) for f in ['switch','gate','fade','ice','dark'] if l[f])
    for iteration in range(8):
        candidates=[]
        for i in range(len(route)-4):
            for j in range(i+4,min(i+18,len(route))):
                if any(tuple(p) in protected for p in route[i+1:j]):break
                a,b=route[i],route[j];distance=abs(a[0]-b[0])+abs(a[1]-b[1]);saved=j-i-distance
                if saved>0 and saved%4==0:candidates.append((saved,i,j))
        rng.shuffle(candidates);candidates.sort(reverse=True);changed=False
        for _,i,j in candidates[:30]:
            for vertical in [False,True]:
                short=[route[i][:]];target=route[j]
                for axis in ([1,0] if vertical else [0,1]):
                    while short[-1][axis]!=target[axis]:
                        p=short[-1][:];p[axis]+=1 if target[axis]>p[axis] else -1;short.append(p)
                if any(key(p) in walls or tuple(p) in protected for p in short[1:-1]):continue
                trial=route[:i]+short+route[j+1:]
                try:replay(l,trial,bought)
                except AssertionError:continue
                route=trial;changed=True;break
            if changed:break
        if not changed:break
    oldcap=l['cap'];l['cap']=len(route)-1+sum(p==l['dark'] for p in route[1:])-2*len(l['homes'])+l['referenceMargin']
    try:records=replay(l,route,bought)
    except AssertionError:l['cap']=oldcap;records=replay(l,route,bought)
    l['spine']=route;l['referenceMethod']='Legal local shortcut search, followed by full rules replay; not globally optimal'
    return route,records
def build(n):
    rng=random.Random(n*90113);band=(n-201)//100;size=18+2*(band//2);hc=8+band//2;required=n%25==0
    if required:
        m=size//2;route=[[0,0]]
        def to(x,y):
            while route[-1][0]!=x:route.append([route[-1][0]+(1 if x>route[-1][0] else -1),route[-1][1]])
            while route[-1][1]!=y:route.append([route[-1][0],route[-1][1]+(1 if y>route[-1][1] else -1)])
        to(m-1,0);to(m-1,2);to(m+1,2);to(size-1,2);to(size-1,size-1);to(m+1,size-1);to(m+1,2);to(m-1,2);to(m-1,size-1);to(0,size-1);to(0,0)
        barrier={(m,y) for y in range(size)};repair_tile=[m,2]
    else:
        rows=list(range(1,size-1,2))
        if len(rows)%2:rows.pop()
        route=[[0,rows[0]],[1,rows[0]]];cursor=2
        for i,y in enumerate(rows):
            end=rng.randrange(size-5,size) if i%2==0 else rng.randrange(2,6)
            route.extend([[x,y] for x in (range(cursor,end+1) if i%2==0 else range(cursor,end-1,-1))])
            if i<len(rows)-1:route.append([end,y+1]);cursor=end
        route.extend([[x,rows[-1]] for x in range(route[-1][0]-1,-1,-1)])
        route.extend([[0,y] for y in range(rows[-1]-1,rows[0]-1,-1)])
        barrier=set();repair_tile=None
    # Eight board orientations, with independently generated street lengths and features.
    def tx(p):
        x,y=p
        if n%2:x=size-1-x
        if n%4<2:y=size-1-y
        if n%8<4:x,y=y,x
        return [x,y]
    route=list(map(tx,route));barrier={tuple(tx(p)) for p in barrier}
    repair_tile=tx(repair_tile) if repair_tile else None
    counts=Counter(map(tuple,route));unique=[i for i in range(3,len(route)-3) if counts[tuple(route[i])]==1]
    targets=[round(len(route)*(i+1)/(hc+1)) for i in range(hc)]
    picks=[]
    for target in targets:
        choices=[i for i in unique if i not in picks];picks.append(min(choices,key=lambda i:abs(i-target-rng.randrange(-2,3))))
    picks.sort();homes=[route[i] for i in picks];used={tuple(route[0]),*map(tuple,homes)}
    def feature(target):
        candidates=[i for i in unique if tuple(route[i]) not in used]
        idx=min(candidates,key=lambda i:abs(i-target));used.add(tuple(route[idx]));return route[idx]
    pairs=[i for i in unique if i+2<len(route) and counts[tuple(route[i+2])]==1 and tuple(route[i]) not in used and tuple(route[i+2]) not in used]
    if not pairs:return None
    si=min(pairs,key=lambda i:abs(i-(picks[0]+2)));switch=route[si];gate=route[si+2]
    used.update([tuple(switch),tuple(gate)]);fade=feature(len(route)*.4);ice=feature(len(route)*.65);dark=feature(len(route)*.8)
    activation=picks[0];squares=[]
    for y in range(size-1):
        for x in range(size-1):
            sq=[[x,y],[x+1,y],[x+1,y+1],[x,y+1]]
            if any(tuple(p) in used or tuple(p) in barrier for p in sq):continue
            overlap=sum(p in route for p in sq)
            if not overlap:continue
            for phase in range(4):
                if all(route[t] not in [sq[(phase+t-activation-1)%4],sq[(phase+t-activation)%4]] for t in range(activation+1,len(route))):
                    squares.append((overlap,sq,phase));break
    rng.shuffle(squares);squares.sort(key=lambda s:-s[0]);patrols=[]
    for _,sq,phase in squares:
        if not any(set(map(tuple,sq))&set(map(tuple,a[0])) for a in patrols):patrols.append((sq,phase))
        if len(patrols)==2:break
    if len(patrols)<2:return None
    protected=set(map(tuple,route))|set(map(tuple,patrols[0][0]+patrols[1][0]))
    alltiles={(x,y) for y in range(size) for x in range(size)}
    target=round(size*size*(.35-band*.018-((n-201)%100)/100*.012))
    options=list(alltiles-protected-barrier);options.sort();rng.shuffle(options)
    walls=set(barrier)|set(options[:max(0,target-len(barrier))])
    if not required:
        shortcuts=[p for p in walls if (p[0]-1,p[1]) in protected and (p[0]+1,p[1]) in protected or (p[0],p[1]-1) in protected and (p[0],p[1]+1) in protected]
        if not shortcuts:return None
        repair_tile=list(rng.choice(sorted(shortcuts)))
    # Connect incidental street pockets, so junction metrics reflect usable ground.
    hard=barrier-{tuple(repair_tile)} if required else {tuple(repair_tile)}
    for _ in range(size*size):
        opened=alltiles-walls
        if required:opened.add(tuple(repair_tile))
        reached={tuple(route[0])};todo=list(reached)
        while todo:
            for q in adjacent(todo.pop()):
                if q in opened and q not in reached:reached.add(q);todo.append(q)
        missing=opened-reached
        if not missing:break
        first=min(missing);queue=deque([first]);parents={first:None};join=None
        while queue and join is None:
            p=queue.popleft()
            for q in adjacent(p):
                if q not in alltiles or q in hard or q in parents:continue
                parents[q]=p
                if q in reached:join=q;break
                queue.append(q)
        assert join is not None
        while join is not None:
            if join not in barrier:walls.discard(join)
            join=parents[join]
    margin=max(1,10-band-((n-201)%100)//25)
    cost=0 if required else 25+5*band
    l=dict(n=n,chapter=(n-1)//10+1,grid=size,brief=f'Light all {hc} houses across branching streets. '+('Use the reserved free repair to connect both districts.' if required else 'Choose house order and crossing timing; repairs are optional.'),depot=route[0],homes=[dict(p=p,name=f'District {i+1}',points=600+40*band+80*i) for i,p in enumerate(homes)],walls=sorted(map(key,walls)),repair=dict(tile=repair_tile,name='Restore district connection' if required else 'Open branching shortcut',band='R',cost=cost,effect='open',stepsSaved=None),fade=fade,ice=ice,dark=dark,switch=switch,gate=gate,echo=True,patrol=patrols[0][0],phase=patrols[0][1],patrol2=patrols[1][0],phase2=patrols[1][1],cap=len(route)-1+sum(p==dark for p in route[1:])-2*hc+margin,spine=route,required=hc,bonus=1000+100*band,
           repairRequired=required,reservedFreeRepair=required,repairGemPrice=cost,difficultyBand=band+1,referenceMargin=margin,routeStatus='Verified reference route; global shortest route not claimed',economyStatus='Gem and voucher metadata follows the shop design; full shop integration remains separate')
    try:
        route,records=tighten_reference(l,route,required,rng)
        assert metrics(l,required)['junctions']>=3
        if required:assert reachable(l,False)<hc and reachable(l,True)==hc
    except AssertionError as err: print("Rejected",n,str(err),flush=True);return None
    return l,records
def main():
    base=json.loads((ROOT/'campaign/levels_001_200.snapshot.json').read_text(encoding='utf-8'));assert len(base)==200
    old=json.loads((ROOT/'design/map-solutions-200.json').read_text(encoding='utf-8'))
    entries=[]
    for l,e in zip(base,old['levels']):
        assert l==e['map'],('200-map archive differs',l['n'])
        for v in e['solutions']:replay(l,[s['p'] for s in v['route']],v['repairPurchased'])
        entries.append(e)
    levels=base[:];seen=set();failed=[]
    for n in range(201,1001):
        item=build(n)
        if not item:failed.append(n);continue
        l,route=item
        layout=json.dumps([l[x] for x in ['grid','depot','homes','walls','patrol','patrol2']])
        assert layout not in seen;seen.add(layout);l['metrics']=metrics(l,l['repairRequired']);assert l['metrics']['components']==1
        fingerprint=hashlib.sha256(json.dumps(l,sort_keys=True).encode()).hexdigest();levels.append(l)
        entries.append(dict(level=n,mapFingerprint=fingerprint,map=l,solutions=[dict(repairPurchased=l['repairRequired'],status='verified_reference',steps=len(route)-1,route=route,optimal=False)]))
        if n%100==0:print('Generated and replay-verified through',n,flush=True)
    assert not failed,failed
    assert len(levels)==1000 and all(l['n']==i+1 for i,l in enumerate(levels))
    archive=dict(schemaVersion=2,created='2026-09-26',description='001-200 retain archived shortest routes. 201-1000 include independently replay-verified reference routes; shortest routes are not claimed. Required maps need the reserved free repair. No patrol or Echo rules changed.',rulesFingerprint=hashlib.sha256((ROOT/'campaign/route-solver.js').read_bytes()).hexdigest(),levels=entries)
    (ROOT/'CAMPAIGN_1000_LEVELS.json').write_text(json.dumps(levels,separators=(',',':')),encoding='utf-8')
    (ROOT/'design/map-solutions-1000.json').write_text(json.dumps(archive,separators=(',',':')),encoding='utf-8')
    OUT.mkdir(exist_ok=True);(OUT/'Last-Light-Courier-1000-Maps.json').write_text(json.dumps(levels,separators=(',',':')),encoding='utf-8');(OUT/'Last-Light-Courier-1000-Map-Solutions.json').write_text(json.dumps(archive,separators=(',',':')),encoding='utf-8')
    with (OUT/'Last-Light-Courier-1000-Level-Metrics.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['Level','Grid','Required houses','Repair required','Free repair reserved','Gem repair proposal','Blocked %','Junctions','Independent loops','Verified reference moves','Finish light','Global shortest verified'])
        for e in entries:
            l=e['map'];m=metrics(l,l.get('repairRequired',False));v=e['solutions'][0]
            w.writerow([l['n'],l.get('grid',8),l['required'],l.get('repairRequired',False),l.get('reservedFreeRepair',False),l.get('repairGemPrice','Legacy points'),m['blockedPercent'],m['junctions'],m['loops'],v['steps'],v['route'][-1]['light'],l['n']<=200])
    print('PASS 1000 maps; 800 new unique layouts; original 200 preserved; all archived routes replayed; 32 mandatory repairs proven by disconnected required houses.',flush=True)
if __name__=='__main__':main()
