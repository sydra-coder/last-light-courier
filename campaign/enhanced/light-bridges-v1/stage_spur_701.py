"""Stage a bridge-only house spur on level 701 without changing the live build."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[3]
source=ROOT/'design/campaign-2000-preview/index.html'
text=source.read_text(encoding='utf-8')
start=text.index('const LEVELS=')
end=text.index(';\n',start)+1
levels=json.loads(text[start+len('const LEVELS='):end-1])
level=levels[700]
assert level['lightBridge']==[16,11]
assert level['homes'][5]['p']==[17,11]
level['homes'][5]['p']=[16,12]
level['walls']=[*level['walls'],'15,12','16,13']
level['oneWayTile']=[17,12]
level['oneWayFrom']=[16,12]
level['brief']+=' District 6 sits on a short lane across the Light Bridge. Leave through its one-way street.'
candidate=text[:start]+'const LEVELS='+json.dumps(levels,separators=(',',':'))+';'+text[end:]
target=Path(__file__).with_name('spur_701_candidate.html')
target.write_text(candidate,encoding='utf-8')
print(target)
