import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dictionary of corrupted sequences to correct characters
    replacements = {
        'Ã£': 'ã', 'Ã§': 'ç', 'Ãµ': 'õ', 'Ã©': 'é', 'Ã‰': 'É',
        'Ãª': 'ê', 'Ã³': 'ó', 'Ãº': 'ú', 'Ã¡': 'á', 'Ã­': 'í',
        'Ã ': 'Á', 'Ã‚': 'Â', 'Ã”': 'Ô', 'Ã§Ã£': 'çã', 'Ã§Ãµ': 'çõ',
        'Ã-': 'Í', 'Â·': '·', 'â†’': '→', 'â†‘': '↑', 'â†“': '↓',
        'â†—': '↗', 'âœ“': '✓', 'âš¡': '⚡', 'PÃºblica': 'Pública',
        'Ã reas': 'Áreas', 'gestÃ£o': 'gestão', ' EducaÃ§Ã£o': ' Educação',
        'SaÃºde': 'Saúde', 'SeguranÃ§a': 'Segurança', 'ExcelÃªncia': 'Excelência',
        'TransparÃªncia': 'Transparência', 'ESTRATÃ‰GICOS': 'ESTRATÉGICOS',
        'DecisÃµes': 'Decisões', 'matrÃ­culas': 'matrículas',
        'ocorrÃªncias': 'ocorrências', 'resoluÃ§Ã£o': 'resolução', 'Ã\xad': 'í',
        'pÃºblica': 'pública', 'estratÃ©gicos': 'estratégicos'
    }

    for bad, good in replacements.items():
        content = content.replace(bad, good)
        
    if "index.md" in filepath:
        content = content.replace('margin-top: 70px;', 'padding-top: 70px; margin-top: 0;')
        
        # Remove duplicate header css
        import re
        content = re.sub(r'(?s)<style>.*?/\* Custom Top Nav for Home - Fixed to top \*/.*?</style>', 
        '<style>.md-header { display: none !important; } .md-main__inner { margin-top: 0 !important; } .md-content { padding-top: 0 !important; } .md-grid { max-width: 100% !important; padding: 0 !important; margin: 0 !important; } .md-content__inner { margin: 0 !important; } .hero-section { padding-top: 70px; margin-top: 0; } .nav-brand { display: flex; align-items: center; gap: 1rem; min-width: max-content; } .nav-logo { background: linear-gradient(135deg, #0ea5e9, #10b981); color: white; width: 35px; height: 35px; min-width: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3); } .nav-titles { display: flex; flex-direction: column; white-space: nowrap; } .nav-main-title { font-weight: 800; font-size: 0.95rem; letter-spacing: 0.5px; line-height: 1.2; } .nav-sub-title { font-size: 0.65rem; color: #94a3b8; letter-spacing: 0.5px; } .nav-links { display: flex; gap: 1.5rem; white-space: nowrap; } .nav-links a { color: #cbd5e1 !important; text-decoration: none !important; font-size: 0.85rem; font-weight: 500; transition: color 0.2s; padding-bottom: 5px; border-bottom: 2px solid transparent; } .nav-links a:hover, .nav-links a.active { color: white !important; border-bottom: 2px solid #55b44d; } .nav-actions { display: flex; align-items: center; gap: 1rem; min-width: max-content; } .nav-badge { font-size: 0.75rem; color: #94a3b8; display: flex; align-items: center; gap: 0.4rem; border: 1px solid #1e3a8a; padding: 0.3rem 0.6rem; border-radius: 15px; white-space: nowrap; } .btn-portal { background: #90d836; color: #0f172a !important; text-decoration: none !important; padding: 0.5rem 1.2rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem; transition: transform 0.2s; white-space: nowrap; } .btn-portal:hover { transform: translateY(-2px); } @media screen and (max-width: 900px) { .nav-links, .nav-badge { display: none; } }</style>', 
        content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base = r"C:\Projeto\Data Lake\docs"
for name in ["index.md", "mapa-ativos.md", "assistente-ia.md", "saude.md", "educacao.md", "seguranca.md", "infraestrutura.md"]:
    fix_file(os.path.join(base, name))
print("Done")
