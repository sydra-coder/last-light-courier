const path = require('node:path');
const { chromium } = require('playwright');

const levels = [1,8,6,9,11,31,51,61,101,151,201,301,401,402,501,601,701,801,901,902,951,952,1001,1002,1003,1101,1201,1204,1301,1401,1402,1601,1701,1805];

(async () => {
  const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  try {
    const page = await browser.newPage({viewport:{width:390,height:844}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('file://' + path.join(__dirname,'tester.html').replaceAll('\\','/'));
    await page.waitForFunction(() => !!window.__campaign && !!window.__integratedShell);
    for (const n of levels) {
      const result = await page.evaluate(n => {
        __campaign.choose(n);
        return {number:__campaign.levels[n-1].n,cells:document.querySelectorAll('#board .cell').length,title:document.querySelector('#levelTitle').textContent,powers:document.querySelectorAll('#candidatePower .powerIcon').length};
      },n);
      if (result.number !== n || result.cells < 64 || !result.title.includes(String(n)) || result.powers !== 9) throw Error('Level failed: '+JSON.stringify(result));
    }
    if (errors.length) throw Error(errors.join(' | '));
    console.log(`PASS ${levels.length} review levels, nine tester powers, no page errors`);
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exitCode=1});
