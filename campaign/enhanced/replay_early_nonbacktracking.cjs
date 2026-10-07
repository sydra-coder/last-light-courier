const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const n=Number(process.env.LLC_EARLY_LEVEL||301);
const proof=JSON.parse(fs.readFileSync(path.join(__dirname,`early-nonbacktracking-${n}.json`)));
if(!proof.route){
  const report={level:n,staticSteps:null,staticOrder:null,completed:false,reason:'no optimistic route under static walls and no-immediate-reversal',states:proof.states};
  fs.writeFileSync(path.join(__dirname,`early-nonbacktracking-${n}-replay.json`),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
  process.exit(0);
}
api.choose(n);api.begin();let blocked=null;
const level=api.getLevel();
if(level.repairRequired&&!api.buyFreeRepair())blocked={step:0,reason:'required free repair unavailable'};
for(let i=1;i<proof.route.length&&!blocked;i++){
  const current=api.getState();
  if(level.lightBridgeRequiresPower&&current.active&&!current.bridgeBuilt&&!api.useBridge()){
    blocked={step:i,reason:'bridge charge unavailable'};break;
  }
  if(!api.move(proof.route[i])){blocked={step:i,tile:proof.route[i],
    open:api.isOpen(proof.route[i]),shadow:api.shadowBlocked(proof.route[i])};break}
}
const end=api.getState();const report={level:n,staticSteps:proof.steps,staticOrder:proof.order,
  completed:!blocked&&end.done&&!end.failed,blocked,steps:end.turns,finishLight:end.light,
  lost:end.lost,rechargeUsed:end.rechargeUsed,leechDrains:end.leechDrains,route:proof.route};
fs.writeFileSync(path.join(__dirname,`early-nonbacktracking-${n}-replay.json`),JSON.stringify(report,null,2));
console.log(JSON.stringify({level:n,staticSteps:report.staticSteps,completed:report.completed,blocked,steps:report.steps,
  finishLight:report.finishLight,lost:report.lost,rechargeUsed:report.rechargeUsed,leechDrains:report.leechDrains}));
