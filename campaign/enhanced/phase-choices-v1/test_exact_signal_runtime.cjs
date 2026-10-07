const fs=require('fs'),path=require('path');
const api=require('../test_integrated_preview.cjs');
const root=path.resolve(__dirname,'..');
const proofs=JSON.parse(fs.readFileSync(path.join(__dirname,'exact_signal_minima.json'),'utf8')).certified;
for(const proof of proofs){
  const n=proof.level;
  api.choose(n);api.begin();
  if(api.minimum()!==null)throw Error(`${n}: default branch was rated as signal branch`);
  api.choose(n);api.begin();
  if(proof.freeRepairRequired&&!api.buyFreeRepair())throw Error(`${n}: free repair unavailable`);
  if(!api.signal())throw Error(`${n}: signal unavailable`);
  const band=(n-1)/100|0;
  const start=band*100+1;
  const report=JSON.parse(fs.readFileSync(path.join(root,`event-aware-${start}-${start+99}-signal-replay.json`),'utf8'));
  const route=report.completedRoutes.find(x=>x.level===n).route;
  for(let i=1;i<route.length;i++)if(!api.move(route[i]))throw Error(`${n}: route blocked at ${i}`);
  const finish=api.getState();
  if(!finish.done||finish.failed||finish.turns!==proof.exactSignalSteps||api.minimum()!==proof.exactSignalSteps)
    throw Error(`${n}: runtime completion minimum mismatch`);
}
console.log('PASS: exact signal branches 1804 and 1900 complete and rate at certified minima; defaults remain unrated');
