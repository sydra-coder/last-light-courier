const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const level=Number(process.env.LLC_CHOICE_LEVEL||1805);
const candidates=JSON.parse(fs.readFileSync(path.join(__dirname,`level-${level}-choice-candidates.json`))).candidates;
const chosen=Number(process.env.LLC_CHOICE_INDEX||0),candidate=candidates[chosen];
const signal=JSON.parse(fs.readFileSync(path.join(__dirname,'../reference-hints-v1/normalized_signal_routes.json')))[level];
function run(route,sendSignal){
  api.choose(level);api.begin();
  if(sendSignal&&!api.signal())throw Error('Signal unavailable');
  let blocked=null;
  for(let i=1;i<route.length;i++)if(!api.move(route[i])){blocked={step:i,tile:route[i],reason:api.getState().reason};break;}
  const state=api.getState();return {completed:!blocked&&state.done&&!state.failed,blocked,
    steps:state.turns,light:state.light,eventTriggered:state.eventTriggered};
}
console.log(JSON.stringify({level,candidate:chosen,close:candidate.close,
  default:run(candidate.route,false),signal:run(signal,true)}));
