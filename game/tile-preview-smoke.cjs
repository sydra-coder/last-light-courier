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
    const cell=page.locator('#board .cell.dark').first();
    await cell.scrollIntoViewIfNeeded();
    const box=await cell.boundingBox();
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    const turns=await page.evaluate(()=>__campaign.getState().turns);
    await page.mouse.down();await page.waitForTimeout(550);
    if(!await page.locator('#tilePreview').isVisible())throw Error('Tile preview did not open on hold');
    if(await page.locator('#tilePreview strong').textContent()!=='Dark street')throw Error('Tile preview did not name the dark street');
    if(!await page.locator('#tilePreview span').textContent().then(text=>text.includes('costs 2 lantern light')))throw Error('Tile preview did not explain the crescent');
    await page.screenshot({path:path.join(__dirname,'tile-preview-review.png')});
    await page.mouse.up();
    if((await page.evaluate(()=>__campaign.getState().turns))!==turns)throw Error('Holding a tile moved the courier');
    await page.waitForTimeout(3100);
    if(await page.locator('#tilePreview').isVisible())throw Error('Tile preview did not close after release');
    if(errors.length)throw Error(errors.join('\n'));
    console.log('PASS hold magnifies tile and label; no move; closes after release');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
