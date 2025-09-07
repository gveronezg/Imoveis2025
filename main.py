# Importa os módulos da pasta 'src'
from src import coletar_imoveis_F
from src import coletar_imoveis_RP
from src import utilits
import os

# Ponto de entrada do programa
if __name__ == "__main__":
    
    PASTA_DE_DADOS = "data"

    # 1. Garante que a pasta 'data' exista
    utilits.garantir_pasta_de_dados(PASTA_DE_DADOS)

    # 2. Define os caminhos completos para os arquivos de saída
    caminho_imoveis_f = os.path.join(PASTA_DE_DADOS, "imoveis_F.csv")
    caminho_imoveis_rp = os.path.join(PASTA_DE_DADOS, "imoveis_RP.csv")

    print("\n--- INICIANDO COLETA DE IMÓVEIS DE FRANCA ---")
    coletar_imoveis_F.colher_dados(caminho_imoveis_f)

    print("\n--- INICIANDO COLETA DE IMÓVEIS DE RIBEIRÃO PRETO ---")
    coletar_imoveis_RP.colher_dados(caminho_imoveis_rp)

    print("\n--- TODOS OS PROCESSOS DE COLETA FORAM CONCLUÍDOS ---")