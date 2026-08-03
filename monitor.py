from pathlib import Path
from datetime import datetime, timedelta
from database import *

def eh_dia_util(data):
    
    # Segunda = 0
    # Domingo = 6

    return data.weekday() < 5

def primeiro_dia_util(ano, mes):

    data = datetime(
        ano,
        mes,
        1
    )

    while not eh_dia_util(data):
        data += timedelta(days=1)

    return data

def ultimo_dia_util(ano, mes):

    # primeiro dia do próximo mês
    if mes == 12:
        data = datetime(
            ano + 1,
            1,
            1
        )

    else:
        data = datetime(
            ano,
            mes + 1,
            1
        )


    # volta um dia para o último dia do mês atual
    data -= timedelta(days=1)


    while not eh_dia_util(data):
        data -= timedelta(days=1)


    return data

def calcular_ultimo_prazo(periodo, hora, regra_dia=None, dia_semana=None, dia_mes=None):

    agora = datetime.now()

    hora_obj = datetime.strptime(
        hora,
        "%H:%M"
    ).time()


    if periodo == "DIARIO":

        prazo = datetime.combine(
            agora.date(),
            hora_obj
        )

        # se ainda não chegou no horário de hoje,
        # o último prazo foi ontem
        if agora < prazo:
            prazo -= timedelta(days=1)

        return prazo
    
    elif periodo == "SEMANAL":

        if dia_semana is None:
            return None

        dia_semana = int(dia_semana)

        dias_desde_dia = (
            agora.weekday() - dia_semana
        ) % 7


        prazo = agora - timedelta(
            days=dias_desde_dia
        )


        prazo = datetime.combine(
            prazo.date(),
            hora_obj
        )


        # Se ainda não chegou no horário dessa semana,
        # volta para a semana anterior
        if agora < prazo:
            prazo -= timedelta(days=7)


        return prazo
    
    elif periodo == "MENSAL":


        if regra_dia == "PRIMEIRO_DIA_UTIL":

            prazo_data = primeiro_dia_util(
                agora.year,
                agora.month
            )


        elif regra_dia == "ULTIMO_DIA_UTIL":

            prazo_data = ultimo_dia_util(
                agora.year,
                agora.month
            )


        else:

            if not dia_mes:
                return None

            prazo_data = datetime(
                agora.year,
                agora.month,
                int(dia_mes)
            )


        prazo = datetime.combine(
            prazo_data.date(),
            hora_obj
        )


        # Se ainda não chegou nesse mês,
        # pega o mês anterior
        if agora < prazo:

            if agora.month == 1:
                ano = agora.year - 1
                mes = 12

            else:
                ano = agora.year
                mes = agora.month - 1


            if regra_dia == "PRIMEIRO_DIA_UTIL":

                prazo_data = primeiro_dia_util(
                    ano,
                    mes
                )


            elif regra_dia == "ULTIMO_DIA_UTIL":

                prazo_data = ultimo_dia_util(
                    ano,
                    mes
                )


            else:

                if not dia_mes:
                    return None

                prazo_data = datetime(
                    ano,
                    mes,
                    int(dia_mes)
                )


            prazo = datetime.combine(
                prazo_data.date(),
                hora_obj
            )


        return prazo
    
def calcular_proximo_prazo(periodo, hora, regra_dia=None, dia_semana=None, dia_mes=None):

    agora = datetime.now()

    hora_obj = datetime.strptime(hora, "%H:%M").time()

    if periodo == "DIARIO":

        prazo = datetime.combine(
            agora.date(),
            hora_obj
        )

        if agora >= prazo:
            prazo += timedelta(days=1)

        return prazo


    elif periodo == "SEMANAL":

        if dia_semana is None:
            return None

        dia_semana = int(dia_semana)

        dias_ate = (dia_semana - agora.weekday()) % 7

        prazo = agora + timedelta(days=dias_ate)

        prazo = datetime.combine(
            prazo.date(),
            hora_obj
        )

        if agora >= prazo:
            prazo += timedelta(days=7)

        return prazo


    elif periodo == "MENSAL":

        if regra_dia == "PRIMEIRO_DIA_UTIL":

            prazo_data = primeiro_dia_util(
                agora.year,
                agora.month
            )

        elif regra_dia == "ULTIMO_DIA_UTIL":

            prazo_data = ultimo_dia_util(
                agora.year,
                agora.month
            )

        else:

            if not dia_mes:
                return None

            prazo_data = datetime(
                agora.year,
                agora.month,
                int(dia_mes)
            )

        prazo = datetime.combine(
            prazo_data.date(),
            hora_obj
        )

        if agora >= prazo:

            if agora.month == 12:
                ano = agora.year + 1
                mes = 1
            else:
                ano = agora.year
                mes = agora.month + 1

            if regra_dia == "PRIMEIRO_DIA_UTIL":

                prazo_data = primeiro_dia_util(
                    ano,
                    mes
                )

            elif regra_dia == "ULTIMO_DIA_UTIL":

                prazo_data = ultimo_dia_util(
                    ano,
                    mes
                )

            else:

                prazo_data = datetime(
                    ano,
                    mes,
                    int(dia_mes)
                )

            prazo = datetime.combine(
                prazo_data.date(),
                hora_obj
            )

        return prazo

