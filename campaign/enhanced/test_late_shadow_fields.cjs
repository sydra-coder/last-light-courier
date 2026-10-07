// Verify the authored late field triggers in the generated playable preview.
const assert=require('assert');
const fs=require('fs');
const path=require('path');
const api=require('./test_integrated_preview.cjs');
const fields=JSON.parse(fs.readFileSync(path.join(__dirname,'shadow-fields-late-v1/fields.json'),'utf8'));
assert.deepStrictEqual(Object.keys(fields).map(Number),[899,943,953,960,974,982,1902,1904,1939,1959,1963]);
for(const [key,field] of Object.entries(fields)){
  const n=Number(key);
  api.choose(n);
  const level=api.getLevel();
  assert.strictEqual(JSON.stringify(level.shadowInfluence2x2.cells),JSON.stringify(field.cells));
  const tile=field.origin;
  // Isolate field behavior from the map's moving patrol for a direct trigger check.
  level.patrol=null;
  level.patrol2=null;
  level.echo=false;
  const base=api.getState();
  const before={...base,active:true,mask:(1<<(field.triggerCount-1))-1};
  const after={...before,mask:(1<<field.triggerCount)-1};
  assert.strictEqual(api.shadowBlocked(tile,before),false,`Level ${n}: field woke early`);
  assert.strictEqual(api.shadowBlocked(tile,after),true,`Level ${n}: field did not wake`);
}
console.log('PASS: eleven late 2×2 fields activate at their authored delivery counts');
