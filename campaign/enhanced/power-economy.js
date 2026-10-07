// Earn a tool by clearing its milestone. The shop only replenishes earned tools.
const POWER_CATALOG=[
  {id:'anchor_trap',name:'Anchor Trap',milestone:100,price:120},
  {id:'decoy_light',name:'Decoy Light',milestone:150,price:140},
  {id:'reveal_pulse',name:'Reveal Pulse',milestone:200,price:160},
  {id:'lumen_flask',name:'Lumen Flask',milestone:300,price:180},
  {id:'road_repair',name:'Road Repair',milestone:400,price:200},
  {id:'light_bridge',name:'Light Bridge',milestone:700,price:220},
  {id:'map_stabilizer',name:'Map Stabilizer',milestone:900,price:240},
  {id:'freeze_seal',name:'Freeze Seal',milestone:1400,price:260},
  {id:'rewind',name:'Rewind',milestone:1400,price:280}
];
function syncPowerUnlocks(){
  save.powerUnlocked??={};save.powerStock??={};
  let changed=false;
  for(const item of POWER_CATALOG){
    if(save.cleared[item.milestone]&&!save.powerUnlocked[item.id]){
      save.powerUnlocked[item.id]=true;
      save.powerStock[item.id]=(save.powerStock[item.id]||0)+2;
      changed=true;
    }
  }
  if(changed)persist();
}
function powerChargeSource(power){
  if(!power)return null;
  if(power==='light_bridge'&&level.lightBridgeRequiresPower)return 'level';
  if(power===level.reviewPower)return 'review';
  if(!save.powerUnlocked?.[power])return null;
  return (save.powerStock?.[power]||0)>0?'inventory':null;
}
function canSpendPowerCharge(power){return !!powerChargeSource(power)}
function chargeLabel(power){
  const source=powerChargeSource(power);
  return source==='level'?'level-provided charge':source==='review'?'review charge':source==='inventory'?'inventory ×'+save.powerStock[power]:'no charges';
}
function consumePowerCharge(power){
  const source=powerChargeSource(power);
  if(!source)return false;
  if(source==='inventory'){
    save.powerStock[power]--;
    persist();
  }
  state.powerSource=source;
  return true;
}
function renderPowerShop(){
  const box=$('powerShop');if(!box)return;
  const wasOpen=!!box.querySelector('details')?.open;
  syncPowerUnlocks();
  const rows=POWER_CATALOG.map(item=>{
    const earned=!!save.powerUnlocked[item.id],stock=save.powerStock[item.id]||0;
    const detail=earned?'Inventory ×'+stock:'Unlock by clearing Level '+item.milestone;
    const disabled=!earned||save.wallet<item.price;
    return '<div class="shopRow"><span><b>'+item.name+'</b><small>'+detail+'</small></span><button type="button" data-buy-power="'+item.id+'" '+(disabled?'disabled':'')+'>'+(earned?'Buy +1 · '+item.price:'Locked')+'</button></div>';
  }).join('');
  box.innerHTML='<details><summary>Earned tools and restocks</summary><p class="mini">Clear each milestone to unlock its tool and receive two charges. Points buy optional restocks after that. This review build gives the assigned sample tool one charge per run, and a required bridge provides its own charge.</p>'+rows+'</details>';
  if(wasOpen)box.querySelector('details').open=true;
}
$('powerShop').addEventListener('click',event=>{
  const button=event.target.closest('[data-buy-power]');if(!button)return;
  const item=POWER_CATALOG.find(entry=>entry.id===button.dataset.buyPower);
  if(!item||!save.powerUnlocked?.[item.id]||save.wallet<item.price)return;
  save.wallet-=item.price;
  save.powerStock[item.id]=(save.powerStock[item.id]||0)+1;
  persist();
  setStatus('Tool restocked',item.name+' +1','One charge added to your inventory for '+item.price+' banked points.');
  render();
});
syncPowerUnlocks();
