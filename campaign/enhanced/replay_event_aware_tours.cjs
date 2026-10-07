// Test static event-aware tours under the full preview movement rules.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const input=path.resolve(process.argv[2]||'');
if(!fs.existsSync(input))throw Error(`Missing event-aware tour file: ${input}`);
const source=JSON.parse(fs.readFileSync(input,'utf8'));
const signal=process.argv.includes('--signal');
const rows=[];
for(const candidate of source.rows){
  const route=candidate.staticCandidateRoute;
  if(!route||route.length-1>=candidate.verifiedRouteSteps)continue;
  api.choose(candidate.level);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Free repair unavailable: ${candidate.level}`);
  if(signal&&!api.signal())throw Error(`Signal unavailable: ${candidate.level}`);
  let blockedStep=null;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){blockedStep=i;break}
  const end=api.getState();
  rows.push({level:candidate.level,steps:route.length-1,referenceSteps:candidate.verifiedRouteSteps,
    completed:blockedStep===null&&end.done&&!end.failed,blockedStep,
    finishLight:end.light,route:blockedStep===null&&end.done&&!end.failed?route:undefined});
}
const completed=rows.filter(x=>x.completed);
const report={input,signal,attempted:rows.length,completed:completed.length,
  completedRoutes:completed,scope:'Static phase-tour candidates replayed under full preview rules. A shorter completion disproves a recorded minimum; failure to find one does not prove optimality.'};
const output=process.env.LLC_EVENT_AWARE_REPLAY_OUTPUT?path.resolve(process.env.LLC_EVENT_AWARE_REPLAY_OUTPUT):input.replace(/\.json$/,'-replay.json');
fs.writeFileSync(output,JSON.stringify(report,null,2));
console.log(JSON.stringify({attempted:report.attempted,completed:report.completed,
  shorterLevels:completed.map(x=>x.level)}));
