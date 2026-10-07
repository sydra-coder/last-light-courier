const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-1601-1700-current-WENS.json')));
const results=[];
for(const n of [1601,1656,1696]){
  const row=source.rows.find(x=>x.level===n);
  for(const powered of [false,true]){
    api.choose(n);api.begin();
    const power=api.getLevel().reviewPower;
    let used=false,blockedAt=null;
    if(powered&&power==='map_stabilizer')used=api.usePower(power);
    for(let i=1;i<row.staticCandidateRoute.length;i++){
      if(!api.move(row.staticCandidateRoute[i])){blockedAt=i;break}
      if(powered&&!used&&((power==='lumen_flask'&&i===1)||(power==='road_repair'&&api.getState().mask)))
        used=api.usePower(power);
    }
    const state=api.getState();
    results.push({level:n,powered,power,powerUsed:used,blockedAt,completed:state.done&&!state.failed,
      steps:state.turns,light:state.light,referenceSteps:row.verifiedRouteSteps,order:row.order});
  }
}
fs.writeFileSync(path.join(__dirname,'current-1601-shortcuts-audit.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results));
