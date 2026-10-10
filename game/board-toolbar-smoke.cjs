const path=require('node:path');
const {chromium}=require('playwright');

(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>window.__campaign&&window.__integratedShell);
    await page.evaluate(()=>{__campaign.choose(1201);__integratedShell.enterBoard()});
    if(await page.locator('#boardMessage').isVisible())throw Error('Summary strip still covers the board');
    if(await page.locator('#boardLegendButton').count())throw Error('Broken question-mark control remains');
    for(const selector of ['#focusCourier','#focusDestination','#retry'])if(await page.locator(selector).isVisible())throw Error('Redundant board control visible: '+selector);
    const zoom=page.locator('#zoomMap');
    if(!await zoom.isVisible())throw Error('Map zoom icon missing');
    const icon=await zoom.evaluate(el=>getComputedStyle(el,'::before').content);
    if(!icon||icon==='none')throw Error('Map zoom icon is not drawn');
    await page.screenshot({path:path.join(__dirname,'board-toolbar-review.png')});
    const before=await zoom.getAttribute('aria-pressed');
    const oldTile=await page.locator('#board .cell').first().elementHandle();
    await zoom.click();
    if(await zoom.getAttribute('aria-pressed')===before)throw Error('Zoom icon did not toggle map size');
    if(await oldTile.evaluate(el=>el.isConnected))throw Error('Fit map left old tile art in place until the next move');
    await page.screenshot({path:path.join(__dirname,'fitted-map-review.png')});
    await page.evaluate(()=>__campaign.choose(3));
    if(await page.locator('.boardZoom').isVisible())throw Error('Small map reserves empty toolbar space');
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS one map zoom icon; no summary or redundant controls');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
