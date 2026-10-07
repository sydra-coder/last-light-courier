"""Find optional Decoy Light placements that redirect patrols safely."""
from pathlib import Path
import json
import argparse

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design/map-solutions-1000.json')
parser.add_argument('--out',type=Path,default=ROOT/'campaign/enhanced/decoys-v1')
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][150:200]
proofs=[];failed=[]
def nearest_target(patrol,tile):
    return min(range(len(patrol)),key=lambda i:(abs(patrol[i][0]-tile[0])+abs(patrol[i][1]-tile[1]),i))
def next_phase(phase,patrol,target,redirect):
    if not redirect:return (phase+1)%len(patrol)
    if phase==target:return phase
    cw=(target-phase+len(patrol))%len(patrol)
    ccw=(phase-target+len(patrol))%len(patrol)
    return (phase+(1 if cw<=ccw else -1))%len(patrol)
for entry in entries:
    level=entry['map'];solution=entry['solutions'][0];route=solution['route']
    trigger=next(i for i,s in enumerate(route) if s['mask'])
    walls=set(level['walls'])
    special={tuple(level[k]) for k in ('depot','fade','ice','dark','switch','gate') if level.get(k)}
    special.update(tuple(h['p']) for h in level['homes'])
    if level.get('repair'):special.add(tuple(level['repair']['tile']))
    choices=[]
    for use in range(trigger,len(route)-5):
        pos=route[use]['p']
        for dx in range(-2,3):
          for dy in range(-2,3):
            if not 0<abs(dx)+abs(dy)<=2:continue
            tile=(pos[0]+dx,pos[1]+dy)
            if not(0<=tile[0]<level['grid'] and 0<=tile[1]<level['grid']):continue
            if tile in special or f'{tile[0]},{tile[1]}' in walls:continue
            patrols=[(1,level['patrol'],route[use]['phase'])]
            if level.get('patrol2'):patrols.append((2,level['patrol2'],route[use]['phase2']))
            pick=min(patrols,key=lambda v:(abs(v[1][v[2]][0]-tile[0])+abs(v[1][v[2]][1]-tile[1]),v[0]))
            chosen=pick[0];target=nearest_target(pick[1],tile)
            phases={1:route[use]['phase'],2:route[use]['phase2']}
            changed=False;valid=True
            for t in range(use+1,len(route)):
                p=route[t]['p'];age=t-use;active=age<=4
                nxt={}
                for idx,patrol,_ in patrols:
                    ph=phases[idx]
                    new=next_phase(ph,patrol,target,active and idx==chosen)
                    if p==patrol[ph] or p==patrol[new]:valid=False;break
                    nxt[idx]=new
                    if active and idx==chosen and new!=(ph+1)%len(patrol):changed=True
                if not valid:break
                phases.update(nxt)
            if valid and changed:choices.append((abs(use-(trigger+5)),use,tile,chosen,target))
    if not choices:
        failed.append(level['n']);continue
    _,use,tile,chosen,target=min(choices)
    proofs.append({'level':level['n'],'useAfterStep':use,'decoyTile':list(tile),'selectedPatrol':chosen,
                   'targetPhase':target,'durationMoves':4,'referenceSteps':solution['steps'],
                   'finishLight':route[-1]['light']})
(OUT/'power_proofs.json').write_text(json.dumps(proofs,separators=(',',':')),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps({'attempted':50,'proofs':len(proofs),'failed':failed},indent=2),encoding='utf-8')
print(f'Decoy demonstration proofs {len(proofs)}/50; failed={failed}')
