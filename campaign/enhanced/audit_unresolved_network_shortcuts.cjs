// Preserve concrete evidence that two network maps still have bypass routes.
const fs=require('fs'),path=require('path');
const api=require('./test_integrated_preview.cjs');
const root=__dirname;
const source=JSON.parse(fs.readFileSync(path.join(root,'event-aware-1301-1400-replay.json'),'utf8'));
const references=JSON.parse(fs.readFileSync(path.join(root,'road-events-v1/post_event_routes.json'),'utf8'));
const targets=[1306,1389];
const rows=[];
for(const n of targets){
  const candidate=source.completedRoutes.find(x=>x.level===n);
  if(!candidate)throw Error(`Missing known shortcut ${n}`);
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired)throw Error(`Unexpected repair dependency ${n}`);
  for(let i=1;i<candidate.route.length-1;i++)
    if(!api.move(candidate.route[i]))throw Error(`Known shortcut ${n} unexpectedly blocked at ${i}`);
  const before=api.getState();
  if(!level.networkCircuitRequired||before.mask!==(1<<level.homes.length)-1||
     before.networkCharged||before.overloadCrossed||before.transferCollected||
     api.move(candidate.route.at(-1)))throw Error(`Known network bypass still clears ${n}`);
  const finish=api.getState();
  if(finish.done||finish.failed)throw Error(`Bypass outcome wrong ${n}`);
  api.choose(n);api.begin();
  const authored=references[n-1001].route;
  for(let i=1;i<authored.length;i++)if(!api.move(authored[i].p))throw Error(`Authored circuit blocked ${n}:${i}`);
  const valid=api.getState();
  if(!valid.done||valid.failed||!valid.networkCharged||!valid.overloadCrossed||!valid.transferCollected)
    throw Error(`Authored circuit incomplete ${n}`);
  const visits=p=>candidate.route.some(q=>q[0]===p[0]&&q[1]===p[1]);
  rows.push({level:n,oldBypassSteps:candidate.steps,referenceSteps:candidate.referenceSteps,
    bypassRejected:true,authoredCircuitCompleted:true,visitsRelay:visits(level.lumenNetwork.relayTile),
    visitsVoltageGate:visits(level.lightOverloadGate.tile),
    visitsTransferReceiver:visits(level.lightTransfer.receiver)});
}
const output=path.join(root,'unresolved-network-shortcuts.json');
fs.writeFileSync(output,JSON.stringify({scope:'Former no-power bypasses now rejected by explicit three-stage network circuit objective. The authored circuit completes. Exact minima and balance remain unproven.',rows:[],resolved:rows},null,2));
console.log(JSON.stringify(rows));
