"""Check patrol-position gates on all authored Shadow Door routes."""
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import replay,key

parser=argparse.ArgumentParser()
parser.add_argument('--solutions',type=Path,default=ROOT/'design'/'map-solutions-1000.json')
parser.add_argument('--base',type=Path,default=ROOT/'campaign'/'enhanced'/'shadow-doors-v1')
args=parser.parse_args()
BASE=args.base
levels=json.loads((BASE/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((BASE/'route_proofs.json').read_text(encoding='utf-8'))
entries=json.loads(args.solutions.read_text(encoding='utf-8'))['levels']
assert len(levels)==len(proofs)==100
assert [l['n'] for l in levels]==list(range(601,701))
for l,proof in zip(levels,proofs):
    n=l['n'];assert proof['level']==n
    sol=entries[n-1]['solutions'][0]
    states=sol['route'];points=[s['p'] for s in states]
    i=proof['doorEntryStep'];assert points[i]==l['shadowDoor']==proof['door']
    assert points.count(l['shadowDoor'])==1
    assert l['shadowLock']==proof['lock'] and l['lockPatrol']==proof['patrol']
    assert key(l['shadowDoor']) not in l['walls']
    patrol=l['patrol'] if l['lockPatrol']==1 else l['patrol2']
    phase=states[i-1]['phase' if l['lockPatrol']==1 else 'phase2']
    assert patrol[phase]==l['shadowLock']
    assert states[i-1]['active']
    checked=replay(l,points,sol['repairPurchased'])
    assert len(checked)-1==proof['referenceSteps']
    assert checked[-1]['mask'].bit_count()>=l['required']
print('PASS: 100 Shadow Doors open at the required patrol position on archived completion routes.')
