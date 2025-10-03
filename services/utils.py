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
    Aguarda o download terminar e renomeia o arquivo para nome_final.
    Se já existir um arquivo com esse nome, ele será sobrescrito.
    """
    tempo_inicial = time.time()
    arquivo_final = os.path.join(pasta_downloads, nome_final)

    while True:
        # procura arquivos baixados
        arquivos = [f for f in os.listdir(pasta_downloads) if f.endswith(".crdownload") or f.endswith(".tmp")]
        if not arquivos:
            # pega o último arquivo baixado
            arquivos = [f for f in os.listdir(pasta_downloads)]
            if arquivos:
                ultimo = max([os.path.join(pasta_downloads, f) for f in arquivos], key=os.path.getctime)

                # se já existir o arquivo final, apaga
                if os.path.exists(arquivo_final):
                    os.remove(arquivo_final)

                # renomeia o último baixado para o nome final
                os.rename(ultimo, arquivo_final)
                print(f"✅ Download finalizado e salvo como: {arquivo_final}")
                return arquivo_final

        if time.time() - tempo_inicial > timeout:
            raise TimeoutError("⏳ Tempo limite atingido esperando download terminar...")

        time.sleep(1)