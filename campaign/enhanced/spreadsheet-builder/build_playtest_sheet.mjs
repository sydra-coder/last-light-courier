import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = 'C:/Sydra/Last Light Courier';
const data = JSON.parse(await fs.readFile(`${root}/campaign/enhanced/playtest_rows.json`, 'utf8'));
if (data.rows.length !== 2000 || data.headers.length !== 14) throw new Error('Unexpected level row shape');
const outputDir = `${root}/outputs/01a1112f-b897-7c03-a6b3-f25018e9f557`;
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('Levels');
sheet.showGridLines = false;

sheet.mergeCells('A1:N1');
sheet.getRange('A1').values = [['Last Light Courier | 2,000-level playtest status']];
sheet.getRange('A1:N1').format = {fill:'#19304A',font:{name:'Aptos',size:17,bold:true,color:'#FFF0D0'}};
sheet.getRange('A1:N1').format.rowHeight = 34;
sheet.mergeCells('A2:N2');
sheet.getRange('A2').values = [['Filter the table below. All 2,000 routes replay in the preview. No-power steps are shortest only where marked Yes; power/alternate steps are verified routes.']];
sheet.getRange('A2:N2').format = {fill:'#E9F0F3',font:{name:'Aptos',size:11,color:'#19304A'}};
sheet.getRange('A2:N2').format.rowHeight = 26;
sheet.mergeCells('A3:N3');
sheet.getRange('A3').values = [['20 districts × 100 levels. Map changes are authored or player-selected. Shadow actors excludes spawner zones and influence fields; those are listed under hazards. Assigned power is the sample tool.']];
sheet.getRange('A3:N3').format = {fill:'#FFF2DD',font:{name:'Aptos',size:10,color:'#51381E'}};
sheet.getRange('A3:N3').format.rowHeight = 25;

const all = [data.headers, ...data.rows];
sheet.getRangeByIndexes(4,0,all.length,all[0].length).values = all;
sheet.getRange('A5:N2005').format.font = {name:'Aptos',size:10,color:'#253548'};
sheet.getRange('A5:N5').format = {fill:'#24455D',font:{name:'Aptos',size:10,bold:true,color:'#FFFFFF'},wrapText:true};
sheet.getRange('A5:N5').format.rowHeight = 32;
sheet.getRange('A6:F2005').setNumberFormat('0');
sheet.getRange('K6:L2005').setNumberFormat('0');
sheet.getRange('A:A').format.columnWidth = 9;
sheet.getRange('B:F').format.columnWidth = 10;
sheet.getRange('G:G').format.columnWidth = 20;
sheet.getRange('H:H').format.columnWidth = 31;
sheet.getRange('I:I').format.columnWidth = 47;
sheet.getRange('J:J').format.columnWidth = 17;
sheet.getRange('K:L').format.columnWidth = 20;
sheet.getRange('M:M').format.columnWidth = 24;
sheet.getRange('N:N').format.columnWidth = 53;
sheet.freezePanes.freezeRows(5);
const table = sheet.tables.add('A5:N2005', true, 'CourierLevels');
table.showFilterButton = true;

workbook.recalculate();
for (const range of ['A1:H12','I5:N12','A1002:H1007','I2000:N2005']) {
  const check = await workbook.inspect({kind:'table',range:`Levels!${range}`,include:'values',tableMaxRows:14,tableMaxCols:15,maxChars:3500});
  console.log(range,check.ndjson);
}
const errors = await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'formula error scan'});
console.log('ERROR_SCAN',errors.ndjson);
for (const [range,name] of [['A1:N6','playtest-top.png'],['A1:H12','playtest-left.png'],['I5:N12','playtest-right.png'],['A304:N307','playtest-rebalanced-301.png'],['A706:N709','playtest-rebalanced-702.png'],['A808:N812','playtest-rebalanced-805.png'],['A834:N839','playtest-rebalanced-831.png'],['A874:N879','playtest-rebalanced-871.png'],['A904:N909','playtest-rebalanced-901.png'],['A954:N959','playtest-rebalanced-952.png']]) {
  const preview = await workbook.render({sheetName:'Levels',range,scale:1.5,format:'png'});
  await fs.writeFile(`${outputDir}/${name}`,new Uint8Array(await preview.arrayBuffer()));
}
await fs.mkdir(outputDir,{recursive:true});
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/Last_Light_Courier_2000_Level_Playtest_Status.xlsx`);
console.log('SAVED',`${outputDir}/Last_Light_Courier_2000_Level_Playtest_Status.xlsx`);
