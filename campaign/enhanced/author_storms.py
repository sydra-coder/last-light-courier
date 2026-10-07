"""Place deterministic wind-shifted blockers on Storm March maps 1001–1100."""
from pathlib import Path
import argparse,json

ROOT = Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/storms-v1')
args=parser.parse_args()
OUT = args.out
OUT.mkdir(parents=True, exist_ok=True)
levels = json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[:100]
proofs = json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[:100]
authored, evidence, failed = [], [], []
for level, proof in zip(levels, proofs):
    assert level['n'] == proof['level']
    route = [tuple(s['p']) for s in proof['route']]
    trigger = proof['triggerStep']
    before = set(route[:trigger+1])
    after = set(route[trigger+1:])
    all_route = set(route)
    walls = set(level['walls'])
    special = {tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    special.add(tuple(level['authoredEvent']['tile']))
    if level.get('repair'): special.add(tuple(level['repair']['tile']))
    choices = []
    for index in range(trigger+2, len(route)-2):
        src = route[index]
        if src in before or src in special or src not in after: continue
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            dst = (src[0]+dx, src[1]+dy)
            if not (0 <= dst[0] < level['grid'] and 0 <= dst[1] < level['grid']): continue
            if dst in all_route or dst in special or f'{dst[0]},{dst[1]}' in walls: continue
            choices.append((abs(index-len(route)//2), index, src, dst))
    if not choices:
        failed.append(level['n']); continue
    _,index,src,dst = min(choices)
    item = dict(level)
    item['stormWind'] = {'trigger':'first_delivery','from':list(src),'to':list(dst)}
    item['brief'] = level['brief']+' The first delivery shifts a windblown roadblock to an adjacent street.'
    authored.append(item)
    evidence.append({'level':level['n'],'triggerStep':trigger,'blockerFrom':list(src),'blockerTo':list(dst),
                     'freedRoadFirstUsedStep':index,'postEventSteps':proof['steps'],'finishLight':proof['finishLight']})
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(evidence,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'authored':len(authored),'failed':failed},indent=2),encoding='utf-8')
print(f'Storm wind authored {len(authored)}/100; failed={failed}')
