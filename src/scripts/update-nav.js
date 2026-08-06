const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'docs');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));

for (const file of files) {
  const filePath = path.join(dir, file);
  if (file === 'violencia-mulher.md') continue; // already has it
  
  let content = fs.readFileSync(filePath, 'utf8');
  if (content.includes('<div class="dash-nav-tabs">') && !content.includes('violencia-mulher')) {
    content = content.replace(/(<a href="\.\.\/assistencia\/".*?<\/a>)/g, '$1\n    <a href="../violencia-mulher/" class="dash-tab">🟣 Violência Mulher</a>');
    fs.writeFileSync(filePath, content);
    console.log('Updated ' + file);
  }
}
