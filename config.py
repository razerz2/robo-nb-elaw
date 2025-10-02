import os
from dotenv import load_dotenv

load_dotenv()

# Credenciais
USER = os.getenv("EUSER")
PASSWORD = os.getenv("EPASS")

# URLs principais
URL_INICIAL = "https://sicredi.elaw.com.br/processoView.elaw"
URL_LOGOUT = "https://sicredi.elaw.com.br/logout"

#Intervalo de Execução
INTERVALO_EXECUCAO = 60
INTERVALO_BAIXAR = 5
INTERVALO = 30