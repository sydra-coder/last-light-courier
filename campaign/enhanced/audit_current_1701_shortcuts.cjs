const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-1701-1800-current-WENS.json')));
const results=[];
for(const n of [1763,1799]){
  const row=source.rows.find(x=>x.level===n);
  for(const powered of [false,true]){
    api.choose(n);api.begin();let used=false,blockedAt=null;
    for(let i=1;i<row.staticCandidateRoute.length;i++){
      if(!api.move(row.staticCandidateRoute[i])){blockedAt=i;break}
      if(powered&&!used&&i===1)used=api.usePower('lumen_flask');
    }
    const state=api.getState();
    results.push({level:n,powered,powerUsed:used,blockedAt,completed:state.done&&!state.failed,
      steps:state.turns,light:state.light,referenceSteps:row.verifiedRouteSteps,order:row.order});
  }
}
fs.writeFileSync(path.join(__dirname,'current-1701-shortcuts-audit.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results));
