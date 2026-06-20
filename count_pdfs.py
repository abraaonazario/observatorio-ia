import zipfile
from collections import Counter

z = zipfile.ZipFile('DATALUTA MOV_AGRARIO_2024-20260602T191955Z-3-001.zip')
folders = Counter()
total = 0

for f in z.namelist():
    if f.endswith('.pdf'):
        parts = f.split('/')
        if len(parts) > 1:
            folders[parts[1]] += 1
            total += 1

print(f"Total de PDFs encontrados: {total}")
print("-" * 30)
for folder, count in folders.most_common():
    print(f"Pasta: {folder.ljust(15)} -> {count} PDFs")
