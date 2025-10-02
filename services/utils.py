import time
import sys
import select
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