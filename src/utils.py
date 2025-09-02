import os

def data_save(PASTA_DADOS, NOME_ARQUIVO):

    # Cria o caminho completo para o arquivo, relativo à raiz do projeto
    caminho_arquivo_csv = os.path.join(PASTA_DADOS, NOME_ARQUIVO)

    # Garante que a pasta 'data' exista no diretório principal
    os.makedirs(PASTA_DADOS, exist_ok=True)

    return caminho_arquivo_csv
