// Replay current normalized levels 201–1000 through the full preview rules.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'reference-hints-v1/normalized_routes.json')));
const failures=[],rows=[];
for(let n=201;n<=1000;n++){
  api.choose(n);api.begin();const level=api.getLevel(),route=routes[n-201];let problem=null,bridges=0;
  if(level.repairRequired&&!api.buyFreeRepair())problem='required free repair unavailable';
  for(let i=1;i<route.length&&!problem;i++){
    const state=api.getState();
    if(level.lightBridgeRequiresPower&&state.active&&!state.bridgeBuilt){
      if(!api.useBridge()){problem=`bridge unavailable before step ${i}`;break}bridges++;
    }
    if(!api.move(route[i].slice(0,2)))problem=`move blocked at step ${i}`;
  }
  const end=api.getState();
  if(!problem&&(!end.done||end.failed))problem='route did not complete';
  if(!problem&&level.lightBridgeRequiresPower&&bridges!==1)problem=`bridge use count ${bridges}`;
  if(problem)failures.push({level:n,problem,steps:end.turns,light:end.light});
  else rows.push({level:n,steps:end.turns,light:end.light,bridges});
}
const report={tested:800,passed:rows.length,failures,scope:'Full runtime replay of normalized default routes 201–1000, including required free repairs and supplied bridges.'};
fs.writeFileSync(path.join(__dirname,'early-canonical-route-audit.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({tested:report.tested,passed:report.passed,failures:failures.slice(0,10)}));
if(failures.length)process.exitCode=1;
