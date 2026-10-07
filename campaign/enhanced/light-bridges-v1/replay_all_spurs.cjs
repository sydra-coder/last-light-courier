const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'spur_routes.json'),'utf8'));
const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'relocated_spur_search.json'),'utf8')).rows;
const failures=[];
for(let n=701;n<=800;n++){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
  const route=routes[n];
  for(let i=1;i<route.length;i++){
    const before=api.getState();
    if(before.active&&!before.bridgeBuilt&&!api.useBridge()){failures.push({level:n,step:i,reason:'power unavailable'});break;}
    if(!api.move(route[i])){failures.push({level:n,step:i,reason:api.getState().reason||'move rejected'});break;}
  }
  const end=api.getState(),proof=expected[n-701].best;
  if(!end.done||end.failed||end.turns!==proof.finishSteps||end.light!==proof.finishLight)
    failures.push({level:n,reason:'finish mismatch',steps:end.turns,light:end.light,expected:proof.finishLight});
}
const report={attempted:100,passed:100-new Set(failures.map(f=>f.level)).size,failed:failures};
fs.writeFileSync(path.join(__dirname,'all_spurs_replay.json'),JSON.stringify(report,null,2));
console.log(`Bridge-house staged route replay: ${report.passed}/100; failures ${failures.length}`);
if(failures.length){console.log(failures.slice(0,10));process.exitCode=1;}
