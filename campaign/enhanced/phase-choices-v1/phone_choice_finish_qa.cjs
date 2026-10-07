const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../../..');
const preview=path.join(root,'design/campaign-2000-preview/index.html');
const defaults=JSON.parse(fs.readFileSync(path.join(root,'campaign/enhanced/reference-hints-v1/normalized_routes.json')));
const signals=JSON.parse(fs.readFileSync(path.join(root,'campaign/enhanced/reference-hints-v1/normalized_signal_routes.json')));
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    const errors=[],rows=[];page.on('pageerror',e=>errors.push(String(e)));
    await page.goto(pathToFileURL(preview).href,{waitUntil:'load'});
    const firstIntro=page.locator('[data-action="start"]');if(await firstIntro.isVisible())await firstIntro.click();
    await page.locator('#menuLevelOne').click();
    for(const [n,branch,expectedSteps,expectedLight] of [[1804,'default',62,14],[1804,'signal',60,16],[1900,'default',118,12],[1900,'signal',110,20]]){
      const intro=page.locator('[data-action="start"]');if(await intro.isVisible())await intro.click();
      const mapAction=page.locator('#board .boardOverlay [data-action="map"]');
      if(await mapAction.isVisible())await mapAction.click();else await page.locator('#levels').click();
      await page.locator('#jumpLevel').fill(String(n));await page.locator('#jumpGo').click();
      if(await intro.isVisible())await intro.click();
      if(n===1900){await page.locator('#bottomNav [data-screen="repairs"]').click();if(await page.locator('#buyRepair').isEnabled())await page.locator('#buyRepair').click();await page.locator('#bottomNav [data-screen="play"]').click()}
      if(branch==='signal')await page.locator('#sendPhaseSignal').click();
      const route=(branch==='signal'?signals[n]:defaults[n-201]);
      const result=await page.evaluate(points=>{
        for(let i=1;i<points.length;i++){
          const [x,y]=points[i],cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
          if(!cell)throw Error(`Missing cell ${x},${y}`);cell.click();
          const turn=Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
          if(turn!==i)throw Error(`Move ${i} rejected; turn ${turn}`);
        }
        const overlay=document.querySelector('#board .boardOverlay');
        return {light:Number(document.getElementById('light').textContent),text:overlay?.textContent||'',
          rating:overlay?.querySelector('.finishStars')?.getAttribute('aria-label'),width:document.documentElement.scrollWidth};
      },route);
      if(route.length-1!==expectedSteps||result.light!==expectedLight||result.width>391||!(branch==='signal'?result.text.includes('Verified minimum'):result.text.includes('Route complete')))
        throw Error(`${n} ${branch}: ${JSON.stringify(result)}`);
      if(branch==='signal'&&result.rating!=='5 out of 5 stars')throw Error(`${n} signal exact rating wrong: ${result.rating}`);
      rows.push({level:n,branch,steps:expectedSteps,finishLight:result.light,width:result.width,rating:result.rating});
      await page.waitForTimeout(900);
      await page.screenshot({path:path.join(__dirname,`phone-choice-${n}-${branch}.png`)});
    }
    if(errors.length)throw Error(`Browser errors ${JSON.stringify(errors)}`);
    fs.writeFileSync(path.join(__dirname,'phone_choice_finish_qa.json'),JSON.stringify({viewport:390,rows,errors},null,2));
    console.log(JSON.stringify({rows,errors}));
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
