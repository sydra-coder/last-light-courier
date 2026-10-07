const fs = require('fs');
const path = require('path');
const sourceDir = 'C:\\Users\\rahul\\.codex\\generated_images\\01a1112e-3975-75e3-9146-c1ec2019c43a';
const names = [
  'exec-9c774560-f8fd-439b-8c8c-710b4f7c09ee.png',
  'exec-3f3b3727-70f1-41e9-a8ca-7a9afd3f9d2a.png',
  'exec-84b5ed92-51d8-48b0-8eef-e1259e3db868.png',
  'exec-ada8c2ff-a2e1-4fc7-b1be-a42d1ed0f6be.png',
  'exec-dc5ba264-307a-4032-a084-638401fd8850.png',
  'exec-407d2e60-ac5b-4f31-9122-9b2d0ba3e996.png',
  'exec-b88a3a57-2d83-41cc-bcd4-460c3afb108f.png',
  'exec-69f89095-a1da-4341-bd4e-08833c86db07.png',
  'exec-e72c9672-458d-4b3f-b900-0671ad09b791.png',
  'exec-78f05400-4c6d-4bfd-a89d-f86904f679d0.png',
  'exec-b400be73-60fa-4bc0-9aa1-784a382321c4.png',
  'exec-fcded96c-c8b0-43f4-9210-16324034a8d9.png',
  'exec-658f6650-237b-461d-aed6-273f38423e36.png',
  'exec-a96554b4-ef32-4e98-9f14-ec9cbad0e9e7.png',
  'exec-3199984d-f27d-49b5-ad78-8f8a0c08c0d2.png',
  'exec-4c57bcb0-d55e-44dd-b108-1a692fc0a2ab.png',
  'exec-8ee604a6-51d5-4fa4-97ea-0a468be292e3.png',
  'exec-348bb6de-198c-4946-ab3d-acf1e61647c9.png',
  'exec-51bbbb3c-0132-4f28-a34a-9fd27e689e0f.png',
  'exec-1302c23b-a0a2-42e5-8b0d-6f0392f36be9.png'
];
const regions = JSON.parse(fs.readFileSync(path.join(__dirname, 'region-shadow-map.json'), 'utf8'));
if (regions.length !== 20 || names.length !== 20) throw new Error('Expected 20 art files and 20 regions');
for (let i = 0; i < 20; i++) {
  const src = path.join(sourceDir, names[i]);
  const dest = path.join(__dirname, `region-${String(i + 1).padStart(2, '0')}-${regions[i].name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-$/, '')}.png`);
  if (!fs.existsSync(src)) throw new Error(`Missing ${src}`);
  fs.copyFileSync(src, dest);
  regions[i].regionArt = path.basename(dest);
  regions[i].source = names[i];
}
fs.writeFileSync(path.join(__dirname, 'region-shadow-map.json'), JSON.stringify(regions, null, 2) + '\n');
const htmlPath = path.join(__dirname, 'region-shadow-review.html');
let html = fs.readFileSync(htmlPath, 'utf8');
html = html.replace("let file=`${id}-${slug[id]}.png`;", "let file=`region-${String(n).padStart(2,'0')}-${name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-$/,'')}.png`;");
fs.writeFileSync(htmlPath, html);
console.log('Installed 20 region-specific PNGs and updated review');
