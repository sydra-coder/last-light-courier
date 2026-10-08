const path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(()=>!!window.__campaign&&!!window.__integratedShell);
    await page.evaluate(()=>__campaign.choose(500));
    await page.waitForTimeout(500);
    const layout=await page.evaluate(()=>{const viewport=document.querySelector('.mapViewport'),frame=document.querySelector('.boardframe'),cell=document.querySelector('#board .cell'),state=__campaign.getState();return {grid:__campaign.getCurrentLevel().grid,zoomed:frame.classList.contains('zoomed'),viewport:viewport.getBoundingClientRect().width,viewportHeight:viewport.getBoundingClientRect().height,world:frame.getBoundingClientRect().width,cell:cell.getBoundingClientRect().width,scrollWidth:viewport.scrollWidth,scrollLeft:viewport.scrollLeft,pos:state.pos,powerOpen:!document.querySelector('#candidatePower .powerInfo').hidden}});
    await page.screenshot({path:path.join(__dirname,'level-500-12-tile-review.png')});
    if(layout.grid!==20||!layout.zoomed||layout.world<=layout.viewport||layout.scrollWidth<=layout.viewport||layout.cell<27||layout.cell>37||Math.abs(layout.viewportHeight-layout.viewport)>22)throw Error('12 tile viewport failed: '+JSON.stringify(layout));
    const icon=page.locator('#candidatePower .powerIcon[data-power="map_stabilizer"]');
    await icon.dispatchEvent('pointerdown',{pointerId:1,pointerType:'touch',clientX:20,clientY:20});
    await page.waitForTimeout(600);
    await icon.dispatchEvent('pointerup',{pointerId:1,pointerType:'touch',clientX:20,clientY:20});
    if(!(await page.evaluate(()=>!document.querySelector('#candidatePower .powerInfo').hidden)))throw Error('Power info did not open');
    await icon.dispatchEvent('pointerdown',{pointerId:2,pointerType:'touch',clientX:20,clientY:20});
    await icon.dispatchEvent('pointerup',{pointerId:2,pointerType:'touch',clientX:20,clientY:20});
    if(!(await page.evaluate(()=>document.querySelector('#candidatePower .powerInfo').hidden)))throw Error('Second click did not dismiss power info');
    if(errors.length)throw Error(errors.join(' | '));
    console.log('PASS 20x20 level viewed through ~12x12 phone viewport and power info dismisses on second tap');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
