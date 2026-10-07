// Test the shop and charge policy without browser UI dependencies.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const shop={innerHTML:'',querySelector:()=>null,addEventListener(_type,handler){this.onClick=handler}};
let persists=0,renders=0;
const ctx={
  save:{wallet:500,cleared:{},powerUnlocked:{},powerStock:{}},
  level:{n:101,reviewPower:'anchor_trap'},state:{},
  $:id=>id==='powerShop'?shop:null,
  persist:()=>persists++,render:()=>renders++,setStatus:()=>{}
};
const source=fs.readFileSync(path.join(__dirname,'power-economy.js'),'utf8');
vm.runInNewContext(source+'\nthis.policy={syncPowerUnlocks,powerChargeSource,consumePowerCharge,renderPowerShop};',ctx);
const p=ctx.policy;
if(p.powerChargeSource('anchor_trap')!=='review')throw Error('Assigned sample lacks a review charge');
if(p.powerChargeSource('decoy_light')!==null)throw Error('Unassigned locked tool got a free charge');
p.renderPowerShop();
if(!shop.innerHTML.includes('Unlock by clearing Level 100'))throw Error('Locked tool not labeled');
shop.onClick({target:{closest:()=>({dataset:{buyPower:'anchor_trap'}})}});
if(ctx.save.wallet!==500)throw Error('Shop sold locked tool');
ctx.save.cleared[100]=true;p.syncPowerUnlocks();
if(!ctx.save.powerUnlocked.anchor_trap||ctx.save.powerStock.anchor_trap!==2)throw Error('Milestone grant failed');
p.syncPowerUnlocks();
if(ctx.save.powerStock.anchor_trap!==2)throw Error('Milestone grant repeated');
if(!p.consumePowerCharge('anchor_trap')||ctx.save.powerStock.anchor_trap!==2)throw Error('Assigned sample spent earned stock');
ctx.level={n:102,reviewPower:null};
if(!p.consumePowerCharge('anchor_trap')||ctx.save.powerStock.anchor_trap!==1)throw Error('Inventory charge not spent');
p.renderPowerShop();
shop.onClick({target:{closest:()=>({dataset:{buyPower:'anchor_trap'}})}});
if(ctx.save.wallet!==380||ctx.save.powerStock.anchor_trap!==2)throw Error('Earned restock purchase failed');
ctx.save.powerStock.anchor_trap=0;
if(p.powerChargeSource('anchor_trap')!==null)throw Error('Empty earned tool should be unavailable');
ctx.level={n:101,reviewPower:'anchor_trap'};
if(p.powerChargeSource('anchor_trap')!=='review')throw Error('Assigned sample unavailable after stock was spent');
ctx.level={n:701,reviewPower:'light_bridge',lightBridgeRequiresPower:true};
if(p.powerChargeSource('light_bridge')!=='level')throw Error('Required bridge lacks guaranteed charge');
if(!p.consumePowerCharge('light_bridge')||ctx.save.wallet!==380)throw Error('Required bridge incorrectly spent wallet');
if(persists<3||renders<1)throw Error('Save or UI refresh missing');
console.log('PASS: milestone grants, locked shop, stock use, restock and required bridge policy');
