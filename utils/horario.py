from datetime import datetime
import time

def dentro_do_horario():
    """
    Verifica se está em dias úteis (Seg-Sex) e no horário das 08h às 18h.
    """
    agora = datetime.now()
    if agora.weekday() >= 5:  # sábado(5) ou domingo(6)
        return False
    if 8 <= agora.hour < 18:
        return True
    return False

def esperar_proximo_horario():
    """
    Espera 5 minutos antes de verificar novamente.
    """
    print("⏸ Fora do horário de execução (Seg-Sex, 08h às 18h).")
    time.sleep(300)
