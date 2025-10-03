import os
import time
import sys
from datetime import datetime

def esperar(segundos):
    print(f"⏳ Aguardando {segundos}s...")
    time.sleep(segundos)

def perguntar_com_timeout(pergunta, timeout=15):
    """
    Pergunta ao usuário com timeout.
    Compatível com Windows (msvcrt) e Linux/Mac (select).
    """
    print(pergunta, end="", flush=True)

    if sys.platform.startswith("win"):  # Windows usa msvcrt
        import msvcrt
        start = time.time()
        resposta = ""
        while True:
            if msvcrt.kbhit():
                char = msvcrt.getche().decode("utf-8")
                if char in ["\r", "\n"]:  # Enter
                    break
                resposta += char
            if time.time() - start > timeout:
                print("\n⏰ Tempo esgotado, assumindo 'N'.")
                return "n"
        print("")  # pular linha após enter
        return resposta.strip().lower()

    else:  # Linux/Mac usa select
        import select
        start = time.time()
        resposta = ""
        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                resposta = sys.stdin.readline().strip().lower()
                break
            if time.time() - start > timeout:
                print("\n⏰ Tempo esgotado, assumindo 'N'.")
                return "n"
        return resposta

def dentro_horario():
    """Retorna True se agora é entre seg-sex 08h–18h."""
    agora = datetime.now()
    return agora.weekday() < 5 and 8 <= agora.hour < 18

def esperar_download(pasta_downloads, nome_final, timeout=120):
    """
    Aguarda o arquivo terminar o download na pasta especificada e renomeia para 'nome_final'.
    """
    tempo_inicial = time.time()
    arquivo_baixado = None

    while time.time() - tempo_inicial < timeout:
        arquivos = os.listdir(pasta_downloads)
        for arquivo in arquivos:
            if arquivo.endswith(".tmp"):
                # Ainda baixando
                continue
            if arquivo != nome_final:  
                # encontramos o arquivo baixado
                caminho_antigo = os.path.join(pasta_downloads, arquivo)
                caminho_novo = os.path.join(pasta_downloads, nome_final)
                os.rename(caminho_antigo, caminho_novo)
                print(f"✅ Download concluído e renomeado para: {nome_final}")
                return caminho_novo
        time.sleep(2)

    raise TimeoutError("⏰ Tempo esgotado esperando o download finalizar.")