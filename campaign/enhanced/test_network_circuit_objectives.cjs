// The network mission must reject the known all-house bypass and accept the authored circuit.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=__dirname;
const old=JSON.parse(fs.readFileSync(path.join(root,'event-aware-1301-1400-replay.json'),'utf8')).completedRoutes;
const reference=JSON.parse(fs.readFileSync(path.join(root,'road-events-v1/post_event_routes.json'),'utf8'));
for(const n of [1306,1389]){
  const fast=old.find(x=>x.level===n);
  if(!fast)throw Error(`Missing bypass proof ${n}`);
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(!level.networkCircuitRequired)throw Error(`Circuit objective absent ${n}`);
  for(let i=1;i<fast.route.length-1;i++)if(!api.move(fast.route[i]))throw Error(`${n}: bypass failed before depot at ${i}`);
  const before=api.getState();
  if(before.mask!==(1<<level.homes.length)-1||before.networkCharged||before.transferCollected||before.overloadCrossed)
    throw Error(`${n}: bypass no longer demonstrates missed circuit`);
  if(api.move(fast.route.at(-1))||api.getState().done)
    throw Error(`${n}: bypass still clears the level`);
  api.choose(n);api.begin();
  const route=reference[n-1001].route;
  for(let i=1;i<route.length;i++)if(!api.move(route[i].p))throw Error(`${n}: circuit route blocked at ${i}`);
  const finish=api.getState();
  if(!finish.done||finish.failed||!finish.networkCharged||!finish.overloadCrossed||!finish.transferCollected)
    throw Error(`${n}: circuit route did not finish with all three stages`);
}
console.log('PASS: two network bypasses rejected; authored relay, gate and receiver routes finish');
