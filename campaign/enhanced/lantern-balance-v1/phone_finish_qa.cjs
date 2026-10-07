// Complete balanced late maps in the rendered 390px browser UI.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../../..');
const preview=path.resolve(process.env.LLC_PREVIEW_PATH||path.join(root,'design/campaign-2000-preview/index.html'));
const routes=JSON.parse(fs.readFileSync(path.join(root,'campaign/enhanced/reference-hints-v1/route_overrides.json'),'utf8'));
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    const errors=[],rows=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('console',e=>{if(e.type()==='error')errors.push(e.text())});
    await page.goto(pathToFileURL(preview).href,{waitUntil:'load'});
    const intro=page.locator('[data-action="start"]');
    if(await intro.isVisible())await intro.click();
    await page.locator('#menuLevelOne').click();
    for(const n of [1414,1483,1485,1487,1508,1540,1549,1551,1610,1612,1626,1672,1680,1694,1698,1708,1711,1716,1775,1793,1807,1828,1873,1940,1980,1994]){
      const mapAction=page.locator('#board .boardOverlay [data-action="map"]');
      if(await mapAction.isVisible())await mapAction.click();
      else await page.locator('#levels').click();
      await page.locator('#jumpLevel').fill(String(n));
      await page.locator('#jumpGo').click();
      if(await intro.isVisible())await intro.click();
      if(n===1775){
        await page.locator('#bottomNav [data-screen="repairs"]').click();
        await page.locator('#buyRepair').click();
        await page.locator('#bottomNav [data-screen="play"]').click();
      }
      const route=routes[n];
      const result=await page.evaluate(points=>{
        for(let i=1;i<points.length;i++){
          const [x,y]=points[i];
          const cell=document.querySelector(`#board .cell[data-x="${x}"][data-y="${y}"]`);
          if(!cell)throw Error(`missing cell ${x},${y}`);
          cell.click();
          const turn=Number(document.getElementById('turns').textContent.match(/\d+/)?.[0]);
          if(turn!==i)throw Error(`move ${i} rejected at ${x},${y}; turn ${turn}`);
        }
        const overlay=document.querySelector('#board .boardOverlay');
        return {light:Number(document.getElementById('light').textContent),
          overlay:overlay?.textContent||'',rating:overlay?.querySelector('.finishStars')?.getAttribute('aria-label'),
          width:document.documentElement.scrollWidth};
      },route);
      const expectedLight=({1483:18,1610:18})[n]??16;
      if(result.light!==expectedLight||result.rating!=='5 out of 5 stars'||!result.overlay.includes('Verified minimum')||result.width>391)
        throw Error(`${n}: phone finish mismatch ${JSON.stringify(result)}`);
      rows.push({level:n,steps:route.length-1,finishLight:result.light,pageWidth:result.width});
      await page.waitForTimeout(900);
      await page.screenshot({path:path.join(__dirname,`phone-finish-${n}.png`)});
    }
    if(errors.length)throw Error(`Browser errors: ${JSON.stringify(errors)}`);
    fs.writeFileSync(path.join(__dirname,'phone-finish-qa.json'),JSON.stringify({viewport:390,rows,errors},null,2));
    console.log(JSON.stringify({rows,errors}));
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
