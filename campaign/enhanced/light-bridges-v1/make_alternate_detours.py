"""Try alternate bridge bypasses obtained by excluding each shortest-bypass cell."""
from pathlib import Path
import json
import os
from make_bridge_detours import shortest,levels,archive

base=Path(__file__).parent
bridge_free={x['level'] for x in json.loads((base/'verified_no_bridge_routes.json').read_text(encoding='utf-8'))}
if os.environ.get('LLC_INCLUDE_ALL_BRIDGE_LEVELS')=='1':bridge_free=set()
rows=[]
for n in range(701,801):
    if n in bridge_free:continue
    l=levels[n-1];old=[s['p'] for s in archive[n-1]['solutions'][0]['route']]
    i=old.index(l['lightBridge']);a,b=old[i-1],old[i+1]
    initial=shortest(l,a,b,'EWSN')
    if initial is None:continue
    seen={tuple(tuple(p) for p in initial)}
    for tile in initial[1:-1]:
        for order in ('EWSN','ENWS','WSEN','NESW','SWNE'):
            detour=shortest(l,a,b,order,tile)
            if detour is None:continue
            key=tuple(tuple(p) for p in detour)
            if key in seen:continue
            seen.add(key)
            route=old[:i]+detour[1:]+old[i+2:]
            rows.append({'level':n,'order':f'avoid-{tile[0]}-{tile[1]}-{order}','steps':len(route)-1,'route':route})
            if len(seen)>=31:break
        if len(seen)>=31:break
Path(os.environ.get('LLC_ALTERNATE_BRIDGE_TOURS_OUT',base/'alternate_detour_tours.json')).write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
print(f'Generated {len(rows)} alternate detours')
