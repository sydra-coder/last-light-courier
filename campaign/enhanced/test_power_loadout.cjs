// Verify an earned optional tool and a required bridge can be used in one run.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const shop={querySelector:()=>null,addEventListener(){},innerHTML:''};
const control={addEventListener(_type,handler){this.onChange=handler},innerHTML:'',hidden:false};
const ctx={
  save:{wallet:500,cleared:{},powerUnlocked:{lumen_flask:true},powerStock:{lumen_flask:1}},
  level:{n:701,reviewPower:'light_bridge',lightBridgeRequiresPower:true,lightBridge:[1,1],bridgeCost:1},
  state:{active:true,light:5,bridgeBuilt:false,usedPowers:{},selectedPower:'lumen_flask',powerUsed:false,done:false,failed:false},
  $:id=>id==='powerShop'?shop:control,
  cap:()=>10,persist:()=>{},render:()=>{},setStatus:()=>{},
  ISO:{cancel:()=>{}},hintPath:null,
  open:()=>true,eq:(a,b)=>a&&b&&a[0]===b[0]&&a[1]===b[1]
};
const source=['power-economy.js','power-loadout.js'].map(name=>fs.readFileSync(path.join(__dirname,name),'utf8')).join('\n');
vm.runInNewContext(source+'\nthis.api={availablePowers,powerReady,renderCandidatePower,useCandidatePower};',ctx);
const p=ctx.api;
if(!p.availablePowers().includes('lumen_flask')||!p.availablePowers().includes('light_bridge'))throw Error('Loadout missing earned or assigned tool');
p.renderCandidatePower();
if(!control.innerHTML.includes('selectedPower')||!control.innerHTML.includes('Lumen Flask'))throw Error('Tool selector not rendered');
if(!p.powerReady('lumen_flask'))throw Error('Earned Flask should be ready');
p.useCandidatePower();
if(ctx.state.light!==8||ctx.save.powerStock.lumen_flask!==0||!ctx.state.usedPowers.lumen_flask)throw Error('Flask stock or effect incorrect');
if(p.powerReady('lumen_flask'))throw Error('Flask reusable without second charge');
ctx.state.selectedPower='light_bridge';
if(!p.powerReady('light_bridge'))throw Error('Required bridge blocked by previous tool use');
p.useCandidatePower();
if(!ctx.state.bridgeBuilt||ctx.state.light!==7||!ctx.state.usedPowers.light_bridge)throw Error('Bridge did not build after Flask');
if(ctx.save.wallet!==500)throw Error('Mandatory bridge spent points');
ctx.save.powerUnlocked.rewind=true;
ctx.save.powerStock.rewind=1;
ctx.state.lastMoveState={...ctx.state,bridgeBuilt:false,usedPowers:{lumen_flask:true},lastMoveState:null};
ctx.state.selectedPower='rewind';
if(!p.powerReady('rewind'))throw Error('Rewind should be ready');
p.useCandidatePower();
if(ctx.state.bridgeBuilt||ctx.state.usedPowers.light_bridge||!ctx.state.usedPowers.rewind)throw Error('Rewind did not restore required bridge eligibility');
if(!p.powerReady('light_bridge')||ctx.save.powerStock.rewind!==0)throw Error('Rewind stranded a required bridge or missed charge');
console.log('PASS: earned Flask, required bridge, and Rewind bridge restoration');
