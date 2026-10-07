"""Prove exact signal-branch steps when live completion meets relaxed phase tour."""
from pathlib import Path
import json,subprocess,sys

root=Path(__file__).resolve().parents[3]
here=Path(__file__).resolve().parent
enhanced=here.parent
line=next(s for s in (root/'design/campaign-2000-preview/index.html').open(encoding='utf-8') if s.startswith('const LEVELS='))
levels=json.loads(line[len('const LEVELS='):-2])
queue={x['level']:x for x in json.loads((enhanced/'event-aware-unresolved-shortcuts.json').read_text())['rows']}
certified=[]
for n in (1804,1900):
    level=levels[n-1]
    assert level['required']==len(level['homes']) and level.get('phaseChoice')
    assert level.get('authoredEvent',{}).get('kind')=='road_close' and level['authoredEvent'].get('trigger')=='first_delivery'
    assert not any(level.get(k) for k in ('transitLink','hiddenRoad','lightBridge','chainEvent','quakeEvent','networkCircuitRequired'))
    output=here/f'relaxed-signal-{n}.json'
    subprocess.run([sys.executable,str(enhanced/'audit_event_aware_tours.py'),
                    '--start',str(n),'--end',str(n),'--signal','--output',str(output)],
                   check=True,capture_output=True,text=True)
    bound=json.loads(output.read_text())['rows'][0]['eventAwareSteps']
    band=(n-1)//100*100+1
    replay=json.loads((enhanced/f'event-aware-{band}-{band+99}-signal-replay.json').read_text())
    completed=next(x for x in replay['completedRoutes'] if x['level']==n)
    assert completed['steps']==queue[n]['signalSteps']==bound==len(completed['route'])-1
    certified.append({'level':n,'exactSignalSteps':bound,'freeRepairRequired':bool(level.get('repairRequired')),
                      'signalLightCost':level['phaseChoice']['signalLightCost'],'finishLight':completed['finishLight'],
                      'proof':'signaled live completion equals relaxed phase-aware road tour bound'})
(here/'exact_signal_minima.json').write_text(json.dumps({
    'scope':'Exact no-power signal-branch step minima; level 1900 includes its mandatory free repair. Signal selects the alternate road closure before moving and the relaxed tour includes that closure.',
    'certified':certified},indent=2))
print(json.dumps(certified))
