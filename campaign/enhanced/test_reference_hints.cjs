// Validate replayed-route hint offers, rejection, and safe next-house segments.
const test=require('./test_integrated_preview.cjs');
let offered=0;
for(let n=201;n<=2000;n++){
  test.choose(n);test.begin();
  const level=test.getLevel();
  if(level.repairRequired&&!test.buyFreeRepair())throw Error(`Level ${n}: free repair unavailable`);
  const before=test.getState();
  const offer=test.hint();
  if(!offer.pending||offer.approveHidden||!offer.message.includes('not claimed shortest'))
    throw Error(`Level ${n}: verified hint missing at start: ${offer.title}`);
  if(test.rejectHint()!==offer.hints)throw Error(`Level ${n}: rejection spent a hint`);
  if(offer.pending.route[0].p[0]!==before.pos[0]||offer.pending.route[0].p[1]!==before.pos[1])
    throw Error(`Level ${n}: hint starts elsewhere`);
  for(let i=1;i<offer.pending.route.length;i++)
    if(!test.move(offer.pending.route[i].p))throw Error(`Level ${n}: hint move ${i} blocked`);
  if(test.getState().mask===before.mask&&!test.getState().done)
    throw Error(`Level ${n}: hint did not reach a house or depot`);
  if(!test.getState().done&&test.getState().mask.toString(2).replace(/0/g,'').length<level.homes.length){
    if(level.lightBridgeRequiresPower&&!test.getState().bridgeBuilt){
      const buildFirst=test.hint();
      if(buildFirst.pending||!buildFirst.approveHidden||!buildFirst.message.includes('level-provided Light Bridge'))
        throw Error(`Level ${n}: bridge action was not explained before hinting`);
      if(test.rejectHint()!==buildFirst.hints||!test.useBridge())
        throw Error(`Level ${n}: bridge prompt spent a hint or bridge charge failed`);
    }
    const followUp=test.hint();
    if(!followUp.pending||followUp.approveHidden)
      throw Error(`Level ${n}: next-house hint missing after first delivery: ${followUp.title}`);
    if(test.rejectHint()!==followUp.hints)throw Error(`Level ${n}: follow-up rejection spent a hint`);
  }
  offered++;
}
test.choose(201);test.begin();
if(!test.usePower('reveal_pulse'))throw Error('Could not alter sample route');
const altered=test.hint();
if(altered.pending||!altered.approveHidden||test.rejectHint()!==altered.hints)
  throw Error('Altered state was offered an unsupported hint or spent one');
console.log(`PASS: ${offered} verified later hints reach a house or depot; rejection and altered states spend none; 100 bridge hints resume after build`);
