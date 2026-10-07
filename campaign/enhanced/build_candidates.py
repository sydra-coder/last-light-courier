"""Resumeable 1001–2000 baseline map candidates; enhanced rules remain separate work."""
from pathlib import Path
import json, hashlib, sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'campaign'/'expansion'))
from build_1000 import build, replay, metrics

OUT=ROOT/'campaign'/'enhanced'/'candidates-v3'
OUT.mkdir(parents=True,exist_ok=True)
regions=['Storm March','The Long Night','Breachlands','The Lumen Engine',"Keeper's Arsenal",'Convergence','The Moving Kingdom','Last Provinces','Black Horizon','The Last Light']
events=['Storm wind / flood','Fog / day-night','Spawner / merge-split','Light network / overload','Map control','Two-system combination','Chained transformation','Regional transit','Multi-phase consequence','Mastery combination']

def targets(n):
    arc=(n-1001)//100;offset=(n-1001)%100
    size=([22,22,20,22,20] if arc==0 else [18,20,18,22,20])[offset//20]
    houses=[4,5,6,7,8][offset//20]
    return arc,size,houses

def candidate(n):
    arc,size,houses=targets(n)
    for attempt in range(60):
        item=build(n,size_override=size,houses_override=houses,band_override=7,seed_override=n*90113+attempt*1000003,winding=True)
        if item is None:continue
        level,route=item
        level['enhancedPlan']={'region':regions[arc],'eventFamily':events[arc],'status':'planned; event not in baseline replay'}
        level['reviewStatus']='candidate geometry and baseline route only; not final design'
        replay(level,[s['p'] for s in route],level['repairRequired'])
        fingerprint=hashlib.sha256(json.dumps(level,sort_keys=True).encode()).hexdigest()
        record={'level':n,'mapFingerprint':fingerprint,'solutions':[{'repairPurchased':level['repairRequired'],'status':'verified_reference_baseline','steps':len(route)-1,'route':route,'optimal':False}]}
        return level,record,attempt
    raise RuntimeError(f'Could not generate level {n} after 60 deterministic attempts')

def main():
    all_levels=[];all_routes=[];used=set()
    for start in range(1001,2001,100):
        end=start+99;lp=OUT/f'levels_{start}_{end}.json';rp=OUT/f'routes_{start}_{end}.json'
        if lp.exists() and rp.exists():
            levels=json.loads(lp.read_text(encoding='utf-8'));routes=json.loads(rp.read_text(encoding='utf-8'))
            assert len(levels)==100 and len(routes)==100
            assert [l['n'] for l in levels]==list(range(start,end+1))
            for l,r in zip(levels,routes):
                assert r['level']==l['n']
                replay(l,[s['p'] for s in r['solutions'][0]['route']],l['repairRequired'])
        else:
            levels=[];routes=[]
            for n in range(start,end+1):
                l,r,attempt=candidate(n)
                geometry=json.dumps([l['grid'],l['depot'],l['homes'],l['walls'],l['patrol'],l['patrol2']])
                if geometry in used:raise RuntimeError(f'Duplicate geometry at {n}')
                used.add(geometry);levels.append(l);routes.append(r)
                if n%25==0:print(f'built {n}, retries {attempt}',flush=True)
            lp.write_text(json.dumps(levels,separators=(',',':')),encoding='utf-8')
            rp.write_text(json.dumps(routes,separators=(',',':')),encoding='utf-8')
        all_levels.extend(levels);all_routes.extend(routes)
        print(f'baseline candidates replayed through {end}',flush=True)
    assert len(all_levels)==1000 and len(all_routes)==1000
    full=json.loads((ROOT/'CAMPAIGN_1000_LEVELS.json').read_text(encoding='utf-8'))+all_levels
    assert [l['n'] for l in full]==list(range(1,2001))
    (OUT/'CAMPAIGN_2000_CANDIDATES.json').write_text(json.dumps(full,separators=(',',':')),encoding='utf-8')
    (OUT/'ROUTES_1001_2000_BASELINE.json').write_text(json.dumps(all_routes,separators=(',',':')),encoding='utf-8')
    print('PASS: 2000 numbered maps; 1000 new baseline candidates replayed. Enhanced mechanics still require integration and validation.',flush=True)

if __name__=='__main__':main()
