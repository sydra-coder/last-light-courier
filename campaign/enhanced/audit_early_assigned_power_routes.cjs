// Verify assigned Decoy Light and Reveal Pulse in the generated preview.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const archive=JSON.parse(fs.readFileSync(path.join(__dirname,'../../design/map-solutions-1000.json'),'utf8')).levels;
const decoys=JSON.parse(fs.readFileSync(path.join(__dirname,'decoys-v1/power_proofs.json'),'utf8'));
const revised=Object.fromEntries(JSON.parse(fs.readFileSync(path.join(__dirname,'early-route-rebalance-v1/power-sample-replay.json'),'utf8')).map(x=>[x.level,x]));
const routeOverrides=JSON.parse(fs.readFileSync(path.join(__dirname,'reference-hints-v1/route_overrides.json'),'utf8'));
const failures=[];
let passed=0;
for(let n=151;n<=300;n++){
  const proof=archive[n-1],route=revised[n]?routeOverrides[n].map(p=>({p})):proof.solutions[0].route,decoy=n<=200?decoys[n-151]:null;
  api.choose(n);api.begin();
  let used=false,problem=null;
  if(api.getLevel().repairRequired&&api.getLevel().repair?.cost===0&&!api.buyFreeRepair())problem='required free repair unavailable';
  if(!decoy&&!revised[n]?.useAfterStep){
    if(!api.usePower('reveal_pulse')||!api.getState().beaconRevealed)problem='Reveal Pulse failed';
    else used=true;
  }
  for(let i=1;i<route.length&&!problem;i++){
    if(revised[n]?.useAfterStep===i){
      if(!api.usePower('reveal_pulse')||!api.getState().beaconRevealed){problem=`Reveal Pulse failed at ${i}`;break}
      used=true;
    }
    if(!api.move(route[i].p)){problem=`route blocked at ${i}: ${api.getState().reason||'move rejected'}`;break}
    if(decoy&&i===decoy.useAfterStep){
      if(!api.usePower('decoy_light')||!api.canDecoyAt(decoy.decoyTile)){problem=`Decoy Light unavailable at ${i}`;break}
      api.placeDecoy(decoy.decoyTile);
      if(api.getState().decoyTurns!==4){problem=`Decoy Light had no effect at ${i}`;break}
      used=true;
    }
  }
  const end=api.getState();
  if(!problem&&(!used||!end.done||end.failed))problem='power-assisted route did not finish';
  if(problem)failures.push({level:n,problem});else passed++;
}
const report={levels:150,passed,failed:failures.length,failures,scope:'One authored power use and route replay on each Decoy Light and Reveal Pulse map; no shortest-route claim.'};
fs.writeFileSync(path.join(__dirname,'early-assigned-power-route-audit.json'),JSON.stringify(report,null,2));
console.log(`Early assigned powers: ${passed}/150 completed`);
if(failures.length){console.log(JSON.stringify(failures.slice(0,10),null,2));process.exitCode=1}
