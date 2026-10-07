// Replay static routes without taking the level's free repair.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const rows=JSON.parse(fs.readFileSync(path.join(__dirname,'no-repair-1625-candidates.json')));
const results=[];
for(const candidate of rows){
  api.choose(1625);api.begin();
  let failedAt=null;
  for(let i=1;i<candidate.route.length;i++)if(!api.move(candidate.route[i])){failedAt=i;break}
  const state=api.getState();
  results.push({order:candidate.order,directions:candidate.directions,steps:candidate.steps,
    failedAt,done:state.done,failed:state.failed,light:state.light,
    actualTurns:state.turns,deliveredMask:state.mask});
}
const complete=results.filter(x=>x.done&&!x.failed);
const report={attempted:rows.length,complete:complete.length,
  shortestComplete:complete.length?Math.min(...complete.map(x=>x.steps)):null,
  firstComplete:complete[0]||null,firstFailures:results.slice(0,8)};
fs.writeFileSync(path.join(__dirname,'no-repair-1625-probe.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report));
