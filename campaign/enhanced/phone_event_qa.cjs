// Trigger representative authored map events through the rendered browser UI.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
const preview=path.resolve(process.env.LLC_PREVIEW_PATH||path.join(root,'design/campaign-2000-preview/index.html'));
const stageName=process.env.LLC_EVENT_QA_NAME||'phone-event';
const archive=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'))).levels;
const quakes=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'quakes-v1/post_event_routes.json'))).map(x=>[x.level,x]));
const roads=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'))).map(x=>[x.level,x]));
const signalRoutes=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'candidates-v3/ROUTES_1001_2000_BASELINE.json'))).map(x=>[x.level,x.solutions[0].route]));
const checks=[
  {n:801,name:'earthquake',deliveries:1},
  {n:951,name:'aftershock',deliveries:2},
  {n:1001,name:'storm and flood',deliveries:1},
  {n:1014,name:'salient road closure',deliveries:1},
  {n:1101,name:'nightfall and day/night',deliveries:1},
  {n:1201,name:'shadow spawner',deliveries:1},
  {n:1301,name:'light network',deliveries:1},
  {n:1306,name:'required circuit',deliveries:1},
  {n:1389,name:'required circuit with eight houses',deliveries:1},
  {n:1404,name:'arsenal road close',deliveries:1},
  {n:1459,name:'salient arsenal closure',deliveries:1},
  {n:1414,name:'balanced winding route',deliveries:1},
  {n:1483,name:'balanced winding route',deliveries:1},
  {n:1485,name:'balanced winding route',deliveries:1},
  {n:1487,name:'balanced winding route',deliveries:1},
  {n:1304,name:'foundry road close',deliveries:1},
  {n:1210,name:'prism road close',deliveries:1},
  {n:1112,name:'nightfall road close',deliveries:1},
  {n:1007,name:'storm road close',deliveries:1},
  {n:1501,name:'convergence field',deliveries:1},
  {n:1508,name:'convergence road close',deliveries:1},
  {n:1601,name:'chain event',deliveries:2},
  {n:1701,name:'transit',deliveries:1},
  {n:1708,name:'express transit',deliveries:1},
  {n:1711,name:'express transit',deliveries:1},
  {n:1716,name:'express transit',deliveries:1},
  {n:1775,name:'express transit',deliveries:1},
  {n:1793,name:'express transit',deliveries:1},
  {n:1704,name:'transit road close',deliveries:1},
  {n:1804,name:'certified signal phase closure',deliveries:1},
  {n:1801,name:'route choice',deliveries:1},
  {n:1802,name:'paired phase default',deliveries:1},
  {n:1802,name:'paired phase signal',deliveries:1,signal:true},
  {n:1927,name:'finale phase signal',deliveries:1,signal:true},
  {n:1922,name:'salient finale closure',deliveries:1},
  {n:1994,name:'certified finale phase closure',deliveries:1},
  {n:1901,name:'finale',deliveries:2}
];
const popcount=x=>x.toString(2).replace(/0/g,'').length;
function route(n){return n>1000?roads.get(n).route:quakes.get(n)?.route||archive[n-1].solutions[0].route}
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  const errors=[],rows=[];
  page.on('pageerror',e=>errors.push(e.stack||String(e)));
  page.on('console',e=>{if(e.type()==='error')errors.push(e.text())});
  await page.goto(pathToFileURL(preview).href,{waitUntil:'load'});
  const intro=page.locator('[data-action="start"]');
  if(await intro.isVisible())await intro.click();
  await page.locator('#menuLevelOne').click();
  for(const test of checks.filter(x=>!process.env.LLC_EVENT_LEVEL||x.n===Number(process.env.LLC_EVENT_LEVEL))){
    await page.locator('#levels').click();
    await page.locator('#jumpLevel').fill(String(test.n));
    await page.locator('#jumpGo').click();
    if(await intro.isVisible())await intro.click();
    if([1775].includes(test.n)){
      await page.locator('#bottomNav [data-screen="repairs"]').click();
      await page.locator('#buyRepair').click();
      await page.locator('#bottomNav [data-screen="play"]').click();
    }
    if(test.signal){
      const signalButton=page.locator('#sendPhaseSignal');
      if(!await signalButton.isVisible()||!await signalButton.isEnabled())throw Error(`Level ${test.n}: phase signal unavailable in browser`);
      await signalButton.click();
    }
    const steps=test.signal?signalRoutes.get(test.n):route(test.n),trigger=steps.findIndex(s=>popcount(s.mask)>=test.deliveries);
    if(trigger<1)throw Error(`Level ${test.n}: no ${test.deliveries}-delivery checkpoint`);
    const result=await page.evaluate(points=>{
      for(let i=1;i<points.length;i++){
        const [x,y]=points[i];
        const cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
        if(!cell)throw Error(`missing cell ${x},${y}`);
        cell.click();
        const turn=Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
        if(turn!==i)throw Error(`move ${i} rejected at ${x},${y}; turn ${turn}`);
      }
      return {turns:document.getElementById('turns').textContent,houses:document.getElementById('housesLit').textContent,
        eventWalls:document.querySelectorAll('#board .cell.eventRoad.wall').length,
        quakeWalls:document.querySelectorAll('#board .cell.quakeClose.wall').length,
        influence:document.querySelectorAll('#board .cell.influenceActive').length,
        visibleCells:document.querySelectorAll('#board .cell').length};
    },steps.slice(0,trigger+1).map(x=>x.p));
    rows.push({...test,trigger,...result});
    if([801,1001,1007,1014,1112,1210,1304,1306,1389,1404,1414,1459,1483,1485,1487,1501,1508,1601,1704,1708,1711,1716,1775,1793,1802,1804,1901,1922,1927,1994].includes(test.n))await page.screenshot({path:path.join(__dirname,`${stageName}-${test.n}${test.signal?'-signal':''}.png`)});
  }
  const report={viewport:{width:390,height:844},cases:rows,errors};
  fs.writeFileSync(path.join(__dirname,`${stageName}-qa-report.json`),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
  if(errors.length||rows.some(r=>r.visibleCells===0))process.exitCode=1;
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
