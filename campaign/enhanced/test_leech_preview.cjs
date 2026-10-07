// Confirm authored Leech drains occur in the generated preview rules.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=path.resolve(__dirname,'../..');
const leeches=JSON.parse(fs.readFileSync(path.join(__dirname,'leech-houses-v1/authored_levels.json'),'utf8'));
const archive=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'),'utf8')).levels;
if(leeches.length<60)throw Error('Too few Leech test maps');
for(const level of leeches){
  const route=archive[level.n-1].solutions[0].route;
  api.choose(level.n);api.begin();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Level ${level.n}: required repair unavailable`);
  for(let i=1;i<route.length;i++)if(!api.move(route[i].p))throw Error(`Level ${level.n}: blocked at ${i}`);
  const state=api.getState();
  if(!state.done||state.failed||!state.rechargeDrained)throw Error(`Level ${level.n}: no completed Leech drain`);
}
console.log(`PASS: ${leeches.length} preview Leech drains occur and every route completes`);
