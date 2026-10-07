// Local development service only. No identity or authoritative run replay yet.
const http = require('node:http');
const { randomUUID } = require('node:crypto');
const { readFileSync, writeFileSync, existsSync } = require('node:fs');
const path = require('node:path');

const file = path.join(__dirname, 'results-dev.json');
const port = Number(process.env.PORT || 8787);
const data = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : { players: {}, runs: {} };
const send = (res, code, body) => { res.writeHead(code, {'Content-Type':'application/json', 'Access-Control-Allow-Origin':'*', 'Access-Control-Allow-Headers':'Content-Type'}); res.end(JSON.stringify(body)); };
const valid = r => Number.isInteger(r.levelId) && r.levelId >= 1 && r.levelId <= 200 && r.rulesRevision === 2 && Number.isInteger(r.lightSpent) && r.lightSpent > 0 && r.lightSpent < 10000 && Number.isInteger(r.steps) && r.steps > 0 && r.steps <= r.lightSpent && r.allHomes === true && r.hintsUsed === 0 && r.repairUsed === false;
const board = levelId => Object.values(data.runs).filter(r => r.levelId === levelId).sort((a,b) => a.lightSpent-b.lightSpent || a.steps-b.steps).slice(0,20);

http.createServer((req,res) => {
  if(req.method === 'OPTIONS'){res.writeHead(204,{'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type'});return res.end();}
  const url = new URL(req.url, 'http://localhost');
  if(req.method === 'GET' && url.pathname === '/health') return send(res,200,{ok:true,mode:'local-development-only'});
  if(req.method === 'GET' && url.pathname === '/levels') return send(res,200,{levels:Array.from({length:200},(_,i)=>({levelId:i+1,best:board(i+1)[0] || null}))});
  if(req.method === 'GET' && /^\/levels\/\d+\/board$/.test(url.pathname)) return send(res,200,{entries:board(Number(url.pathname.split('/')[2]))});
  if(req.method === 'POST' && url.pathname === '/players') {const id=randomUUID(), name='Courier '+id.slice(0,6);data.players[id]={id,name};writeFileSync(file,JSON.stringify(data));return send(res,201,{id,name});}
  if(req.method === 'POST' && url.pathname === '/runs') {
    let raw='';req.on('data',chunk=>{raw+=chunk;if(raw.length>10000)req.destroy();});req.on('end',()=>{
      let r;try{r=JSON.parse(raw)}catch{return send(res,400,{error:'Invalid JSON'})}
      if(!data.players[r.playerId] || !valid(r))return send(res,400,{error:'Invalid or ineligible run'});
      const key=r.playerId+':'+r.levelId, previous=data.runs[key];
      if(!previous || r.lightSpent<previous.lightSpent || r.lightSpent===previous.lightSpent && r.steps<previous.steps){data.runs[key]={playerId:r.playerId,playerName:data.players[r.playerId].name,levelId:r.levelId,lightSpent:r.lightSpent,steps:r.steps};writeFileSync(file,JSON.stringify(data));}
      return send(res,200,{accepted:true,personalBest:data.runs[key],globalBest:board(r.levelId)[0]});
    });return;
  }
  send(res,404,{error:'Not found'});
}).listen(port,'127.0.0.1',()=>console.log(`Local results test service: http://127.0.0.1:${port}`));
