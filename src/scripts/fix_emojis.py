import os

filepath = r"c:\Projeto\Data Lake\docs\index.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'Ã reas Monitoradas': 'Áreas Monitoradas',
    'Ã REAS DE GESTÃƒO': 'ÁREAS DE GESTÃO',
    'ðŸ›¢ï¸ ': '🛢️',
    'ðŸ”Œ': '🔌',
    'ðŸ¤–': '🤖',
    'ðŸ“Š': '📊',
    'bruto Ã  decisão': 'bruto à decisão',
    'ðŸ“ˆ': '📈',
    'ðŸ›¡ï¸ ': '🛡️',
    'ðŸ‘¥': '👥'
}

for bad, good in replacements.items():
    content = content.replace(bad, good)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed emojis and encoding in index.md")
