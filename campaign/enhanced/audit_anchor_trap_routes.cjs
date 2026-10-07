// Seek a completed route with a captured, immobile patrol on each Anchor Trap map.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const archive=JSON.parse(fs.readFileSync(path.join(__dirname,'../../design/map-solutions-1000.json'),'utf8')).levels;
const results=[],failures=[];
for(let n=101;n<=150;n++){
  const level=api.LEVELS[n-1],route=archive[n-1].solutions[0].route;
  let found=null,attempts=0;
  for(let at=1;at<route.length-4&&!found;at++){
    if(!route[at].mask)continue;
    const p=route[at].p,remaining=new Set(route.slice(at+1).map(step=>step.p.join(',')));
    const candidates=[];
    for(const [patrol,phase] of [[level.patrol,route[at].phase],[level.patrol2,route[at].phase2]]){
      if(!patrol)continue;
      for(let ahead=1;ahead<patrol.length;ahead++){
        const tile=patrol[(phase+ahead)%patrol.length];
        if(!remaining.has(tile.join(','))&&Math.abs(tile[0]-p[0])+Math.abs(tile[1]-p[1])<=2)candidates.push(tile);
      }
    }
    for(const tile of candidates){
      attempts++;
      api.choose(n);api.begin();
      if(level.repairRequired&&level.repair?.cost===0)api.buyFreeRepair();
      let blocked=false;
      for(let i=1;i<=at;i++)if(!api.move(route[i].p)){blocked=true;break}
      if(blocked||!api.usePower('anchor_trap')||!api.canTrapAt(tile))continue;
      api.placeTrap(tile);
      let captured=false,held=false;
      for(let i=at+1;i<route.length;i++){
        const before=api.getState();
        if(!api.move(route[i].p)){blocked=true;break}
        const after=api.getState();
        if(after.trappedPatrol)captured=true;
        if(before.trappedPatrol){
          const key=before.trappedPatrol===1?'phase':'phase2';
          if(after[key]!==before[key])throw Error(`Level ${n}: captured shadow moved`);
          held=true;
        }
      }
      const end=api.getState();
      if(!blocked&&captured&&held&&end.done&&!end.failed){found={level:n,useAfterStep:at,tile,attempts};break}
    }
  }
  if(found)results.push(found);else failures.push({level:n,attempts});
}
const report={levels:50,passed:results.length,failed:failures.length,results,failures,
  scope:'One recorded route per map with a captured and stationary patrol; not an optimal route or proof for every trap placement.'};
fs.writeFileSync(path.join(__dirname,'anchor-trap-route-audit.json'),JSON.stringify(report,null,2));
console.log(`Anchor Trap: ${results.length}/50 maps captured a patrol and completed the route`);
if(failures.length){console.log(JSON.stringify(failures.slice(0,10),null,2));process.exitCode=1}
