"""Find safe use points for optional Freeze Seal and Rewind loadouts."""
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/arsenal-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((args.road_events/'authored_levels.json').read_text(encoding='utf-8'))[400:500]
routes=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[400:500]
proofs=[];failed=[]
for level,record in zip(levels,routes):
    assert level['n']==record['level']
    steps=record['route'];trigger=record['triggerStep']
    power='freeze_seal' if level['n']%2 else 'rewind'
    if power=='rewind':
        assert steps[trigger]['mask'] and not steps[trigger-1]['mask']
        proofs.append({'level':level['n'],'power':power,'useAfterStep':trigger,
                       'restoresStep':trigger-1,'replaySteps':record['steps'],'finishLight':record['finishLight']})
        continue
    candidates=[]
    for use in range(trigger,len(steps)-4):
        okay=True;phase1=steps[use]['phase'];phase2=steps[use]['phase2']
        for t in range(use+1,len(steps)):
            p=steps[t]['p']
            frozen=t<=use+3
            ph1=phase1 if frozen else (steps[t-1]['phase']-3)%len(level['patrol'])
            ph2=phase2 if frozen else (steps[t-1]['phase2']-3)%len(level['patrol2'])
            for patrol,ph in ((level['patrol'],ph1),(level['patrol2'],ph2)):
                if patrol and (p==patrol[ph] or not frozen and p==patrol[(ph+1)%len(patrol)]):
                    okay=False;break
            if not okay:break
        if okay:candidates.append(use)
    if not candidates:
        failed.append(level['n']);continue
    use=min(candidates,key=lambda i:(abs(i-(trigger+6)),i))
    proofs.append({'level':level['n'],'power':power,'useAfterStep':use,'frozenMoves':[use+1,use+2,use+3],
                   'replaySteps':record['steps'],'finishLight':record['finishLight']})
(OUT/'power_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':100,'proofs':len(proofs),'failedFreezeLevels':failed},indent=2),encoding='utf-8')
print(f'Power-use proofs {len(proofs)}/100; missing freeze={failed}')
