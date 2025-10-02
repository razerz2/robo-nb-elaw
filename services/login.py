from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def logar(driver):
    """
    Realiza login no sistema Elaw.
    """
    driver.get("https://sicredi.elaw.com.br/login.elaw")
    wait = WebDriverWait(driver, 30)

    # Exemplo, ajuste de acordo com seus campos de login:
    usuario = wait.until(EC.presence_of_element_located((By.ID, "username")))
    senha = wait.until(EC.presence_of_element_located((By.ID, "password")))

    usuario.send_keys("seu_usuario")
    senha.send_keys("sua_senha")

    botao = wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))
    botao.click()

    print("✅ Login realizado com sucesso!")
