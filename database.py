import sqlite3

DB = "banco.db"

# Conexão com o banco de dados
def conectar():
    return sqlite3.connect(DB)

# Cria as tabelas - Se não existirem
def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rotinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nome TEXT NOT NULL,

        executavel TEXT,

        periodo TEXT NOT NULL,

        hora TEXT NOT NULL,

        regra_dia TEXT,

        dia_semana INTEGER,

        dia_mes INTEGER,

        ativo INTEGER NOT NULL DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoramentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rotina_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        pasta TEXT NOT NULL,
        arquivo TEXT,
        obrigatorio INTEGER NOT NULL DEFAULT 1,

        FOREIGN KEY(rotina_id)
            REFERENCES rotinas(id)
            ON DELETE CASCADE
    )
    """)

    conexao.commit()
    conexao.close()
    
# ---------- ROTINAS ----------
    
# Função de criação de rotina 
def criar_rotina(
    nome,
    executavel,
    periodo,
    hora,
    regra_dia=None,
    dia_semana=None,
    dia_mes=None,
    ativo=1
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO rotinas
        (
            nome,
            executavel,
            periodo,
            hora,
            regra_dia,
            dia_semana,
            dia_mes,
            ativo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        executavel,
        periodo,
        hora,
        regra_dia,
        dia_semana,
        dia_mes,
        ativo
    ))

    conexao.commit()
    conexao.close()
    
# Função que lista todas as rotinas    
def listar_rotinas_ativas():

    conexao = conectar()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM rotinas
        WHERE ativo = 1
        ORDER BY nome
    """)

    rotinas = cursor.fetchall()

    conexao.close()

    return [dict(rotina) for rotina in rotinas]

def listar_rotinas_inativas():

    conexao = conectar()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM rotinas
        WHERE ativo = 0
        ORDER BY nome
    """)

    rotinas = cursor.fetchall()

    conexao.close()

    return [dict(rotina) for rotina in rotinas]

def restaurar_rotina(id_rotina):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE rotinas
        SET ativo = 1
        WHERE id = ?
    """, (id_rotina,))

    conexao.commit()
    conexao.close()

# Função para INATIVAR rotina - Caso precise reativar
def inativar_rotina(id_rotina):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE rotinas
        SET ativo = 0
        WHERE id = ?
    """, (id_rotina,))

    conexao.commit()
    conexao.close()
    
def excluir_rotina(id_rotina):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM monitoramentos
        WHERE rotina_id = ?
    """, (id_rotina,))

    cursor.execute("""
        DELETE FROM rotinas
        WHERE id = ?
    """, (id_rotina,))

    conexao.commit()
    conexao.close()
    
# Função para buscar rotina    
def buscar_rotina(id_rotina):

    conexao = conectar()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM rotinas
        WHERE id = ?
    """, (id_rotina,))

    rotina = cursor.fetchone()

    conexao.close()

    return dict(rotina)

# Atualiza os DADOS da rotina
def atualizar_rotina(
    id_rotina,
    nome,
    executavel,
    periodo,
    hora,
    regra_dia=None,
    dia_semana=None,
    dia_mes=None,
    ativo=1
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE rotinas

        SET
            nome = ?,
            executavel = ?,
            periodo = ?,
            hora = ?,
            regra_dia = ?,
            dia_semana = ?,
            dia_mes = ?,
            ativo = ?

        WHERE id = ?
    """, (
        nome,
        executavel,
        periodo,
        hora,
        regra_dia,
        dia_semana,
        dia_mes,
        ativo,
        id_rotina
    ))

    conexao.commit()
    conexao.close()
    
# ---------- MONITORAMENTO ----------    

# Função para criar o monitoramento
def criar_monitoramento(
    rotina_id,
    tipo,
    pasta,
    arquivo=None,
    obrigatorio=1
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO monitoramentos
        (
            rotina_id,
            tipo,
            pasta,
            arquivo,
            obrigatorio
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        rotina_id,
        tipo,
        pasta,
        arquivo,
        obrigatorio
    ))

    conexao.commit()
    conexao.close()
    
# Função para listar monitoramentos
def listar_monitoramentos(rotina_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM monitoramentos
        WHERE rotina_id = ?
        ORDER BY id
    """, (rotina_id,))

    monitoramentos = cursor.fetchall()

    conexao.close()

    return monitoramentos

# Função que busca monitoramento expecífico
def buscar_monitoramento(id_monitoramento):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM monitoramentos
        WHERE id = ?
    """, (id_monitoramento,))

    monitoramento = cursor.fetchone()

    conexao.close()

    return monitoramento

# Função que conta quantos monitoramentos tem em uma rotina
def contar_monitoramentos(rotina_id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM monitoramentos
        WHERE rotina_id = ?
    """, (rotina_id,))

    quantidade = cursor.fetchone()[0]

    conexao.close()

    return quantidade

# Função para atualizar DADOS do monitoramento
def atualizar_monitoramento(
    id_monitoramento,
    tipo,
    pasta,
    arquivo,
    obrigatorio
):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE monitoramentos

        SET
            tipo = ?,
            pasta = ?,
            arquivo = ?,
            obrigatorio = ?

        WHERE id = ?
    """, (
        tipo,
        pasta,
        arquivo,
        obrigatorio,
        id_monitoramento
    ))

    conexao.commit()
    conexao.close()
    
# Função que EXCLUI um monitoramento   
def excluir_monitoramento(id_monitoramento):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE
        FROM monitoramentos
        WHERE id = ?
    """, (id_monitoramento,))

    conexao.commit()
    conexao.close()