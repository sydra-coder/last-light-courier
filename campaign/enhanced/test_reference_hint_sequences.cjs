// Follow successive approved-route offers through each later level's houses.
const test=require('./test_integrated_preview.cjs');
let segments=0,bridgePrompts=0,levels=0;
for(let n=201;n<=2000;n++){
  test.choose(n);test.begin();
  const level=test.getLevel();
  if(level.repairRequired&&!test.buyFreeRepair())throw Error(`Level ${n}: required repair unavailable`);
  let guard=0;
  while(!test.getState().done&&test.getState().mask.toString(2).replace(/0/g,'').length<level.homes.length){
    if(++guard>level.homes.length+2)throw Error(`Level ${n}: hint sequence did not advance`);
    const before=test.getState(),offer=test.hint();
    if(level.lightBridgeRequiresPower&&before.active&&!before.bridgeBuilt){
      if(offer.pending||!offer.message.includes('level-provided Light Bridge'))
        throw Error(`Level ${n}: expected bridge prompt`);
      if(test.rejectHint()!==offer.hints||!test.useBridge())throw Error(`Level ${n}: bridge prompt failed`);
      bridgePrompts++;
      continue;
    }
    if(!offer.pending||offer.approveHidden)throw Error(`Level ${n}: missing segment after ${guard-1} deliveries: ${offer.title}`);
    if(test.rejectHint()!==offer.hints)throw Error(`Level ${n}: rejection spent a hint`);
    for(let i=1;i<offer.pending.route.length;i++)
      if(!test.move(offer.pending.route[i].p))throw Error(`Level ${n}: segment ${guard}, step ${i} blocked`);
    if(!test.getState().done&&test.getState().mask===before.mask)
      throw Error(`Level ${n}: segment ${guard} did not advance to a house`);
    segments++;
  }
  levels++;
}
console.log(`PASS: ${segments} successive verified house segments across ${levels} levels; ${bridgePrompts} no-cost bridge prompts`);
