from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

from config.config import data_save

def colher_dados(arquivo_csv):
    pagina = 1  # contador de páginas
    
    # Cria o CSV com cabeçalho, se ainda não existir
    if not os.path.exists(arquivo_csv):
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["preco", "endereco", "detalhe_localizacao", "caracteristicas", "descricao"])

    while True:
        print(f"\n➡️ Abrindo página {pagina}")
        url = f"https://www.imovelweb.com.br/casas-terrenos-comerciais-apartamentos-venda-franca-sp-pagina-{pagina}.html"

        # Abre o navegador
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        try:
            driver.get(url)

            # Espera o container principal dos posts estar presente
            container = wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "postingsList-module__postings-container")
                )
            )

            # Busca todos os cards de posts dentro do container principal
            posts = container.find_elements(By.CLASS_NAME, "postingsList-module__card-container")

            # Se não houver posts, encerra o loop
            if not posts:
                print("🚫 Nenhum imóvel encontrado nesta página. Encerrando scraping.")
                driver.quit()
                break

            resultados = []

            for post in posts:
                try:
                    preco = post.find_element(By.CLASS_NAME, "postingPrices-module__price").text
                    endereco = post.find_element(By.CLASS_NAME, "postingLocations-module__location-address").text
                    bairro = post.find_element(By.CLASS_NAME, "postingLocations-module__location-text").text
                    caracteristicas = post.find_element(By.CLASS_NAME, "postingMainFeatures-module__posting-main-features-block-one-line").text
                    descricao = post.find_element(By.CLASS_NAME, "postingCard-module__posting-description").text

                    resultados.append([preco, endereco, bairro, caracteristicas, descricao])

                    print(preco, endereco, bairro, caracteristicas, descricao, "\n")

                except Exception as e:
                    print(f"⚠️ Erro ao extrair dados de um post: {e}")
                    continue

            # Salva os resultados no CSV
            with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(resultados)

        except Exception as e:
            print(f"❌ Erro ao acessar página {pagina}: {e}")
            driver.quit()
            break

        # Fecha o navegador
        driver.quit()
        print(f"✅ Página {pagina} processada com sucesso e salva no CSV.\n")

        # Incrementa o número da página
        pagina += 1

        # Pequena pausa para evitar bloqueio do site
        time.sleep(2)

        data_save(PASTA_DADOS="data", NOME_ARQUIVO="imoveis.csv")
