const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const row=JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-1201-1300-current-WENS.json'))).rows.find(x=>x.level===1236);
const results=[];
for(const powered of [false,true]){
  api.choose(1236);api.begin();
  let used=false,blockedAt=null;
  for(let i=1;i<row.staticCandidateRoute.length;i++){
    if(!api.move(row.staticCandidateRoute[i])){blockedAt=i;break}
    if(powered&&!used&&api.getState().mask)used=api.usePower('road_repair');
  }
  const state=api.getState();
  results.push({powered,powerUsed:used,blockedAt,completed:state.done&&!state.failed,
    steps:state.turns,light:state.light,referenceSteps:row.verifiedRouteSteps});
}
fs.writeFileSync(path.join(__dirname,'current-1236-shortcut-audit.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results));
