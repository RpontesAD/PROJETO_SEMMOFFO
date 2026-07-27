from database import *
from monitor import *
from datetime import datetime

def mostrar_rotinas():
    print("\n=== ROTINAS ===")

    for rotina in listar_rotinas():
        print(rotina)


def mostrar_monitoramentos(rotina_id):
    print(f"\n=== MONITORAMENTOS DA ROTINA {rotina_id} ===")

    for monitoramento in listar_monitoramentos(rotina_id):
        print(monitoramento)

#prazo = calcular_ultimo_prazo(
#    "MENSAL",
#    "09:00",
#    regra_dia="ULTIMO_DIA_UTIL"
#)


#arquivo = datetime(
#    2026,
#    6,
#    20,
#    9,
#    0
#)


#status = verificar_status(
#    arquivo,
#    prazo
#)


#print("Prazo:", prazo)
#print("Arquivo:", arquivo)
#print("Status:", status)

print(verificar_rotina(1))
