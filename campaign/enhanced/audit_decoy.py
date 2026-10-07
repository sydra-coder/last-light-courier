"""Check all authored Decoy Light placements and resulting patrol phases."""
from pathlib import Path
import json
import argparse
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design/map-solutions-1000.json')
parser.add_argument('--proofs',type=Path,default=ROOT/'campaign/enhanced/decoys-v1/power_proofs.json')
args=parser.parse_args()
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels'][150:200]
proofs=json.loads(args.proofs.read_text(encoding='utf-8'))
assert len(entries)==len(proofs)==50
for entry,proof in zip(entries,proofs):
    l=entry['map'];route=entry['solutions'][0]['route'];use=proof['useAfterStep'];tile=proof['decoyTile']
    assert l['n']==proof['level'] and route[use]['active']
    assert 0<sum(abs(a-b) for a,b in zip(tile,route[use]['p']))<=2
    assert f'{tile[0]},{tile[1]}' not in l['walls']
    patrols=[(1,l['patrol'],route[use]['phase'])]
    if l.get('patrol2'):patrols.append((2,l['patrol2'],route[use]['phase2']))
    chosen=min(patrols,key=lambda v:(sum(abs(a-b) for a,b in zip(v[1][v[2]],tile)),v[0]))
    assert chosen[0]==proof['selectedPatrol']
    target=min(range(len(chosen[1])),key=lambda i:(sum(abs(a-b) for a,b in zip(chosen[1][i],tile)),i))
    assert target==proof['targetPhase'] and proof['durationMoves']==4
    phases={1:route[use]['phase'],2:route[use]['phase2']};changed=False
    for t in range(use+1,len(route)):
        p=route[t]['p'];active=t-use<=4
        for idx,patrol,_ in patrols:
            phase=phases[idx]
            if active and idx==chosen[0] and phase!=target:
                cw=(target-phase+len(patrol))%len(patrol)
                ccw=(phase-target+len(patrol))%len(patrol)
                nxt=(phase+(1 if cw<=ccw else -1))%len(patrol)
            elif active and idx==chosen[0]:nxt=phase
            else:nxt=(phase+1)%len(patrol)
            assert p!=patrol[phase] and p!=patrol[nxt],(l['n'],t)
            if active and idx==chosen[0] and nxt!=(phase+1)%len(patrol):changed=True
            phases[idx]=nxt
    assert changed and route[-1]['p']==l['depot'] and route[-1]['light']>=0
print('50 Decoy Light placements redirect a patrol and preserve completion route')
