const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const input=path.resolve(process.env.LLC_EVENT_AWARE_INPUT||path.join(__dirname,'event-aware-801-sample.json'));
const proof=JSON.parse(fs.readFileSync(input));
const results=[];
for(const row of proof.rows){
  if(!row.staticCandidateRoute)continue;
  api.choose(row.level);api.begin();let blocked=null;
  if(api.getLevel().repairRequired&&!api.buyFreeRepair())blocked={step:0,reason:'required repair unavailable'};
  for(let i=1;i<row.staticCandidateRoute.length&&!blocked;i++){
    const tile=row.staticCandidateRoute[i];
    if(!api.move(tile))blocked={step:i,tile,open:api.isOpen(tile),shadow:api.shadowBlocked(tile),reason:api.getState().reason};
  }
  const end=api.getState();
  const candidateSteps=row.eventAwareSteps??row.echoAwareSteps;
  const referenceSteps=row.verifiedRouteSteps??row.referenceSteps;
  const completed=!blocked&&end.done&&!end.failed;
  results.push({level:row.level,candidateSteps,referenceSteps,completed,
    shorterThanCurrent:completed&&end.turns<referenceSteps,
    blocked,steps:end.turns,light:end.light,order:row.order});
}
const output=input.replace(/\.json$/,'-replay.json');
fs.writeFileSync(output,JSON.stringify({source:input,rows:results},null,2));
console.log(JSON.stringify({tested:results.length,completed:results.filter(x=>x.completed).length,
  shorterThanCurrent:results.filter(x=>x.shorterThanCurrent).length,
  successes:results.filter(x=>x.shorterThanCurrent),
  ties:results.filter(x=>x.completed&&x.steps===x.referenceSteps),
  slower:results.filter(x=>x.completed&&x.steps>x.referenceSteps),
  failures:results.filter(x=>!x.completed).slice(0,5)}));
