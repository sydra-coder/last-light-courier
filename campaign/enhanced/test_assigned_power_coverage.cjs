// Keep the compact playtest index and generated preview's sample tools aligned.
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const rows=JSON.parse(fs.readFileSync(path.join(__dirname,'playtest_rows.json'),'utf8')).rows;
const names={anchor_trap:'Anchor Trap x1',decoy_light:'Decoy Light x1',reveal_pulse:'Reveal Pulse x1',
  light_bridge:'Light Bridge x1',freeze_seal:'Freeze Seal x1',rewind:'Rewind x1',
  lumen_flask:'Lumen Flask x1',road_repair:'Road Repair x1',map_stabilizer:'Map Stabilizer x1'};
if(rows.length!==2000||api.LEVELS.length!==2000)throw Error('Campaign length mismatch');
for(let i=0;i<2000;i++){
  const n=i+1,power=api.LEVELS[i].reviewPower,listed=rows[i][6];
  if((power?names[power]:'None')!==listed)throw Error(`Level ${n}: workbook says ${listed}; preview says ${power||'None'}`);
  if(n>=1001&&!(n>=1401&&n<=1500)){
    const expected=['lumen_flask','road_repair','map_stabilizer'][(n-1001)%3];
    if(power!==expected)throw Error(`Level ${n}: sample tool cycle lost`);
  }
}
api.choose(1003);api.begin();
if(!api.usePower('map_stabilizer')||api.powerReady('map_stabilizer'))throw Error('Review charge not limited to one use per run');
api.choose(1003);api.begin();
if(!api.powerReady('map_stabilizer'))throw Error('Review charge did not return on restart');
console.log('PASS: all 2,000 preview sample tools match the playtest workbook');
