const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');

const root = path.resolve(__dirname, '..', '..');
const html = fs.readFileSync(path.join(__dirname, 'region-mix-review.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert(script, 'review script exists');
new vm.Script(script);

const regionMap = JSON.parse(fs.readFileSync(path.join(root, 'design', 'shadow-variants', 'region-shadow-map.json'), 'utf8'));
const couriers = JSON.parse(fs.readFileSync(path.join(root, 'design', 'character-variants', 'manifest.json'), 'utf8'));
assert.equal(regionMap.length, 20);
for (const region of regionMap) assert(html.includes(region.name), `missing ${region.name}`);
for (const courier of couriers) assert(html.includes(courier.name), `missing ${courier.name}`);
const shadowIds = JSON.parse(html.match(/const shadowIds=(\[[^\]]+\])/)[1]);
assert.deepEqual(shadowIds, regionMap.map(row => Number(row.shadow) - 1), 'region shadow assignments match current map');
for (const power of ['anchor_trap', 'decoy_light', 'reveal_pulse', 'lumen_flask', 'road_repair', 'light_bridge', 'map_stabilizer', 'freeze_seal', 'rewind']) assert(html.includes(`data-power="${power}"`), `missing ${power}`);

const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
const elements = Object.fromEntries(ids.map(id => [id, { id, value: ({ volume: 65, light: 100, distance: 6, region: 0, courier: 0 })[id] ?? 0, checked: false, textContent: '', add(option) { (this.options ??= []).push(option); }, setAttribute() {} }]));
let voices = 0;
class Param { setValueAtTime() {} exponentialRampToValueAtTime() {} setTargetAtTime() {} cancelScheduledValues() {} }
class Node { constructor() { this.gain = new Param(); this.frequency = new Param(); } connect() {} start() { voices++; } stop() {} }
class AudioContext { constructor() { this.currentTime = 0; this.destination = new Node(); } createGain() { return new Node(); } createOscillator() { return new Node(); } resume() { return Promise.resolve(); } }
const document = { hidden: false, getElementById: id => elements[id], querySelectorAll: () => [], addEventListener() {} };
const sandbox = { document, window: { AudioContext }, Option: function(text, value) { return { text, value }; }, setInterval: () => 1, clearInterval() {}, setTimeout(fn) { fn(); } };
vm.runInNewContext(script, sandbox);
assert.equal(elements.region.options.length, 20);
assert.equal(elements.courier.options.length, 18);

(async () => {
  await elements.start.onclick();
  assert(voices >= 5, 'starting mix schedules audible notes');
  for (const method of ['regionSolo', 'courierSolo', 'shadowSolo']) {
    const before = voices; await elements[method].onclick(); assert(voices > before, `${method} schedules sound`);
  }
  for (const cue of [...html.matchAll(/data-cue="([^"]+)"/g)].map(m => m[1])) {
    const before = voices;
    await elements.events.onclick({ target: { closest: () => ({ dataset: { cue }, textContent: cue }) } });
    assert(voices > before, `${cue} schedules sound`);
  }
  for (const power of [...html.matchAll(/data-power="([^"]+)"/g)].map(m => m[1])) {
    const before = voices;
    await elements.powers.onclick({ target: { closest: () => ({ dataset: { power }, textContent: power }) } });
    assert(voices > before, `${power} schedules sound`);
  }
  elements.region.value = 19;
  elements.region.onchange();
  assert.match(elements.shadowName.textContent, /Night Wisp/);
  console.log(`Review controls schedule sound; ${regionMap.length} regions, ${couriers.length} couriers, nine powers and all events mapped.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
