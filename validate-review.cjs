const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(__dirname + '/last-light-courier-review.html', 'utf8');
const source = html.match(/const levels=\[([\s\S]*?)\];\nconst key=/);
if (!source) throw new Error('Level data not found in HTML');
const levels = vm.runInNewContext('[' + source[1] + ']');

for (const [n, level] of levels.entries()) {
  const at = (r, c) => r * 8 + c;
  const houses = [], walls = new Set(), darks = new Set();
  let depot = -1;
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
    const ch = level.rows[r][c], p = at(r, c);
    if (ch === 'H') houses.push(p);
    if (ch === 'D') depot = p;
    if (ch === 'X' || ch === 'R' && !level.repair?.dark) walls.add(p);
    if (ch === 'R' && level.repair?.dark) darks.add(p);
  }
  if (level.rows.length !== 8 || level.rows.some(row => row.length !== 8) || depot < 0 || houses.length < level.need) throw new Error(`Bad map ${n + 1}`);
  const shadowAt = step => level.patrol ? at(...level.patrol[step % level.patrol.length]) : -1;
  const queue = [{p:depot, mask:0, light:level.light, step:0, active:!!level.patrol&&!level.wake, route:''}];
  const seen = new Set();
  let answer;
  for (let q = 0; q < queue.length; q++) {
    const s = queue[q], count = s.mask.toString(2).replace(/0/g, '').length;
    if (s.p === depot && count >= level.need) { answer = s; break; }
    const id = [s.p,s.mask,s.light,s.step % (level.patrol?.length || 1),s.active].join(',');
    if (seen.has(id)) continue;
    seen.add(id);
    for (const [dr,dc,letter] of [[-1,0,'U'],[1,0,'D'],[0,-1,'L'],[0,1,'R']]) {
      const r = Math.floor(s.p/8)+dr,c=s.p%8+dc;
      if (r<0||r>7||c<0||c>7) continue;
      const p=at(r,c),cost=darks.has(p)?2:1;
      if (walls.has(p)||s.light<cost) continue;
      if (s.active&&p===shadowAt(s.step+1)) continue;
      let mask=s.mask,light=s.light-cost,active=s.active,step=s.step;
      if (active) step++;
      const hi=houses.indexOf(p);
      const delivered=hi>=0&&!(mask & (1<<hi));
      if (delivered) {
        mask|=1<<hi; light=Math.min(level.light,light+2);
        if (level.wake&&!active) {active=true;step=0;}
      }
      if (active&&p===shadowAt(step)&&!delivered) continue;
      if (light===0&&p!==depot) continue;
      queue.push({p,mask,light,active,step,route:s.route+letter});
    }
  }
  if (!answer) throw new Error(`Level ${n+1} has no no-repair return route`);
  console.log(`${String(n+1).padStart(2,'0')} ${level.name}: ${answer.route.length} moves, ${answer.light} light left, route ${answer.route}`);
}
