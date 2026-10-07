// Test optimistic phase tours in the actual preview; never treat static search as completion.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const signal=process.argv.includes('--signal');
const source=path.join(__dirname,signal?'current-phase-signal-search.json':'current-phase-default-search.json');
const proof=JSON.parse(fs.readFileSync(source));
const rows=[];
for(const row of proof.rows){
  if(!row.staticCandidateRoute)continue;
  api.choose(row.level);api.begin();
  let blocked=null;
  if(api.getLevel().repairRequired&&!api.buyFreeRepair())blocked={step:0,reason:'free repair'};
  if(signal&&!blocked&&!api.signal())blocked={step:0,reason:'signal'};
  for(let i=1;i<row.staticCandidateRoute.length&&!blocked;i++)
    if(!api.move(row.staticCandidateRoute[i]))blocked={step:i,tile:row.staticCandidateRoute[i],reason:api.getState().reason};
  const state=api.getState();
  rows.push({level:row.level,referenceSteps:row.verifiedRouteSteps,candidateSteps:row.eventAwareSteps,
    completed:!blocked&&state.done&&!state.failed,playedSteps:state.turns,
    finishLight:state.light,blocked,order:row.order,
    route:!blocked&&state.done&&!state.failed?row.staticCandidateRoute:undefined});
}
const output=source.replace(/\.json$/,'-replay.json');
fs.writeFileSync(output,JSON.stringify({scope:'Static candidates replayed under full preview rules; completed tours only, no optimality claim.',signal,rows},null,2));
console.log(JSON.stringify({signal,attempted:rows.length,completed:rows.filter(x=>x.completed).length,
  shorter:rows.filter(x=>x.completed&&x.playedSteps<x.referenceSteps).length,
  exactTies:rows.filter(x=>x.completed&&x.playedSteps===x.referenceSteps).length,
  failures:rows.filter(x=>!x.completed).slice(0,8)}));
