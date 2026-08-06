import cloudscraper
import json
import os

url = "https://revendedoresapi.anp.gov.br/v1/combustivel?uf=MT"

print(f"Buscando dados de: {url}")
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
resposta = scraper.get(url)

if resposta.status_code == 200:
    dados = resposta.json()
    
    # Garantir que o diretório docs/data existe
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "combustiveis_mt.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        
    print(f"Dados salvos com sucesso em {output_path}")
    print(f"Total de registros encontrados: {len(dados.get('data', []))}")
else:
    print(f"Erro ao acessar API: {resposta.status_code}")
    print(resposta.text)
