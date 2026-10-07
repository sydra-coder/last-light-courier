// Verify the generated preview's early 2x2 fields and completion routes.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const authored=JSON.parse(fs.readFileSync(path.join(__dirname,'shadow-influence-v1/authored_levels.json'),'utf8'));
const archive=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
const html=fs.readFileSync(path.join(root,'design/campaign-2000-preview/index.html'),'utf8');
if(!html.includes("const influence=level.shadowInfluence2x2?.cells.some(tile=>eq(tile,p))"))throw Error('Canvas shadow field cue missing');
if(authored.length!==25)throw Error('Expected 25 early fields');
for(const authoredLevel of authored){
  const n=authoredLevel.n,route=archive[n-1].solutions[0].route;
  api.choose(n);api.begin();
  const level=api.getLevel(),cells=level.shadowInfluence2x2.cells;
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Level ${n}: required repair unavailable`);
  if(cells.length!==4||cells.some(p=>api.shadowBlocked(p)))throw Error(`Level ${n}: field active too early`);
  for(let i=1;i<route.length;i++){
    if(!api.move(route[i].p))throw Error(`Level ${n}: route blocked at ${i}`);
    if(api.getState().active&&cells.some(p=>!api.shadowBlocked(p)))throw Error(`Level ${n}: field not blocking after delivery`);
  }
  const state=api.getState();
  if(!state.done||state.failed)throw Error(`Level ${n}: route did not complete`);
}
console.log(`PASS: ${authored.length} early 2×2 fields cue and block at delivery; all routes complete`);
