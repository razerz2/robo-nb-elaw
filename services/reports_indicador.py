from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time


def _preencher_datas(driver, wait, data_inicial, data_final):
    """Preenche o intervalo de datas no formulário."""
    campo_de = wait.until(EC.presence_of_element_located((By.ID, "tabSearchTab:dataFrom_input")))
    campo_ate = wait.until(EC.presence_of_element_located((By.ID, "tabSearchTab:dataTo_input")))
    campo_de.clear(); campo_de.send_keys(data_inicial)
    campo_ate.clear(); campo_ate.send_keys(data_final)
    print(f"📅 Datas aplicadas: {data_inicial} → {data_final}")


def _selecionar_checkbox_tarefa(driver, wait):
    """Marca o checkbox 'Tarefa'."""
    label = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[@for='tabSearchTab:comboAgendamentoClasse:1']"))
    )
    label.click()
    print("☑️ Checkbox tarefa marcado.")


def _selecionar_status(driver, wait, validos):
    """Desmarca todos os tokens e seleciona apenas os status válidos."""
    tokens = driver.find_elements(By.CSS_SELECTOR, ".ui-selectcheckboxmenu-token-icon")
    for t in tokens:
        try:
            t.click(); time.sleep(0.2)
        except:
            pass

    dropdown = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".ui-selectcheckboxmenu-multiple-container"))
    )
    dropdown.click(); time.sleep(0.5)

    opcoes = driver.find_elements(By.CSS_SELECTOR, "li.ui-selectcheckboxmenu-item")
    for o in opcoes:
        if o.text.strip() in validos:
            o.click()
            print(f"✔️ Selecionado: {o.text.strip()}")

    dropdown.click()
    time.sleep(0.5)


def _abrir_dialog_excel(driver, wait):
    """Abre o diálogo do Excel e muda para o iframe."""
    btn_excel = wait.until(EC.element_to_be_clickable((By.ID, "btnExcel")))
    btn_excel.click()
    print("📥 Botão Excel clicado.")

    wait.until(EC.visibility_of_element_located((By.ID, "btnExcel_dlg")))
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btnExcel_dlg iframe")))
    driver.switch_to.frame(iframe)
    print("🔄 Mudamos para o iframe do relatório.")


def _configurar_modelo(driver, wait):
    """Seleciona modelo pré-configurado e relatório 'Tarefas'."""
    # Modelo pré-configurado
    lbl = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[@for='elawReportForm:elawReportOption:0']"))
    )
    lbl.click()
    print("☑️ Selecionado: Modelos pré-configurados")

    btn_continuar = wait.until(EC.element_to_be_clickable((By.ID, "elawReportForm:continuarBtn")))
    btn_continuar.click()
    print("➡️ Continuar clicado.")

    # Dropdown Tarefas
    dd = wait.until(EC.element_to_be_clickable((By.ID, "elawReportForm:selectElawReport_label")))
    dd.click()
    opcoes = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
            "ul[id$='selectElawReport_items'] li.ui-selectonemenu-item"))
    )
    time.sleep(1)

    alvo = next((o for o in opcoes if o.text.strip() == "Tarefas"), None)
    if not alvo:
        raise Exception("❌ Opção 'Tarefas' não encontrada!")

    wait.until(EC.element_to_be_clickable(alvo)).click()
    print("✔️ Relatório selecionado: Tarefas")

    # Botão gerar
    btn_gerar = wait.until(EC.element_to_be_clickable((By.ID, "elawReportForm:elawReportGerarBtn")))
    btn_gerar.click()
    print("📊 Gerar relatório clicado.")


def _capturar_id(driver, wait):
    """Captura o ID do relatório gerado."""
    id_elem = wait.until(EC.presence_of_element_located((
        By.XPATH, "//span[normalize-space()='ID']/ancestor::div[contains(@class,'ui-g')]/div[last()]"
    )))
    relatorio_id = id_elem.text.strip()
    print(f"🆔 Relatório solicitado com ID: {relatorio_id}")
    return relatorio_id


def gerar_relatorio(driver):
    """
    Fluxo completo:
    - Acessa a tela
    - Preenche filtros
    - Abre Excel -> Tarefas
    - Gera relatório
    - Retorna o ID
    """
    wait = WebDriverWait(driver, 30)
    url_relatorio = "https://sicredi.elaw.com.br/agendamentoContenciosoList.elaw"
    driver.get(url_relatorio)

    hoje = datetime.now()
    ano = hoje.year
    #data_inicial = f"01/01/{ano} 00:00"
    data_inicial = "18/09/2025 00:00"
    data_final = hoje.strftime("%d/%m/%Y") + " 23:59"

    time.sleep(2)
    _preencher_datas(driver, wait, data_inicial, data_final)
    time.sleep(1)
    _selecionar_checkbox_tarefa(driver, wait)
    time.sleep(1)
    _selecionar_status(driver, wait, {"Concluídas", "Concluídas em atraso"})

    # Pesquisar
    btn = wait.until(EC.element_to_be_clickable((By.ID, "tabSearchTab:btnPesquisar")))
    btn.click()
    print("🔎 Pesquisa disparada.")

    # Excel
    _abrir_dialog_excel(driver, wait)
    time.sleep(2)
    _configurar_modelo(driver, wait)
    time.sleep(2)
    relatorio_id = _capturar_id(driver, wait)

    # Volta pro principal e recarrega
    driver.switch_to.default_content()
    driver.refresh()
    print("🔄 Página recarregada.")

    return relatorio_id
