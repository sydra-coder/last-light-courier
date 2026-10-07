// Real-browser touch controls and navigation smoke test on representative maps.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/rahul/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  const errors=[],rows=[];
  page.on('pageerror',e=>errors.push(e.stack||String(e)));
  page.on('console',e=>{if(e.type()==='error')errors.push(e.text())});
  await page.goto(pathToFileURL(path.resolve(__dirname,'../../design/campaign-2000-preview/index.html')).href,{waitUntil:'load'});
  const intro=page.locator('[data-action="start"]');
  if(await intro.isVisible())await intro.click();
  await page.locator('#menuLevelOne').click();
  for(const n of [1,1001,1501,2000]){
    if(n!==1){
      await page.locator('#levels').click();
      await page.locator('#jumpLevel').fill(String(n));
      await page.locator('#jumpGo').click();
    }
    if(await intro.isVisible())await intro.click();
    const safe=page.locator('#board .cell.safe');
    const safeCount=await safe.count();
    if(!safeCount)throw Error(`Level ${n}: no safe neighboring tile`);
    const before=await page.locator('#turns').textContent();
    await safe.first().click();
    const after=await page.locator('#turns').textContent();
    if(!/0 moves/.test(before)||!/1 move/.test(after))throw Error(`Level ${n}: tap did not move (${before} -> ${after})`);
    await page.locator('#retry').click();
    const restarted=await page.locator('#turns').textContent();
    if(!/0 moves/.test(restarted))throw Error(`Level ${n}: restart failed (${restarted})`);
    const zoom=page.locator('#zoomMap');
    const beforeZoom=await zoom.getAttribute('aria-pressed');
    await zoom.click();
    const afterZoom=await zoom.getAttribute('aria-pressed');
    if(beforeZoom===afterZoom)throw Error(`Level ${n}: zoom failed`);
    await page.locator('#levels').click();
    await page.locator('#jumpLevel').fill(String(n));
    const routeTitle=await page.locator('#routeBookTitle').textContent();
    const routeFeatures=await page.locator('#routeBookFeatures').textContent();
    if(!routeTitle.includes(`Level ${n}`)||!routeFeatures.trim())throw Error(`Level ${n}: route book missing`);
    await page.locator('#pickerClose').click();
    rows.push({n,safeCount,before,after,restarted,beforeZoom,afterZoom,routeTitle});
  }
  const report={viewport:{width:390,height:844},levels:rows,errors};
  fs.writeFileSync(path.join(__dirname,'phone-interaction-qa-report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({levels:rows.length,errors,rows}));
  if(errors.length)process.exitCode=1;
  await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
