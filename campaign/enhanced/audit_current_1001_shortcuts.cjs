// Verify the two current 1001–1100 shortcuts with and without their sample power.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const source=JSON.parse(fs.readFileSync(path.join(__dirname,'event-aware-1001-1100-current-WENS.json')));
const selected=new Map(source.rows.filter(x=>[1009,1019].includes(x.level)).map(x=>[x.level,x]));
const results=[];
for(const [number,row] of selected){
  for(const powered of [false,true]){
    api.choose(number);api.begin();
    const level=api.getLevel();
    if(level.repairRequired&&!api.buyFreeRepair())throw Error(`repair unavailable ${number}`);
    let powerUsed=false,blockedAt=null;
    if(powered&&level.reviewPower==='map_stabilizer')powerUsed=api.usePower(level.reviewPower);
    for(let i=1;i<row.staticCandidateRoute.length;i++){
      if(!api.move(row.staticCandidateRoute[i])){blockedAt=i;break}
      if(powered&&!powerUsed&&level.reviewPower==='lumen_flask'&&i===1)
        powerUsed=api.usePower(level.reviewPower);
    }
    const state=api.getState();
    results.push({level:number,powered,power:level.reviewPower,powerUsed,blockedAt,
      completed:state.done&&!state.failed,steps:state.turns,light:state.light,
      referenceSteps:row.verifiedRouteSteps,houseOrder:row.order});
  }
}
const output=path.join(__dirname,'current-1001-shortcuts-audit.json');
fs.writeFileSync(output,JSON.stringify({scope:'Two full-rule shorter tour candidates; powered samples are diagnostic only.',results},null,2));
console.log(JSON.stringify(results));
