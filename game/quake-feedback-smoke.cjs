const path=require('node:path');
const fs=require('node:fs');
const {chromium}=require('playwright');

(async()=>{
  const route=JSON.parse(fs.readFileSync(path.join(__dirname,'../campaign/enhanced/reference-hints-v1/normalized_routes.json'),'utf8'))[600].map(step=>step.slice(0,2));
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    const reached=await page.evaluate(steps=>{
      __campaign.choose(801);__integratedShell.enterBoard();
      for(let i=1;i<steps.length;i++){
        if(!__campaign.move(steps[i]))throw Error('Recorded route rejected at move '+i);
        if(__campaign.getState().quakeTriggered)return i;
      }
      return 0;
    },route);
    if(!reached)throw Error('Earthquake did not trigger on the first house');
    await page.waitForFunction(()=>!document.getElementById('quakeBanner').hidden);
    if(!await page.locator('#playScreen.quakeHit').count())throw Error('Persistent quake marker missing');
    if(!await page.locator('body.quakeShaking').count())throw Error('Screen shake missing');
    await page.locator('#quakeLogButton').click();
    const log=await page.locator('.quakeLog').innerText();
    if(!log.includes('Road closes')||!log.includes('Open → Blocked')||!log.includes('Road opens')||!log.includes('Blocked → Open'))throw Error('Before/after quake roads missing: '+log);
    if(!log.includes('Column 8, row 2')||!log.includes('Column 9, row 3'))throw Error('Level 801 quake coordinates missing: '+log);
    if(await page.locator('.quakeLogRoad').count()!==6||!log.includes('Verified route:'))throw Error('Random quake pattern or live light check missing: '+log);
    await page.screenshot({path:path.join(__dirname,'quake-log-review.png')});
    await page.locator('.quakeLogRoad button').first().click();
    if(!await page.locator('#integratedOverlay').evaluate(el=>el.hidden))throw Error('View did not return to the board');
    await page.evaluate(step=>__campaign.move(step),route[reached+1]);
    if(await page.locator('#quakeBanner').evaluate(el=>el.hidden))throw Error('Banner vanished too early');
    await page.waitForTimeout(3300);
    if(!await page.locator('#quakeBanner').evaluate(el=>el.hidden))throw Error('Banner did not clear');
    if(!await page.locator('#playScreen.quakeHit').count())throw Error('Quake marker vanished');
    await page.evaluate(()=>__campaign.reset());
    await page.waitForFunction(()=>!document.getElementById('playScreen').classList.contains('quakeHit'));
    await page.evaluate(({reached,route})=>{document.body.classList.add('reduceMotion');for(let i=1;i<=reached;i++)__campaign.move(route[i])},{reached,route});
    await page.waitForFunction(()=>!document.getElementById('quakeBanner').hidden);
    const motion=await page.locator('.shell').evaluate(el=>getComputedStyle(el).animationDuration);
    if(parseFloat(motion)>0.01)throw Error('Reduce Motion did not suppress the shake: '+motion);
    await page.locator('#quakeLogButton').click();
    await page.locator('#quakePatternSelect').selectOption('801-3');
    await page.locator('[data-quake-replay]').click();
    if((await page.evaluate(()=>__campaign.getState().mask))!==0)throw Error('Pattern replay did not reset the map');
    const selected=await page.evaluate(({reached,route})=>{for(let i=1;i<=reached;i++)__campaign.move(route[i]);return __campaign.getState().quakePilot?.variant},{reached,route});
    if(selected!=='801-3')throw Error('Pattern picker selected '+selected);
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS first-house quake shake, before/after log, pattern replay, reset, reduced motion');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