def verificar_arquivo(caminho):
    
    arquivo = Path(caminho)

    if not arquivo.exists():
        return {
            "existe": False,
            "caminho": str(arquivo),
            "data_modificacao": None
        }

    data = datetime.fromtimestamp(
        arquivo.stat().st_mtime
    )

    return {
        "existe": True,
        "caminho": str(arquivo),
        "data_modificacao": data
    }

def verificar_status(data_modificacao, ultimo_prazo):

    if data_modificacao >= ultimo_prazo:
        return "Atualizado"

    return "Atrasado"
    
def verificar_rotina(id_rotina):

    rotina = buscar_rotina(id_rotina)

    if not rotina:
        return None


    id = rotina["id"]
    nome = rotina["nome"]
    executavel = rotina["executavel"]
    periodo = rotina["periodo"]
    hora = rotina["hora"]
    regra_dia = rotina["regra_dia"]
    dia_semana = rotina["dia_semana"]
    dia_mes = rotina["dia_mes"]
    ativo = rotina["ativo"]


    prazo = calcular_ultimo_prazo(
        periodo,
        hora,
        regra_dia,
        dia_semana,
        dia_mes
    )
    
    proximo_prazo = calcular_proximo_prazo(
        periodo,
        hora,
        regra_dia,
        dia_semana,
        dia_mes
    )


    monitoramentos = listar_monitoramentos(
        id_rotina
    )


    resultado = {
        "id": id,
        "nome": nome,
        "executavel": executavel,
        "periodicidade": periodo,
        "hora": hora,
        "prazo": prazo,
        "proximo_prazo": proximo_prazo,
        "monitoramentos": len(monitoramentos),
        "arquivos": []
    }


    for monitoramento in monitoramentos:

        id_monitoramento = monitoramento["id"]
        tipo = monitoramento["tipo"]
        pasta = monitoramento["pasta"]
        arquivo = monitoramento["arquivo"]
        obrigatorio = monitoramento["obrigatorio"]
        nome = monitoramento["nome"]


        if tipo == "ARQUIVO_ALVO":

            caminho = Path(
                pasta,
                arquivo
            )

            info = verificar_arquivo(caminho)

            nome_arquivo = arquivo


        elif tipo == "ULTIMO_ARQUIVO":

            info = buscar_ultimo_arquivo(pasta)

            nome_arquivo = info["arquivo"]


        if not info["existe"]:

            status = "Arquivo não encontrado"

        else:

            if prazo is None:
                status = "Configuração inválida"
            else:
                status = verificar_status(
                    info["data_modificacao"],
                    prazo
                )


        resultado["arquivos"].append({
            "id": id_monitoramento,
            "tipo": tipo,
            "nome": nome,
            "arquivo": nome_arquivo,
            "caminho": info.get("caminho"),
            "data_modificacao": info["data_modificacao"].strftime("%Y-%m-%d %H:%M") if info["data_modificacao"] else None,
            "status": status

        })


    return resultado

def buscar_ultimo_arquivo(pasta):

    pasta = Path(pasta)

    if not pasta.exists() or not pasta.is_dir():
        return {
            "existe": False,
            "arquivo": None,
            "caminho": None,
            "data_modificacao": None
        }

    arquivos_ignorados = {
    "desktop.ini"
}

    arquivos = [
        arquivo
        for arquivo in pasta.iterdir()
        if arquivo.is_file()
        and arquivo.name.lower() not in arquivos_ignorados
    ]

    if not arquivos:
        return {
            "existe": False,
            "arquivo": None,
            "caminho": None,
            "data_modificacao": None
        }

    arquivo_recente = max(
        arquivos,
        key=lambda arquivo: arquivo.stat().st_mtime
    )

    return {
        "existe": True,
        "arquivo": arquivo_recente.name,
        "caminho": str(arquivo_recente),
        "data_modificacao": datetime.fromtimestamp(
            arquivo_recente.stat().st_mtime
        )
    }