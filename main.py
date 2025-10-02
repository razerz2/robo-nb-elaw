import os
import time
import logging
import shutil
from datetime import datetime, timedelta
from services.auth import login
from services.reports_processos import gerar_relatorio
from services.baixar_relatorio import baixar_relatorio
from services.utils import dentro_horario, perguntar_com_timeout
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    ultima_execucao = None  # guarda a última data em que rodou

    while True:
        agora = datetime.now()

        # Se já executou hoje, só espera até o próximo dia útil
        if ultima_execucao and ultima_execucao.date() == agora.date():
            logging.info("✅ Já executado hoje, aguardando próximo dia útil...")
            # Calcula o tempo até 08h do próximo dia
            proximo = (agora + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
            espera = (proximo - agora).total_seconds()
            time.sleep(espera)
            continue

        # Se estiver fora do horário → perguntar se quer executar mesmo assim
        if not dentro_horario():
            resposta = perguntar_com_timeout(
                "⏸ Fora do horário de execução (Seg-Sex, 08h às 18h).\n👉 Deseja executar mesmo assim? (Y/N): ",
                timeout=15,
            )
            if resposta != "y":
                logging.info("⏳ Fora do horário, aguardando 30 minutos para checar novamente...")
                time.sleep(30 * 60)
                continue

        # Configuração do Chrome para baixar direto sem prompt

        # pasta_downloads = r"C:\Users\SEU_USUARIO\OneDrive\RelatoriosRobo"
        pasta_downloads = os.path.join(os.getcwd(), "downloads")
        os.makedirs(pasta_downloads, exist_ok=True)

        chrome_options = Options()
        prefs = {
            "download.default_directory": pasta_downloads,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")  # 🚀 abre o Chrome no modo anônimo

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        try:
            login(driver)
            relatorio_id = gerar_relatorio(driver)
            logging.info(f"ID capturado: {relatorio_id}")
            baixar_relatorio(driver, relatorio_id, pasta_downloads)
            ultima_execucao = datetime.now()  # marca que rodou hoje
        except Exception as e:
            logging.error(f"❌ Erro na execução: {e}")
        finally:
            driver.quit()
            shutil.rmtree(os.path.join(os.getcwd(), "profile"), ignore_errors=True)
            print("🧹 Navegador encerrado, dados apagados.\n")

        # Depois de rodar → espera até o próximo dia
        logging.info("⏱ Execução concluída. Aguardando próximo dia útil...\n")
        proximo = (datetime.now() + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
        espera = (proximo - datetime.now()).total_seconds()
        time.sleep(espera)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("🛑 Execução interrompida manualmente (CTRL+C).")
