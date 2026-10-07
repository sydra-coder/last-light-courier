"""Find optimistic delivery tours while honoring first/second road changes.

The search is exact for its static phase graph: delivered houses may be
revisited; an unvisited house triggers the next phase when entered; the depot
ends a run. It ignores actors, lantern, timed systems and other conditional
roads; candidates must be replayed in the live runtime.
"""
from collections import deque
from pathlib import Path
import argparse,json,os

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--start',type=int,default=1001)
parser.add_argument('--end',type=int,default=1100)
parser.add_argument('--signal',action='store_true')
parser.add_argument('--allow-transit',action='store_true',help='Treat unlocked transit between marked stops as one relaxed move')
parser.add_argument('--neighbor-order',default='EWSN')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
assert 201<=args.start<=args.end<=2000
assert sorted(args.neighbor_order)==sorted('EWSN')
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])[args.start-1:args.end]
proofs={x['level']:x for x in json.loads((root/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text())}
signal_proofs={x['level']:x['solutions'][0]['route'] for x in json.loads((root/'campaign/enhanced/candidates-v3/ROUTES_1001_2000_BASELINE.json').read_text())}
normalized=json.loads((root/'campaign/enhanced/reference-hints-v1/normalized_routes.json').read_text())
normalized_signal=json.loads((root/'campaign/enhanced/reference-hints-v1/normalized_signal_routes.json').read_text())
directions={'E':(1,0),'W':(-1,0),'S':(0,1),'N':(0,-1)}

def phase_walls(level,phase,signal):
    walls={tuple(map(int,s.split(','))) for s in level['walls']}
    if level.get('repairRequired') and level.get('repair',{}).get('effect')=='open':
        walls.discard(tuple(level['repair']['tile']))
    if phase>=1:
        if level.get('authoredEvent'):
            event=level['authoredEvent']
            p=level['phaseChoice']['alternateClose'] if signal and level.get('phaseChoice') else event['tile']
            walls.add(tuple(p))
        if level.get('quakeEvent'):
            for p in level['quakeEvent']['open']:walls.discard(tuple(p))
            walls.add(tuple(level['quakeEvent']['close']))
    if phase>=2 and level.get('chainEvent'):
        for p in level['chainEvent']['open']:walls.discard(tuple(p))
        walls.add(tuple(level['chainEvent']['close']))
    return walls

def segment(level,points,walls,mask,source,target):
    start=points[source];goal=points[target]
    if start in walls or goal in walls:return None
    forbidden={points[0]} if source!=0 and target!=0 else set()
    forbidden.update(p for index,p in enumerate(points[1:],1)
                     if not mask&(1<<(index-1)) and index!=target)
    queue=deque([start]);parent={start:None};size=level['grid']
    while queue:
        current=queue.popleft()
        if current==goal:
            route=[];p=goal
            while p is not None:route.append(p);p=parent[p]
            return list(reversed(route))
        x,y=current
        neighbors=[]
        for name in args.neighbor_order:
            dx,dy=directions[name];neighbors.append((x+dx,y+dy))
        if args.allow_transit and mask and level.get('transitLink'):
            a,b=map(tuple,level['transitLink']['stops'])
            if current==a:neighbors.append(b)
            elif current==b:neighbors.append(a)
        for p in neighbors:
            if 0<=p[0]<size and 0<=p[1]<size and p not in walls and p not in forbidden and p not in parent:
                parent[p]=current;queue.append(p)
    return None

def solve(level,signal):
    points=[tuple(level['depot']),*[tuple(h['p']) for h in level['homes']]]
    count=len(points)-1;full=(1<<count)-1
    walls_by_phase=[phase_walls(level,phase,signal) for phase in (0,1,2)]
    segments={}
    def leg(mask,source,target):
        key=(mask,source,target)
        if key not in segments:
            segments[key]=segment(level,points,walls_by_phase[min(mask.bit_count(),2)],mask,source,target)
        return segments[key]
    best={(0,0):0};parent={}
    for mask in range(full+1):
        for source in range(count+1):
            current=best.get((mask,source))
            if current is None or (source==0 and mask):continue
            for target in range(1,count+1):
                bit=1<<(target-1)
                if mask&bit:continue
                path=leg(mask,source,target)
                if not path:continue
                newmask=mask|bit;cost=current+len(path)-1
                key=(newmask,target)
                if cost<best.get(key,10**9):best[key]=cost;parent[key]=(mask,source)
    choices=[]
    for source in range(1,count+1):
        path=leg(full,source,0)
        if (full,source) in best and path:choices.append((best[(full,source)]+len(path)-1,source))
    if not choices:return None
    steps,last=min(choices)
    order=[];mask=full;source=last
    while source:
        order.append(source);mask,source=parent[(mask,source)]
    order=[0,*reversed(order),0]
    route=[points[0]]
    mask=0
    for index,(a,b) in enumerate(zip(order,order[1:])):
        route.extend(leg(mask,a,b)[1:])
        if b:mask|=1<<(b-1)
    assert len(route)-1==steps
    return steps,[list(p) for p in route],order

rows=[]
for level in levels:
    n=level['n']
    if args.signal and not level.get('phaseChoice'):continue
    result=solve(level,args.signal)
    # Compare default tours with the currently promoted, state-normalized route.
    # The old post-event archive can be much longer than a certified live route.
    reference=len(normalized_signal[str(n)])-1 if args.signal else len(normalized[n-201])-1
    rows.append({'level':n,'verifiedRouteSteps':reference,
                 'eventAwareSteps':result[0] if result else None,
                 'staticCandidateRoute':result[1] if result else None,
                 'order':result[2] if result else None})
output=args.output or root/f'campaign/enhanced/event-aware-{args.start}-{args.end}{"-signal" if args.signal else ""}.json'
output.write_text(json.dumps({'scope':'Exact static phase tour with delivery-triggered roads; ignores actors, light, timers and other conditional road rules.',
                              'levels':len(rows),'candidates':sum(r['staticCandidateRoute'] is not None for r in rows),
                              'shorterGeometry':sum(r['eventAwareSteps'] is not None and r['eventAwareSteps']<r['verifiedRouteSteps'] for r in rows),
                              'rows':rows},indent=2))
print(json.dumps({'output':str(output),'levels':len(rows),'candidates':sum(r['staticCandidateRoute'] is not None for r in rows),
                  'shorterGeometry':sum(r['eventAwareSteps'] is not None and r['eventAwareSteps']<r['verifiedRouteSteps'] for r in rows)}))
