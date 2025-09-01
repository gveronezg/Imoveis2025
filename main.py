import src.coletar_imoveis
import os

if __name__ == "__main__":
    src.coletar_imoveis.colher_dados(os.path.join("data", "imoveis.csv"))
