const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const choices=[['event-aware-1501-1600-current-WENS.json',1567],['event-aware-1501-1600-current-EWSN.json',1588]];
const rows=[];
for(const [file,n] of choices){
  const row=JSON.parse(fs.readFileSync(path.join(__dirname,file))).rows.find(x=>x.level===n);
  for(const powered of [false,true]){
    api.choose(n);api.begin();
    let used=false,blockedAt=null;
    if(powered)used=api.usePower('map_stabilizer');
    for(let i=1;i<row.staticCandidateRoute.length;i++)
      if(!api.move(row.staticCandidateRoute[i])){blockedAt=i;break}
    const end=api.getState();
    rows.push({level:n,powered,powerUsed:used,blockedAt,completed:end.done&&!end.failed,
      steps:end.turns,light:end.light,referenceSteps:row.verifiedRouteSteps,order:row.order});
  }
}
fs.writeFileSync(path.join(__dirname,'current-1501-shortcuts-audit.json'),JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows));
