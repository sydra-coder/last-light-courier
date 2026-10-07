"""Certify exact transit step minima from replayed routes and relaxed tours."""
from pathlib import Path
import json, os, subprocess, sys

root=Path(__file__).resolve().parents[3]
here=Path(__file__).resolve().parent
preview=Path(os.environ.get('LLC_PREVIEW_PATH',root/'design/campaign-2000-preview/index.html'))
line=next(s for s in preview.open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
proofs=json.loads((here/'express_routes.json').read_text())
assert {p['level'] for p in proofs}=={1708,1711,1716,1775,1793}
certified=[]
for proof in proofs:
    n=proof['level'];level=levels[n-1]
    assert level['required']==len(level['homes']) and level.get('transitLink')
    assert level.get('authoredEvent',{}).get('kind')=='road_close' and level['authoredEvent'].get('trigger')=='first_delivery'
    assert not any(level.get(k) for k in ('hiddenRoad','lightBridge','chainEvent','quakeEvent','phaseChoice','networkCircuitRequired'))
    assert bool(level.get('repairRequired'))==proof['freeRepairRequired']
    output=here/f'relaxed-{n}.json'
    subprocess.run([sys.executable,str(root/'campaign/enhanced/audit_event_aware_tours.py'),
                    '--start',str(n),'--end',str(n),'--allow-transit','--output',str(output)],
                   check=True,capture_output=True,text=True)
    bound=json.loads(output.read_text())['rows'][0]['eventAwareSteps']
    assert bound==proof['transitSteps']==len(proof['route'])-1,(n,bound,proof['transitSteps'])
    assert any(abs(a[0]-b[0])+abs(a[1]-b[1])>1 for a,b in zip(proof['route'],proof['route'][1:]))
    certified.append({'level':n,'exactSteps':bound,'freeRepairRequired':proof['freeRepairRequired'],
                      'finishLight':proof['transitFinishLight'],'walkingSteps':proof['walkingSteps'],
                      'proof':'live transit completion equals relaxed delivery-phase road tour with unlocked transit edges'})
(here/'exact_transit_minima.json').write_text(json.dumps({
    'scope':'Exact no-power transit-inclusive step minima; level 1775 includes its mandatory free repair. Runtime routes were replayed and equal freshly generated relaxed road bounds with transit unlocked after first delivery.',
    'certified':certified},indent=2))
print(json.dumps(certified))
