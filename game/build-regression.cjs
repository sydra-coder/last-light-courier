const fs=require('node:fs');
const path=require('node:path');
const dir=__dirname;
let html=fs.readFileSync(path.join(dir,'tester.html'),'utf8');
const begin=html.indexOf('const LEVELS=');
const end=html.indexOf('];',begin);
if(begin<0||end<0||!html.includes('last-light-courier-tester-v1'))throw Error('Tester build markers missing; run node game/build.cjs first');
html=html.slice(0,begin)+'const LEVELS=[window.LLCRegression.level]'+html.slice(end+1);
html=html.replace('<title>Last Light Courier — tester build</title>','<title>Last Light Courier — regression arena</title>');
html=html.replace('last-light-courier-tester-v1','last-light-courier-regression-v1');
html=html.replace("document.body.classList.add('testerBuild');", "document.body.classList.add('testerBuild','regressionBuild');");
html=html.replace('function choose(n){','function choose(n){if(document.body.classList.contains(\'regressionBuild\'))n=1;');
html=html.replace('function minimumForLevel(n,bought=false,signaled=false){','function minimumForLevel(n,bought=false,signaled=false){if(document.body.classList.contains(\'regressionBuild\'))return null;');
html=html.replace('<script src="tile-symbols.js"></script></head>','<script src="tile-symbols.js"></script><script src="regression-fixture.js"></script><link rel="stylesheet" href="regression.css"></head>');
html=html.replace('<script src="player-data.js"></script><script src="shell.js"></script></body>','<script src="regression-player-data.js"></script><script src="shell.js"></script><script src="regression-ui.js"></script></body>');
if(!html.includes('window.LLCRegression.level')||!html.includes('regression-ui.js'))throw Error('Regression build injection failed');
fs.writeFileSync(path.join(dir,'regression.html'),html);
fs.writeFileSync(path.join(dir,'regression-player-data.js'),fs.readFileSync(path.join(dir,'player-data.js'),'utf8').replace('llc-tester-data-v1','llc-regression-data-v1'));
const remix=html
  .replace('Last Light Courier — regression arena','Last Light Courier — Level 500 test remix')
  .replace('last-light-courier-regression-v1','last-light-courier-level-500-test-v1')
  .replace('<script src="regression-fixture.js"></script>','<script src="regression-fixture.js"></script><script src="level-500-test-fixture.js"></script>')
  .replace('regression-player-data.js','level-500-test-player-data.js');
if(!remix.includes('level-500-test-fixture.js')||!remix.includes('last-light-courier-level-500-test-v1'))throw Error('Level 500 test injection failed');
fs.writeFileSync(path.join(dir,'level-500-test.html'),remix);
fs.writeFileSync(path.join(dir,'level-500-test-player-data.js'),fs.readFileSync(path.join(dir,'regression-player-data.js'),'utf8').replace('llc-regression-data-v1','llc-level-500-test-data-v1'));
console.log('Built game/regression.html and game/level-500-test.html');
