// Express service is useful, but its five maps retain a viable walking choice.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'../event-aware-1701-1800-replay.json'),'utf8')).completedRoutes;
const express=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'express_routes.json'),'utf8')).map(x=>[x.level,x]));
const rows=[];
for(const [n,proof] of express){
  const route=source.find(x=>x.level===n)?.route;
  if(!route)throw Error(`Walking route missing ${n}`);
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired)api.buyFreeRepair();
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))throw Error(`${n}: walking alternative blocked at ${i}`);
  const finish=api.getState();
  if(!finish.done||finish.failed||finish.turns<=proof.transitSteps||finish.light<1)
    throw Error(`${n}: walking alternative did not finish`);
  rows.push({level:n,walkingSteps:finish.turns,walkingFinishLight:finish.light,expressSteps:proof.transitSteps});
}
console.log(JSON.stringify(rows));
