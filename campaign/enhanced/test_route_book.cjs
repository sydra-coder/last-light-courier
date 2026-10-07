const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
const source=script?.match(/^function renderRouteBook\(.*$/m)?.[0];
const levelLine=script?.match(/^const LEVELS=.*;$/m)?.[0];
if(!source||!levelLine||!html.includes('id="routeBook"'))throw Error('Route book missing');
if(!(html.indexOf('id="jumpLevel"')<html.indexOf('id="routeBook"')&&html.indexOf('id="routeBook"')<html.indexOf('id="pickerChapters"')))throw Error('Route book must be visible beside the jump control');
const levels=JSON.parse(levelLine.slice('const LEVELS='.length,-1));
const nodes={};
const $=id=>nodes[id]??(nodes[id]={textContent:'',dataset:{}});
const ctx={LEVELS:levels,$};
vm.runInNewContext(source+'\nthis.inspect=renderRouteBook',ctx);
for(const n of [1,101,201,301,501,701,801,1001,1201,1401,1901,2000]){
  ctx.inspect(n);
  if(!nodes.routeBookTitle.textContent.includes(`Level ${n} ·`))throw Error(`Title ${n}`);
  if(!nodes.routeBookTitle.textContent.includes(`${levels[n-1].homes.length} houses`))throw Error(`House count ${n}`);
  if(Number(nodes.routeBookPlay.dataset.routeLevel)!==n)throw Error(`Play target ${n}`);
}
for(const [n,needle] of [[201,'2×2 shadow field'],[301,'Shadow drains house light'],[701,'Light Bridge'],[801,'Quake'],[1001,'Flood'],[1113,'One-way road'],[1201,'Spawner']]){
  ctx.inspect(n);
  if(!nodes.routeBookFeatures.textContent.includes(needle))throw Error(`Level ${n}: missing ${needle}`);
}
ctx.inspect(1601);
if(!nodes.routeBookFeatures.textContent.includes('after second delivery'))throw Error('Second-delivery event timing absent');
for(let n=1;n<=2000;n++){
  ctx.inspect(n);
  if(Number(nodes.routeBookPlay.dataset.routeLevel)!==n||!nodes.routeBookTitle.textContent.includes(`${levels[n-1].homes.length} houses`))throw Error(`Route book data mismatch at ${n}`);
}
console.log('PASS: route book summarizes all 2000 maps, with representative hazard and timing checks');
