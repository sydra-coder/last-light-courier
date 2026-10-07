// Check generated early minimum lookup and unrated later completion copy.
const fs=require('fs');
const path=require('path');
const vm=require('vm');
const html=fs.readFileSync(process.env.LLC_PREVIEW_PATH?path.resolve(process.env.LLC_PREVIEW_PATH):path.resolve(__dirname,'../../design/campaign-2000-preview/index.html'),'utf8');
const a=html.indexOf('const EARLY_MINIMA='),b=html.indexOf('function shortestSafeRoute(targetMask){',a);
const tail=html.indexOf('routeCache.set(cacheKey,null);return null;',b);
const end=tail<0?-1:html.indexOf('}',tail)+1;
if(a<0||b<0||end<0)throw Error('Generated minimum lookup missing');
const source=html.slice(a,end);
const early=JSON.parse(fs.readFileSync(path.join(__dirname,'early-winding-v1','shortest_routes.json'),'utf8'));
let repaired=false;
const ctx={level:{n:101,homes:Array(7)},state:{powerUsed:false,trapTile:null},repaired:()=>repaired,
  save:{repairs:{}},LEVELS:[],routeCache:new Map()};
vm.runInNewContext(source+'\nthis.lookup=shortestSafeRoute;this.minimum=minimumForLevel;',ctx);
function expect(actual,wanted,label){if(actual!==wanted)throw Error(`${label}: ${actual} != ${wanted}`)}
expect(ctx.lookup(127),early[0].steps,'101 exact');
expect(ctx.minimum(101,false),early[0].steps,'101 menu minimum');
ctx.state.powerUsed=true;expect(ctx.lookup(127),null,'powered run is unrated');ctx.state.powerUsed=false;
ctx.level.n=125;repaired=true;expect(ctx.lookup(127),early[24].steps,'125 free repair exact');
repaired=false;expect(ctx.lookup(127),null,'125 without repair');
expect(ctx.minimum(125,true),early[24].steps,'125 repaired menu minimum');
expect(ctx.minimum(125,false),null,'125 no-repair menu minimum');
ctx.level.n=201;expect(ctx.lookup(127),null,'201 unknown minimum');
expect(ctx.minimum(201,false),null,'201 menu unknown minimum');
const late=JSON.parse(fs.readFileSync(process.env.LLC_EXACT_CERT_PATH||path.join(__dirname,'event-aware-exact-minima-late.json'),'utf8')).certified;
for(const proof of late){
  ctx.level.n=proof.level;ctx.level.homes=Array(7);
  expect(ctx.lookup(127),proof.exactNoPowerSteps,`${proof.level} exact`);
  expect(ctx.minimum(proof.level,false),proof.exactNoPowerSteps,`${proof.level} menu minimum`);
  expect(ctx.minimum(proof.level,true),null,`${proof.level} repaired menu unrated`);
  repaired=true;expect(ctx.lookup(127),null,`${proof.level} repaired run unrated`);repaired=false;
  ctx.state.powerUsed=true;expect(ctx.lookup(127),null,`${proof.level} powered run unrated`);ctx.state.powerUsed=false;
}
const transit=JSON.parse(fs.readFileSync(path.join(__dirname,'transit-v1/exact_transit_minima.json'),'utf8')).certified;
for(const proof of transit){
  ctx.level.n=proof.level;ctx.level.homes=Array(7);repaired=proof.freeRepairRequired;
  expect(ctx.lookup(127),proof.exactSteps,`${proof.level} transit exact`);
  expect(ctx.minimum(proof.level,repaired),proof.exactSteps,`${proof.level} transit menu minimum`);
  expect(ctx.minimum(proof.level,!repaired),null,`${proof.level} wrong repair state unrated`);
  repaired=!proof.freeRepairRequired;expect(ctx.lookup(127),null,`${proof.level} wrong repair run unrated`);
  repaired=proof.freeRepairRequired;ctx.state.powerUsed=true;
  expect(ctx.lookup(127),null,`${proof.level} powered run unrated`);ctx.state.powerUsed=false;repaired=false;
}
const signal=JSON.parse(fs.readFileSync(path.join(__dirname,'phase-choices-v1/exact_signal_minima.json'),'utf8')).certified;
const defaultExact=new Map(late.map(p=>[p.level,p.exactNoPowerSteps]));
for(const proof of signal){
  ctx.level.n=proof.level;ctx.level.homes=Array(7);repaired=proof.freeRepairRequired;ctx.state.phaseSignal=true;
  expect(ctx.lookup(127),proof.exactSignalSteps,`${proof.level} signal exact`);
  expect(ctx.minimum(proof.level,repaired,true),proof.exactSignalSteps,`${proof.level} signal menu minimum`);
  const unsignaled=repaired?null:(defaultExact.get(proof.level)??null);
  expect(ctx.minimum(proof.level,repaired,false),unsignaled,`${proof.level} unsignaled menu minimum`);
  ctx.state.phaseSignal=false;expect(ctx.lookup(127),unsignaled,`${proof.level} unsignaled run minimum`);
  ctx.state.phaseSignal=true;ctx.state.powerUsed=true;expect(ctx.lookup(127),null,`${proof.level} powered signal unrated`);
  ctx.state.powerUsed=false;ctx.state.phaseSignal=false;repaired=false;
}
if(html.includes('Shortest route unavailable')||!html.includes('Route completed; no verified minimum'))
  throw Error('Unrated completion copy is stale');
console.log('PASS: exact 101–200, certified late, transit and signal minima, repair/power guards, and honest unrated completion copy');
