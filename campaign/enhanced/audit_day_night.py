"""Replay phase timing, moon-road entry and lantern balance on 100 routes."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'campaign/enhanced/day-night-v1'
levels=json.loads((folder/'authored_levels.json').read_text(encoding='utf-8'))
proofs=json.loads((folder/'route_proofs.json').read_text(encoding='utf-8'))
routes=json.loads((ROOT/'campaign/enhanced/road-events-v1/post_event_routes.json').read_text(encoding='utf-8'))[100:200]
assert len(levels)==len(proofs)==len(routes)==100
day_dusk=0
for level,proof,record in zip(levels,proofs,routes):
    n=level['n'];assert n==proof['level']==record['level']
    route=record['route'];trigger=record['triggerStep'];cycle=level['dayNightCycle']
    assert trigger==proof['triggerStep'] and cycle['nightMoves']==6 and cycle['dayMoves']==4
    moon=tuple(cycle['moonRoad']);assert tuple(route[proof['moonRoadStep']]['p'])==moon
    assert sum(tuple(s['p'])==moon for s in route)==1
    assert proof['moonRoadStep']>trigger+10
    assert proof['entryAge']==proof['moonRoadStep']-1-trigger
    assert proof['entryAge']%10<5  # Remains open for at least one move after entry.
    cap=level['cap']+(3 if level['repairRequired'] and level['repair']['effect']=='beacon' else 0)
    delta=0
    for i,s in enumerate(route):
        light=min(cap,s['light']+delta)
        age=i-1-trigger
        if i>trigger and tuple(s['p'])==tuple(level['nightfall']['tile']) and age%10>=6:
            light=min(cap,light+level['nightfall']['extraLight'])
            day_dusk+=1
        delta=light-s['light']
        if i<len(route)-1:assert light>0,(n,i,light)
        if tuple(s['p'])==moon:assert i==proof['moonRoadStep'] and age%10<6
    assert light>=0 and route[-1]['p']==level['depot']
print(f'PASS: 100 day/night routes enter moon road at night and complete; {day_dusk} daytime dusk crossings save light')
