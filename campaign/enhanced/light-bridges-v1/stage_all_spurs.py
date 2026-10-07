"""Stage all 100 bridge-house redesigns in a separate browser preview."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
source=ROOT/'design/campaign-2000-preview/index.html'
html=source.read_text(encoding='utf-8');start=html.index('const LEVELS=');end=html.index(';\n',start)+1
levels=json.loads(html[start+len('const LEVELS='):end-1])
found=json.loads((HERE/'relocated_spur_search.json').read_text(encoding='utf-8'))['rows']
assert len(found)==100 and all(row['found'] for row in found)
overlays={};routes={}
for row in found:
    n=row['level'];item=row['best'];level=levels[n-1]
    bridge=item.get('bridgeTo',level['lightBridge']);house=item['houseTo'];exit_tile=item['oneWayTile']
    old_house=level['homes'][item['houseIndex']]['p']
    assert old_house==item['houseFrom']
    assert level.get('oneWayTile') is None or level['oneWayTile']==exit_tile
    level['lightBridge']=bridge
    level['homes'][item['houseIndex']]['p']=house
    level['walls']=sorted((set(level['walls'])|set(item['addedWalls']))-set(item['openedCells']))
    level['oneWayTile']=exit_tile;level['oneWayFrom']=item['oneWayFrom']
    level['phase']=item['phase'];level['phase2']=item['phase2']
    level['cap']+=item.get('capBoost',0)
    level['bridgeHouseIndex']=item['houseIndex']
    level['brief']+=' The marked bridge reaches a house lane. Leave through its one-way road.'
    overlays[str(n)]={'bridge':bridge,'houseIndex':item['houseIndex'],'house':house,
                      'oneWayTile':exit_tile,'oneWayFrom':item['oneWayFrom'],
                      'addedWalls':item['addedWalls'],'openedCells':item['openedCells'],
                      'phase':item['phase'],'phase2':item['phase2'],'capBoost':item.get('capBoost',0)}
    routes[str(n)]=item['route']
candidate=html[:start]+'const LEVELS='+json.dumps(levels,separators=(',',':'))+';'+html[end:]
(HERE/'all_spurs_candidate.html').write_text(candidate,encoding='utf-8')
(HERE/'spur_overlays.json').write_text(json.dumps(overlays,separators=(',',':')),encoding='utf-8')
(HERE/'spur_routes.json').write_text(json.dumps(routes,separators=(',',':')),encoding='utf-8')
print('Staged',len(overlays),'bridge-house maps and route overrides')
