import re
import os

files = ['saude.md', 'educacao.md', 'seguranca.md', 'infraestrutura.md', 'financas.md', 'assistencia.md']
time_pattern = re.compile(r'\s*<div class="dash-nav-time">.*?</div>', re.DOTALL)

for file in files:
    path = os.path.join('docs', file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = time_pattern.search(content)
    if match:
        time_html = match.group(0).strip()
        # Remove from its current location
        content = content.replace(match.group(0), '')
        
        # Insert into dash-actions
        actions_tag = '<div class="dash-actions">'
        if actions_tag in content:
            new_actions = actions_tag + '\n      ' + time_html
            content = content.replace(actions_tag, new_actions)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f"Updated {file}")
