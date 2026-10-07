"""Independently recheck optional power-use reference routes."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--arsenal',type=Path,default=ROOT/'campaign/enhanced/arsenal-v1')
args=parser.parse_args()
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[400:500]
routes=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[400:500]
proofs=json.loads((args.arsenal/'power_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(routes)==len(proofs)==100
for level,record,proof in zip(levels,routes,proofs):
    assert level['n']==record['level']==proof['level']
    steps=record['route'];use=proof['useAfterStep'];trigger=record['triggerStep']
    assert proof['replaySteps']==record['steps'] and proof['finishLight']==record['finishLight']
    assert all(s['p']!=level['authoredEvent']['tile'] for s in steps[trigger+1:])
    assert steps[-1]['p']==level['depot'] and steps[-1]['light']>=0
    if proof['power']=='rewind':
        assert level['n']%2==0 and use==trigger and proof['restoresStep']==trigger-1
        assert steps[use-1]['mask']==0 and steps[use]['mask']!=0
        # Rewinding restores the entire pre-delivery snapshot, including
        # mask/phase/light, so replaying the same move reaches this record.
        continue
    assert proof['power']=='freeze_seal' and level['n']%2==1
    assert use>=trigger and proof['frozenMoves']==[use+1,use+2,use+3]
    for t in range(use+1,len(steps)):
        frozen=t<=use+3;p=steps[t]['p']
        for patrol,field in ((level['patrol'],'phase'),(level['patrol2'],'phase2')):
            if not patrol:continue
            ph=steps[use][field] if frozen else (steps[t-1][field]-3)%len(patrol)
            assert p!=patrol[ph],(level['n'],t,'occupied')
            if not frozen:assert p!=patrol[(ph+1)%len(patrol)],(level['n'],t,'next')
print('100 arsenal routes pass power-use checks: 50 Freeze Seal, 50 Rewind')
