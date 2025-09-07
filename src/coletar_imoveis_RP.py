from playwright.sync_api import sync_playwright, TimeoutError
import csv
import os

# CONFIGURAÇÃO
LIMITE_DE_DADOS = 5000
LOTE_SALVAMENTO_IMOVEIS = 1000

# O nome da função foi padronizado para colher_dados
def colher_dados(arquivo_csv):
    resultados_em_memoria = []
    total_imoveis_salvos = 0
    proxima_meta_salvamento = LOTE_SALVAMENTO_IMOVEIS
    
    if not os.path.exists(arquivo_csv):
        with open(arquivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["preco", "endereco", "detalhe_localizacao", "caracteristicas", "descricao"])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        page = context.new_page()
        page.set_default_timeout(30000)

        url_inicial = "https://www.imovelweb.com.br/imoveis-venda-ribeirao-preto-sp.html"
        print(f"➡️  Acessando URL (Ribeirão Preto): {url_inicial}")
        page.goto(url_inicial, wait_until='domcontentloaded')

        pagina_atual = 1

        while total_imoveis_salvos < LIMITE_DE_DADOS:
            print(f"\n--- Processando pág {pagina_atual} | Salvos: {total_imoveis_salvos} | Em memória: {len(resultados_em_memoria)} ---")
            
            try:
                page.wait_for_selector(".postingsList-module__postings-container", state='visible')
                posts_locators = page.locator(".postingsList-module__card-container").all()

                if not posts_locators:
                    print("🚫 Nenhum imóvel encontrado nesta página. Encerrando.")
                    break

                for post_locator in posts_locators:
                    if total_imoveis_salvos + len(resultados_em_memoria) >= LIMITE_DE_DADOS:
                        break
                    try:
                        preco = post_locator.locator(".postingPrices-module__price").text_content()
                        endereco = post_locator.locator(".postingLocations-module__location-address").text_content()
                        bairro = post_locator.locator(".postingLocations-module__location-text").text_content()
                        caracteristicas = post_locator.locator(".postingMainFeatures-module__posting-main-features-block-one-line").text_content()
                        descricao = post_locator.locator(".postingCard-module__posting-description").text_content()

                        resultados_em_memoria.append([
                            preco.strip(), endereco.strip(), bairro.strip(),
                            " ".join(caracteristicas.split()), descricao.strip()
                        ])
                    except TimeoutError:
                        continue
                
                if (total_imoveis_salvos + len(resultados_em_memoria)) >= proxima_meta_salvamento:
                    print(f"--- Meta de {proxima_meta_salvamento} atingida. Salvando {len(resultados_em_memoria)} imóveis... ---")
                    with open(arquivo_csv, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerows(resultados_em_memoria)
                    
                    total_imoveis_salvos += len(resultados_em_memoria)
                    resultados_em_memoria.clear()
                    proxima_meta_salvamento += LOTE_SALVAMENTO_IMOVEIS

                if total_imoveis_salvos >= LIMITE_DE_DADOS:
                    print(f"\n🏁 Meta final de {LIMITE_DE_DADOS} imóveis atingida.")
                    break

                next_button = page.locator('a[data-qa="PAGING_NEXT"]')
                if next_button.is_visible():
                    next_button.click()
                    page.wait_for_load_state('domcontentloaded')
                    pagina_atual += 1
                else:
                    print("✅ Fim da paginação.")
                    break
            except Exception as e:
                print(f"❌ Erro inesperado, encerrando: {e}")
                break
        
        if resultados_em_memoria:
            dados_restantes = resultados_em_memoria[:LIMITE_DE_DADOS - total_imoveis_salvos]
            print(f"--- Salvando lote final com {len(dados_restantes)} imóveis restantes... ---")
            with open(arquivo_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(dados_restantes)
            total_imoveis_salvos += len(dados_restantes)

        browser.close()
    
    print(f"\n✅ Scraping concluído! Total de {total_imoveis_salvos} imóveis salvos em '{arquivo_csv}'.")