"""Vary patrol phase on bridge-free detours with local two-step turns."""
from pathlib import Path
import json

base=Path(__file__).parent
tours=json.loads((base/'bridge_detour_tours.json').read_text(encoding='utf-8'))
proofs=json.loads((base/'route_proofs.json').read_text(encoding='utf-8'))
bridge_free={x['level'] for x in json.loads((base/'verified_no_bridge_routes.json').read_text(encoding='utf-8'))}
rows=[]
for tour in tours:
    if tour['order']!='EWSN' or tour['level'] in bridge_free:continue
    n=tour['level']
    # The bridge proof records the crossing index on the archived route.
    crossing=proofs[n-701]['bridgeEntryStep']
    route=tour['route']
    for offset in range(-24,25,4):
        i=max(2,min(len(route)-3,crossing+offset))
        if route[i-1]==route[0] or route[i]==route[0]:continue
        for repeat in (1,2,3):
            bounce=[route[i-1],route[i]]*repeat
            candidate=route[:i+1]+bounce+route[i+1:]
            rows.append({'level':n,'order':f'timing-{offset}-{repeat}','steps':len(candidate)-1,'route':candidate})
(base/'timing_detour_tours.json').write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
print(f'Generated {len(rows)} timing variants')
