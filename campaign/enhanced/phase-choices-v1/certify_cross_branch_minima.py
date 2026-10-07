"""Extend signal certificates where a full replay meets the relaxed tour bound."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
enhanced=here.parent
path=here/'exact_signal_minima.json'
existing=json.loads(path.read_text(encoding='utf-8'))
cross={row['level']:row for row in json.loads((here/'cross_branch_routes.json').read_text(encoding='utf-8'))}
signals=json.loads((enhanced/'reference-hints-v1/normalized_signal_routes.json').read_text(encoding='utf-8'))
new=[]
for n in (1807,1828,1994):
    replay=cross[n]['defaultRouteUnderSignal']
    bound=json.loads((here/f'relaxed-signal-{n}.json').read_text(encoding='utf-8'))['rows'][0]['eventAwareSteps']
    assert replay['completed'] and replay['steps']==bound==len(signals[str(n)])-1
    new.append({'level':n,'exactSignalSteps':bound,'freeRepairRequired':False,
                'signalLightCost':0,'finishLight':replay['finishLight'],
                'proof':'signaled full-rule replay equals relaxed phase-aware road tour bound'})
certified={item['level']:item for item in existing['certified']}
certified.update({item['level']:item for item in new})
existing['certified']=[certified[n] for n in sorted(certified)]
existing['scope']='Exact signal-branch step minima under selected first-delivery closure, certified where full-rule completion equals relaxed phase-aware road tour bound. Required free repair is included where stated.'
path.write_text(json.dumps(existing,indent=2),encoding='utf-8')
print(json.dumps(new))
