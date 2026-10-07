const assert = require('node:assert/strict');
const {spawn} = require('node:child_process');
const {unlinkSync, existsSync} = require('node:fs');
const path = require('node:path');
const base = 'http://127.0.0.1:18787';
const file = path.join(__dirname, 'results-dev.json');
if (existsSync(file)) throw new Error('Move existing results-dev.json before this test');
const child = spawn(process.execPath,[path.join(__dirname,'results-server.cjs')],{env:{...process.env,PORT:'18787'},stdio:'ignore'});
const request = async (url,method='GET',body) => {
  const response=await fetch(base+url,{method,headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});
  return {status:response.status,data:await response.json()};
};
(async()=>{
  for(let i=0;i<30;i++){try{await request('/health');break}catch{await new Promise(r=>setTimeout(r,100))}}
  const player=(await request('/players','POST')).data;
  const run={playerId:player.id,levelId:1,rulesRevision:2,lightSpent:20,steps:20,allHomes:true,hintsUsed:0,repairUsed:false};
  assert.equal((await request('/runs','POST',run)).status,200);
  assert.equal((await request('/runs','POST',{...run,lightSpent:22,steps:22})).data.personalBest.lightSpent,20);
  assert.equal((await request('/runs','POST',{...run,lightSpent:18,steps:18})).data.globalBest.lightSpent,18);
  assert.equal((await request('/runs','POST',{...run,hintsUsed:1})).status,400);
  assert.equal((await request('/levels/1/board')).data.entries.length,1);
  console.log('Results service tests passed');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>{child.kill();setTimeout(()=>{if(existsSync(file))unlinkSync(file)},150)});
