import json
import os

input_file = r"C:\Users\Administrator\.gemini\antigravity-ide\brain\b8cbcb72-649c-417a-a9eb-0c9a6885e302\.system_generated\steps\181\content.md"

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# O read_url_content pode ter retornado o JSON direto ou em uma linha
json_start = content.find('{"status":')
if json_start != -1:
    json_str = content[json_start:]
    try:
        dados_completos = json.loads(json_str)
        
        # Como passamos ?uf=MT, não precisamos filtrar novamente, mas vamos garantir
        dados_mt = [posto for posto in dados_completos.get("data", []) if posto.get("uf") == "MT"]
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "data")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "combustiveis_mt.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"status": 200, "data": dados_mt}, f, ensure_ascii=False)
            
        print(f"Sucesso! {len(dados_mt)} postos de MT salvos em {output_path}")
    except Exception as e:
        print(f"Erro ao parsear JSON: {e}")
else:
    print("Não encontrou o JSON")
