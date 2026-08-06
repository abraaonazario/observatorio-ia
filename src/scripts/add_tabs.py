import os
tabs_to_add = '''    <a href="../financas/" class="dash-tab">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg> Finanças
    </a>
    <a href="../assistencia/" class="dash-tab">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg> Social
    </a>
  </div>'''

for file in ['saude.md', 'educacao.md', 'seguranca.md', 'infraestrutura.md']:
    path = os.path.join('docs', file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'financas/' not in content:
        content = content.replace('</a>\n  </div>\n  <div class="dash-nav-right">', '</a>\n' + tabs_to_add + '\n  <div class="dash-nav-right">')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
