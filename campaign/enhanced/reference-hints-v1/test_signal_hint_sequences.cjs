// Every authored signal branch should offer safe next-house hints from its own state.
const api=require('../test_integrated_preview.cjs');
let levels=0,segments=0;
for(let n=1801;n<=2000;n++){
  if(!api.LEVELS[n-1].phaseChoice)continue;
  api.choose(n);api.begin();
  const level=api.getLevel();
  if(level.repairRequired&&!api.buyFreeRepair())throw Error(`${n}: required repair unavailable`);
  if(!api.signal())throw Error(`${n}: signal unavailable`);
  let guard=0;
  while(!api.getState().done&&api.getState().mask.toString(2).replace(/0/g,'').length<level.homes.length){
    if(++guard>level.homes.length+2)throw Error(`${n}: hint sequence did not advance`);
    const before=api.getState(),offer=api.hint();
    if(!offer.pending||offer.approveHidden)throw Error(`${n}: signaled segment missing: ${offer.title}`);
    if(api.rejectHint()!==offer.hints)throw Error(`${n}: rejection spent a hint`);
    for(let i=1;i<offer.pending.route.length;i++)
      if(!api.move(offer.pending.route[i].p))throw Error(`${n}: signaled hint blocked at ${i}`);
    if(!api.getState().done&&api.getState().mask===before.mask)
      throw Error(`${n}: hint did not reach a house`);
    segments++;
  }
  levels++;
}
if(levels!==125)throw Error(`Expected 125 signal branches, got ${levels}`);
console.log(`PASS: ${segments} successive signaled house segments across ${levels} branches; rejection spent no hints`);
