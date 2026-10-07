// Exercise each assigned courier tool through actual browser controls.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
const early=JSON.parse(fs.readFileSync(path.join(root,'design/map-solutions-1000.json'))).levels;
const late=new Map(JSON.parse(fs.readFileSync(path.join(__dirname,'road-events-v1/post_event_routes.json'))).map(x=>[x.level,x]));
const cases=[
  {n:101,power:'anchor_trap',stage:'first'},
  {n:151,power:'decoy_light',stage:'first'},
  {n:201,power:'reveal_pulse',stage:'start'},
  {n:701,power:'light_bridge',stage:'first'},
  {n:901,power:'map_stabilizer',stage:'start'},
  {n:1001,power:'lumen_flask',stage:'one'},
  {n:1002,power:'road_repair',stage:'first'},
  {n:1401,power:'freeze_seal',stage:'first'},
  {n:1402,power:'rewind',stage:'one'}
];
function route(n){return n<=1000?early[n-1].solutions[0].route:late.get(n).route}
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  const errors=[],rows=[];
  page.on('pageerror',e=>errors.push(e.stack||String(e)));
  page.on('console',e=>{if(e.type()==='error')errors.push(e.text())});
  await page.goto(pathToFileURL(path.join(root,'design/campaign-2000-preview/index.html')).href,{waitUntil:'load'});
  const intro=page.locator('[data-action="start"]');
  if(await intro.isVisible())await intro.click();
  await page.locator('#menuLevelOne').click();
  for(const test of cases){
    await page.locator('#levels').click();
    await page.locator('#jumpLevel').fill(String(test.n));
    await page.locator('#jumpGo').click();
    if(await intro.isVisible())await intro.click();
    const steps=route(test.n);
    const first=steps.findIndex(step=>step.mask);
    if(first<1)throw Error(`Level ${test.n}: missing first delivery in recorded route`);
    const until=test.stage==='start'?0:test.stage==='one'?1:first;
    let moved=await page.evaluate(points=>{
      for(let i=1;i<points.length;i++){
        const [x,y]=points[i];
        const cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
        if(!cell)throw Error(`missing cell ${x},${y}`);
        cell.click();
        const turn=Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
        if(turn!==i)throw Error(`move ${i} rejected at ${x},${y}; turn ${turn}`);
      }
      return Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
    },steps.slice(0,until+1).map(x=>x.p));
    const selector=page.locator('#selectedPower');
    if(await selector.inputValue()!==test.power)await selector.selectOption(test.power);
    const button=page.locator('#useCandidatePower');
    const enabled=await button.isEnabled();
    const lightBefore=Number(await page.locator('#light').textContent());
    const targetsBefore=await page.locator('#board .cell.trapTarget,#board .cell.decoyTarget').count();
    if(enabled)await button.click();
    let targetsAfter=await page.locator('#board .cell.trapTarget,#board .cell.decoyTarget').count();
    if(test.power==='anchor_trap'&&!targetsAfter){
      const follow=await page.evaluate(({points,offset})=>{
        for(let i=0;i<points.length;i++){
          const [x,y]=points[i];
          const cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
          if(!cell)throw Error(`missing cell ${x},${y}`);
          cell.click();
          const turn=Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
          if(turn!==offset+i+1)throw Error(`move ${offset+i+1} rejected at ${x},${y}; turn ${turn}`);
          const targets=document.querySelectorAll('#board .cell.trapTarget').length;
          if(targets)return {turn,targets};
        }
        return {turn:offset+points.length,targets:0};
      },{points:steps.slice(until+1).map(x=>x.p),offset:until});
      moved=follow.turn;targetsAfter=follow.targets;
    }
    let placed=false;
    if(enabled&&['anchor_trap','decoy_light'].includes(test.power)&&targetsAfter){
      await page.locator('#board .cell.trapTarget,#board .cell.decoyTarget').first().click();
      placed=true;
    }
    const lightAfter=Number(await page.locator('#light').textContent());
    const turnsAfter=await page.locator('#turns').textContent();
    if(test.power==='lumen_flask'&&lightAfter<=lightBefore)throw Error('Lumen Flask did not restore light');
    if(test.power==='light_bridge'&&lightAfter>=lightBefore)throw Error('Light Bridge did not cost light');
    if(test.power==='rewind'&&!/0 moves/.test(turnsAfter))throw Error('Rewind did not undo the move');
    const afterText=await page.locator('#candidatePower').innerText();
    rows.push({n:test.n,power:test.power,stage:test.stage,moved,enabled,targetsBefore,targetsAfter,placed,lightBefore,lightAfter,turnsAfter,afterText:afterText.slice(0,180)});
  }
  const report={viewport:{width:390,height:844},cases:rows,errors};
  fs.writeFileSync(path.join(__dirname,'phone-power-qa-report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
  if(errors.length||rows.some(x=>!x.enabled||(['anchor_trap','decoy_light'].includes(x.power)&&!x.placed)))process.exitCode=1;
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
