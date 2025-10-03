import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from services.utils import esperar_download
from config import INTERVALO_BAIXAR, NOME_ARQUIVO

def baixar_relatorio(driver, relatorio_id, pasta_downloads="downloads"):
    """
    Acessa 'Meus relatórios', pesquisa e baixa o relatório pelo ID fornecido.
    Caso o arquivo ainda não esteja pronto, refaz TODO o processo a cada X minutos.
    """
    wait = WebDriverWait(driver, 30)

    while True:
        try:
            # 1) Vai para a página inicial após login
            driver.get("https://sicredi.elaw.com.br/processoView.elaw")
            time.sleep(3)

            # 2) Abre o menu da maleta (ícone pi-briefcase)
            menu_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[@class='notifications-item']//i[contains(@class,'pi-briefcase')]/..")
                )
            )
            menu_btn.click()
            time.sleep(2)

            # 3) Clica no link "Meus relatórios" (href fixo, token dinâmico)
            meus_relatorios = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[starts-with(@href,'userElawReportRequestList.elaw?faces-redirect=true&etoken=')]")
                )
            )
            driver.execute_script("arguments[0].click();", meus_relatorios)
            print("📂 Acessando 'Meus relatórios'...")
            time.sleep(2)

            # 4) Clica em "Pesquisar"
            btn_pesquisar = wait.until(EC.element_to_be_clickable((By.ID, "btnPesquisar")))
            driver.execute_script("arguments[0].click();", btn_pesquisar)
            print("🔎 Pesquisa disparada.")
            time.sleep(3)

            # 5) Procurar na tabela o relatório pelo ID
            tabela = wait.until(EC.presence_of_element_located((By.ID, "tableElawReportRequest_data")))
            linhas = tabela.find_elements(By.TAG_NAME, "tr")

            alvo = None
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, "td")
                if len(colunas) > 3 and colunas[3].text.strip() == relatorio_id:
                    alvo = linha
                    break

            if not alvo:
                raise Exception(f"❌ Relatório com ID {relatorio_id} não encontrado na lista.")

            # 6) Verificar se existe link na 3ª coluna
            try:
                link_download = alvo.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
                driver.execute_script("arguments[0].click();", link_download)
                print(f"📥 Download iniciado para relatório ID {relatorio_id}")

                # Esperar e renomear o arquivo
                esperar_download(pasta_downloads, NOME_ARQUIVO)
                break  # Sai do loop porque o download foi feito

            except Exception:
                print(
                    f"⏳ Relatório {relatorio_id} ainda não está pronto. "
                    f"Refazendo processo de download em {INTERVALO_BAIXAR} minutos..."
                )
                time.sleep(INTERVALO_BAIXAR * 60)  # espera alguns minutos antes de repetir tudo

        except Exception as e:
            print(f"⚠️ Erro durante a tentativa de baixar relatório: {e}")
            print(f"⏳ Repetindo todo o processo em {INTERVALO_BAIXAR} minutos...")
            time.sleep(INTERVALO_BAIXAR * 60)

    # 7) Download finalizado
    print("✅ Download solicitado e concluído com sucesso.")