"""Find route-preserving bridge positions with room for a one-way house dogleg."""
from collections import Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
line=next(line for line in (ROOT/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if line.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2]);archive=json.loads((ROOT/'design/map-solutions-1000.json').read_text(encoding='utf-8'))['levels']
def neighbors(p):
    x,y=p;return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
rows=[]
for number in range(701,801):
    level=levels[number-1];states=archive[number-1]['solutions'][0]['route']
    points=[tuple(s['p']) for s in states];route=set(points);counts=Counter(points)
    homes={tuple(h['p']) for h in level['homes']}
    protected={tuple(level['depot'])}|homes|set(map(tuple,level['patrol']))|set(map(tuple,level.get('patrol2',[])))
    protected|={tuple(level[k]) for k in ('fade','ice','dark','switch','gate') if level.get(k)}
    if level.get('repair'):protected.add(tuple(level['repair']['tile']))
    first=next(i for i,s in enumerate(states) if s['mask'])
    options=[]
    for index in range(first+2,len(points)-5):
        bridge=points[index];v=points[index+1]
        if bridge in protected or counts[bridge]!=1 or min(s['light'] for s in states[index:])<2:continue
        if states[index]['mask']==(1<<len(homes))-1:continue
        dx,dy=v[0]-bridge[0],v[1]-bridge[1]
        if abs(dx)+abs(dy)!=1:continue
        for sign in (1,-1):
            ox,oy=dy*sign,-dx*sign;u=(bridge[0]+ox,bridge[1]+oy);w=(v[0]+ox,v[1]+oy)
            if not all(0<=p[0]<level['grid'] and 0<=p[1]<level['grid'] for p in (u,w)):continue
            if u in route or w in route or u in protected or w in protected:continue
            seals=[p for p in neighbors(u) if p not in (bridge,w)]
            if any(p in route or p in protected for p in seals):continue
            options.append({'bridge':list(bridge),'step':index,'houseSpur':list(u),'oneWayExit':list(w),'seal':[list(p) for p in seals]})
    rows.append({'level':number,'options':options})
output=Path(__file__).with_name('relocated_dogleg_screen.json')
output.write_text(json.dumps({'scope':'Geometry only; powered route, light and shadows unverified.','rows':rows},indent=2),encoding='utf-8')
print('Maps with structural alternatives:',sum(bool(r['options']) for r in rows),'/100')
print('No alternatives:',[r['level'] for r in rows if not r['options']])
