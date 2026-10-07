const fs = require('node:fs');
const path = __dirname + '/last-light-courier-review.html';
let html = fs.readFileSync(path, 'utf8');
function replace(from, to) {
  if (!html.includes(from)) throw new Error('Replacement target missing: ' + from.slice(0, 90));
  html = html.replace(from, to);
}
replace('<button class="secondary" data-action="how">How to play</button>', '<button class="secondary" data-action="how">How to play</button><button class="secondary" data-action="settings">Settings</button>');
replace('These ten playable maps follow the level briefs and are open for design feedback.', 'These ten playable maps follow the level briefs and are open for design feedback. A separate 1,000-map experimental archive exists for later review; it is not presented as approved legacy campaign geometry.');
replace('aria-label="Next level">→</button></div></div><div class="notice">', 'aria-label="Next level">→</button><button class="nav-btn" data-action="settings">Settings</button></div></div><div class="notice">');
replace('<div class="board">${Array.from', '<div class="board view-${saved.view}"><canvas id="scene" aria-hidden="true"></canvas>${Array.from');
replace('<span>Tap an adjacent tile to move</span><span>${run.active?\'Outlined tile: shadow’s next step\':\'Shadow: \'+(l.patrol?\'waiting\':\'none\')}</span>', '<span>Tap a green neighbor or use the D-pad</span><span>${run.active?\'Red marks a shadow-blocked move\':\'Shadow: \'+(l.patrol?\'waiting\':\'none\')}</span>');
replace('<div class="controls"><button', '<div><div class="chapter" style="text-align:center;margin-bottom:8px">D-pad · tile taps also work</div><div class="controls"><button');
replace('aria-label="Move right">→</button></div><div class="side-actions">', 'aria-label="Move right">→</button></div></div><div class="side-actions">');
replace("if(screen==='game')renderGame();renderDialog()}", "if(screen==='game'){renderGame();renderScene()}renderDialog()}");
replace('const d=e.target.closest(\'[data-dialog]\');', 'const choice=e.target.closest(\'[data-view]\');if(choice&&dialog?.settings){saved.view=choice.dataset.view;persist();dialog=null;render();return}const d=e.target.closest(\'[data-dialog]\');');
replace("if(a==='how')how()", "if(a==='how')how();if(a==='settings')settings()");
fs.writeFileSync(path, html);
