"""Combine fully replayed closure candidates for a single campaign stage."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
root=here.parent
stage=here/'four-choice-promotion-stage'
stage.mkdir(exist_ok=True)
events=json.loads((root/'house-order-screen-v1/event_tiles.json').read_text())
routes=json.loads((root/'reference-hints-v1/route_overrides.json').read_text())
promoted=[]
for n in (1807,1828,1980,1994):
    result=json.loads((here/f'level-{n}-choice-screen.json').read_text())
    index=result['winner']
    assert index is not None
    replay=result['attempts'][index]
    assert replay['default']['completed'] and replay['signal']['completed']
    assert replay['default']['steps']>replay['signal']['steps']
    item=json.loads((here/f'level-{n}-choice-candidates.json').read_text())['candidates'][index]
    events[str(n)]=item['close']
    routes[str(n)]=item['route']
    promoted.append({'level':n,'closure':item['close'],'defaultSteps':replay['default']['steps'],
                     'defaultFinishLight':replay['default']['light'],
                     'signalSteps':replay['signal']['steps'],'signalFinishLight':replay['signal']['light']})
(stage/'event_tiles.json').write_text(json.dumps(events))
(stage/'route_overrides.json').write_text(json.dumps(routes))
(stage/'choices.json').write_text(json.dumps(promoted,indent=2))
print(json.dumps(promoted))
