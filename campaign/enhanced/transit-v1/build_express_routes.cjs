// Reuse a live-completed walking tour, then replace its long return leg with transit.
const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=__dirname;
const stops=JSON.parse(fs.readFileSync(path.join(root,'express_stop_overlays.json'),'utf8'));
const candidates=JSON.parse(fs.readFileSync(path.join(root,'../event-aware-1701-1800-replay.json'),'utf8')).completedRoutes;
const proofs=[];
for(const [key,pair] of Object.entries(stops)){
  const n=Number(key),fast=candidates.find(x=>x.level===n);
  if(!fast)throw Error(`Missing completed walking route ${n}`);
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`Free repair unavailable ${n}`);
  const homeKeys=new Set(level.homes.map(h=>h.p.join(',')));
  const last=fast.route.reduce((index,p,i)=>homeKeys.has(p.join(','))?i:index,0);
  const board=fast.route.findIndex((p,i)=>i>last&&JSON.stringify(p)===JSON.stringify(pair[0]));
  if(board<0||JSON.stringify(fast.route.at(-2))!==JSON.stringify(pair[1])||
     JSON.stringify(level.transitLink.stops)!==JSON.stringify(pair))throw Error(`Stop alignment wrong ${n}`);
  const route=[...fast.route.slice(0,board+1),pair[1],fast.route.at(-1)];
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))throw Error(`${n}: express route blocked at ${i}`);
  const finish=api.getState();
  if(!finish.done||finish.failed||finish.turns!==route.length-1||finish.turns>=fast.steps)
    throw Error(`${n}: express route did not improve the walking tour`);
  proofs.push({level:n,route,walkingSteps:fast.steps,transitSteps:finish.turns,
    transitFinishLight:finish.light,savedAgainstWalking:fast.steps-finish.turns,
    freeRepairRequired:!!level.repairRequired});
}
fs.writeFileSync(path.join(root,'express_routes.json'),JSON.stringify(proofs,null,2));
console.log(JSON.stringify(proofs.map(({level,walkingSteps,transitSteps,transitFinishLight})=>({level,walkingSteps,transitSteps,transitFinishLight}))));
