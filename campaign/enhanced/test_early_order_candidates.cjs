const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'early-order-301-310-static.json'))).rows;
const rows=[];
for(const item of source){
  api.choose(item.level);api.begin();const route=item.staticCandidateRoute;
  let blocked=null;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked={step:i,tile:route[i],reason:api.getState().reason,
    open:api.isOpen(route[i]),legal:api.legal(route[i]),shadow:api.shadowBlocked(route[i])};break}
  const end=api.getState();
  rows.push({level:item.level,lowerBound:item.eventAwareSteps,referenceSteps:item.verifiedRouteSteps,
    completed:!blocked&&end.done&&!end.failed,blocked,steps:end.turns,finishLight:end.light,order:item.order,route});
}
fs.writeFileSync(path.join(__dirname,'early-order-301-310-replay.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows.map(({level,lowerBound,completed,blocked,steps,finishLight,order})=>({level,lowerBound,completed,blocked,steps,finishLight,order}))));
