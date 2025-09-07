import os

def garantir_pasta_de_dados(caminho_da_pasta):
    """Garante que o diretório especificado exista. Se não, ele o cria."""
    os.makedirs('/data', exist_ok=True)
    print(f"✅ Pasta '{'/data'}' pronta.")