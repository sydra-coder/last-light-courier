"""Independently replay the shortened final leg after each transit ride."""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--road-events',type=Path,default=ROOT/'campaign/enhanced/road-events-v1')
parser.add_argument('--transit',type=Path,default=ROOT/'campaign/enhanced/transit-v1')
args=parser.parse_args()
levels=json.loads((args.transit/'authored_levels.json').read_text(encoding='utf-8'))
base=json.loads((args.road_events/'post_event_routes.json').read_text(encoding='utf-8'))[700:800]
proofs=json.loads((args.transit/'route_proofs.json').read_text(encoding='utf-8'))
assert len(levels)==len(base)==len(proofs)==100
for l,b,r in zip(levels,base,proofs):
    assert l['n']==b['level']==r['level']
    i=r['boardAtStep'];j=r['exitAtOldStep'];a,exit_tile=r['stops']
    old=b['route'];assert old[i]['p']==a and old[j]['p']==exit_tile
    assert i>=r['lastHouseStep'] and j-i-1==r['stepsSaved']>=9
    assert sum(abs(x-y) for x,y in zip(a,exit_tile))>=4
    assert r['walkingSteps']==b['steps'] and r['transitSteps']==b['steps']-r['stepsSaved']
    assert l['transitLink']['stops']==r['stops'] and l['transitLink']['rideLight']==2
    s=dict(old[i]);assert s['active'] and s['mask']!=0
    suffix=[exit_tile]+[record['p'] for record in old[j+1:]]
    walls=set(l['walls'])
    if l.get('repairRequired') and l.get('repair') and l['repair']['effect']=='open':
        walls.discard(f"{l['repair']['tile'][0]},{l['repair']['tile'][1]}")
    for step,p in enumerate(suffix):
        previous=s['p']
        if step>0:assert sum(abs(x-y) for x,y in zip(previous,p))==1,(l['n'],step)
        assert f'{p[0]},{p[1]}' not in walls and p!=l['authoredEvent']['tile'],(l['n'],step)
        assert not(p==l['fade'] and s['fade']==0 or p==l['ice'] and s['ice']==0),(l['n'],step,'crossing')
        assert p!=l['gate'] or s['gate']>0 or l.get('repairRequired') and l['repair']['effect']=='latch'
        for patrol,phase in ((l['patrol'],s['phase']),(l['patrol2'],s['phase2'])):
            if patrol:assert p!=patrol[phase] and p!=patrol[(phase+1)%len(patrol)],(l['n'],step,'shadow')
        if l['echo']:assert p not in s['trail'],(l['n'],step,'Echo')
        cost=2 if step==0 or p==l['dark'] and not(l.get('repairRequired') and l['repair']['effect']=='lamp') else 1
        light=s['light']-cost
        final=step==len(suffix)-1
        assert light>0 or final and p==l['depot'],(l['n'],step,'light')
        s={'p':p,'mask':s['mask'],'light':light,'active':True,
           'phase':(s['phase']+1)%len(l['patrol']),
           'phase2':(s['phase2']+1)%len(l['patrol2']) if l['patrol2'] else s['phase2'],
           'fade':5 if p==l['fade'] and s['fade'] is None else None if s['fade'] is None else max(0,s['fade']-1),
           'ice':4 if p==l['ice'] and s['ice'] is None else None if s['ice'] is None else max(0,s['ice']-1),
           'gate':4 if p==l['switch'] else max(0,s['gate']-1),
           'trail':(s['trail'][-1:]+[previous]) if l['echo'] else []}
    assert s['p']==l['depot'] and s['light']==r['transitFinishLight'] and s['mask'].bit_count()>=l['required']
print('100 transit rides replay from boarding stop through safe return; walking routes remain available')
