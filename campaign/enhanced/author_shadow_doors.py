"""Author timing-based Shadow Doors for levels 601–700.

The door opens only while one of the existing patrols stands on its lock tile.
Each archived reference route enters the door at such a phase.
"""
from pathlib import Path
from collections import Counter
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign'/'enhanced'/'shadow-doors-v1')
args=parser.parse_args()
OUT=args.out
OUT.mkdir(parents=True,exist_ok=True)
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][600:700]
assert [e['level'] for e in entries]==list(range(601,701))

authored=[];proofs=[]
for entry in entries:
    l=entry['map'];states=entry['solutions'][0]['route'];points=[s['p'] for s in states]
    activation=next(i for i,s in enumerate(states) if s['mask'])
    counts=Counter(map(tuple,points))
    special={tuple(l[k]) for k in ('depot','fade','ice','dark','switch','gate') if l[k]}
    special.update(tuple(h['p']) for h in l['homes'])
    if l.get('repair'):special.add(tuple(l['repair']['tile']))
    candidates=[]
    for i in range(activation+3,len(points)-5):
        tile=points[i]
        if tuple(tile) in special or counts[tuple(tile)]!=1:continue
        for patrol_number,patrol,phase_key in ((1,l['patrol'],'phase'),(2,l['patrol2'],'phase2')):
            if not patrol:continue
            lock=patrol[states[i-1][phase_key]]
            if tuple(lock) in special or lock==tile:continue
            candidates.append((abs(i-len(points)*.48),patrol_number,i,tile,lock))
    assert candidates,l['n']
    _,patrol_number,index,tile,lock=min(candidates)
    item=dict(l)
    item['shadowDoor']=tile
    item['shadowLock']=lock
    item['lockPatrol']=patrol_number
    item['brief']=l['brief']+' A Shadow Door opens only while the marked patrol stands on its lock.'
    authored.append(item)
    proofs.append({'level':l['n'],'door':tile,'lock':lock,'patrol':patrol_number,
                   'doorEntryStep':index,'referenceSteps':entry['solutions'][0]['steps']})

assert len(authored)==len(proofs)==100
(OUT/'authored_levels.json').write_text(json.dumps(authored,separators=(',',':')),encoding='utf-8')
(OUT/'route_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
print('Authored 100 timing-based Shadow Doors in levels 601–700.')
