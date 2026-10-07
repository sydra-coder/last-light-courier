// Test whether a certified short route also survives the other road choice.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=path.resolve(__dirname,'..');
const defaults=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_routes.json')));
const signals=JSON.parse(fs.readFileSync(path.join(root,'reference-hints-v1/normalized_signal_routes.json')));
const ids=[1804,1807,1828,1873,1900,1980,1994];
function tryRoute(n,branch,route){
  api.choose(n);api.begin();const level=api.getLevel();
  if(level.repairRequired)api.buyFreeRepair();
  if(branch==='signal'&&!api.signal())throw Error(`Signal unavailable at ${n}`);
  for(let i=1;i<route.length;i++)if(!api.move(route[i].slice(0,2)))
    return {completed:false,blockedAt:i,position:route[i].slice(0,2),state:api.getState()};
  const state=api.getState();
  return {completed:state.done&&!state.failed,steps:state.turns,finishLight:state.light};
}
const rows=ids.map(n=>{
  const ordinary=defaults[n-201],signaled=signals[n];
  return {level:n,defaultRouteUnderSignal:tryRoute(n,'signal',ordinary),signalRouteUnderDefault:tryRoute(n,'default',signaled)};
});
const output=path.join(__dirname,'cross_branch_routes.json');
fs.writeFileSync(output,JSON.stringify(rows,null,2));
console.log(JSON.stringify(rows.map(x=>({level:x.level,defaultUnderSignal:x.defaultRouteUnderSignal.completed,
  signalUnderDefault:x.signalRouteUnderDefault.completed,defaultBlockedAt:x.defaultRouteUnderSignal.blockedAt,
  signalBlockedAt:x.signalRouteUnderDefault.blockedAt}))));
