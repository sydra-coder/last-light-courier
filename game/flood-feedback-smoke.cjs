const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/')+'?level=1002');
    await page.waitForFunction(()=>!!window.__campaign&&!!window.__integratedShell);
    await page.evaluate(()=>__integratedShell.enterBoard());
    const initial=await page.evaluate(()=>{
      const level=__campaign.getCurrentLevel(),tile=level.floodRoad.tile,cell=document.querySelector(`#board .cell[data-x="${tile[0]}"][data-y="${tile[1]}"]`);
      return {level:level.n,mark:cell.querySelector('.timer')?.textContent,log:!document.querySelector('#quakeLogButton').hidden};
    });
    if(initial.level!==1002||initial.mark!=='≈'||!initial.log)throw Error('Flood review did not initialize: '+JSON.stringify(initial));
    await page.evaluate(()=>{
      const level=__campaign.getCurrentLevel(),homes=new Set(level.homes.map(h=>h.p.join(',')));
      for(const tile of level.spine.slice(1)){if(!__campaign.move(tile))throw Error('Recorded route blocked before delivery at '+tile);if(homes.has(tile.join(',')))break}
    });
    await page.waitForFunction(()=>!document.querySelector('#weatherBanner').hidden);
    const triggered=await page.evaluate(()=>{
      const level=__campaign.getCurrentLevel(),state=__campaign.getState(),tile=level.floodRoad.tile,cell=document.querySelector(`#board .cell[data-x="${tile[0]}"][data-y="${tile[1]}"]`);
      return {start:state.floodStart,turns:state.turns,mark:cell.querySelector('.timer')?.textContent,visible:!document.querySelector('#weatherBanner').hidden,history:__campaign.feedbackHistory()};
    });
    if(triggered.start===null||triggered.mark!=='≈4'||!triggered.visible||!triggered.history.includes('storm'))throw Error('Flood countdown cue missing: '+JSON.stringify(triggered));
    await page.screenshot({path:path.join(__dirname,'flood-countdown-review.png')});
    await page.locator('#quakeLogButton').click();
    const before=await page.locator('.quakeLogRoads').innerText();
    if(!before.includes('Low road')||!before.includes('Wind blocks'))throw Error('Event log missing changed roads: '+before);
    await page.screenshot({path:path.join(__dirname,'flood-log-review.png')});
    await page.keyboard.press('Escape');
    await page.evaluate(()=>{
      const level=__campaign.getCurrentLevel(),offset=level.spine.findIndex((p,i)=>i>0&&level.homes.some(h=>h.p.join(',')===p.join(',')));
      for(const tile of level.spine.slice(offset+1,offset+5))if(!__campaign.move(tile))throw Error('Recorded route blocked during countdown at '+tile);
    });
    await page.waitForFunction(()=>document.querySelector('#weatherBanner strong').textContent.includes('FLOODED'));
    const flooded=await page.evaluate(()=>{
      const level=__campaign.getCurrentLevel(),tile=level.floodRoad.tile,cell=document.querySelector(`#board .cell[data-x="${tile[0]}"][data-y="${tile[1]}"]`);
      return {mark:cell.querySelector('.timer')?.textContent,wall:cell.classList.contains('wall'),banner:document.querySelector('#weatherBanner strong').textContent,history:__campaign.feedbackHistory()};
    });
    if(flooded.mark!=='✕'||!flooded.wall||!flooded.banner.includes('FLOODED')||!flooded.history.includes('flood'))throw Error('Flood closure cue missing: '+JSON.stringify(flooded));
    await page.screenshot({path:path.join(__dirname,'flood-closure-review.png')});
    await page.locator('#quakeLogButton').click();
    const after=await page.locator('.quakeLogRoads').innerText();
    if(!after.includes('Open → Open → Blocked'))throw Error('Flood log missing before/after closure: '+after);
    await page.screenshot({path:path.join(__dirname,'flood-log-after-review.png')});
    if(errors.length)throw Error(errors.join(' | '));
    console.log('PASS flood countdown, screen cue, sound event, closure and before/after log');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
