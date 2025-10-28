import bcrypt
import pandas as pd
from sqlalchemy.orm import Session

from src.model import models


# ==========================================================
# 🔹 CRUD - USUÁRIO
# ==========================================================

def gerar_hash_senha(senha: str) -> str:
    """Gera o hash da senha com bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def criar_usuario(db: Session, nome: str, sobrenome: str, cpf: str, senha: str, id_empresa: int):
    senha_hash = gerar_hash_senha(senha)
    usuario = models.Usuario(
        nome=nome,
        sobrenome=sobrenome,
        cpf=cpf,
        senha=senha_hash,
        id_empresa=id_empresa,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# ==========================================================
# 🔹 CRUD - EQUIPAMENTO
# ==========================================================

def criar_local_equipamento(
        db: Session,
        municipio: str,
        bairro: str,
        latitude: float,
        longitude: float,
):
    local_equipamento_equipamento = models.LocalEquipamento(
        municipio=municipio,
        bairro=bairro,
        latitude=latitude,
        longitude=longitude
    )
    db.add(local_equipamento_equipamento)
    db.commit()
    db.refresh(local_equipamento_equipamento)
    return local_equipamento_equipamento


def criar_equipamento(
        db: Session,
        nome: str,
        tipo: str,
        situacao: str,
        voltagem: str,
        vazao: float,
        profundidade: float,
        ult_manutencao=None,
        ult_limpeza=None,
        id_empresa=None,
        id_local_equipamento=None
):
    equipamento = models.Equipamento(
        nome=nome,
        tipo=tipo,
        situacao=situacao,
        voltagem=voltagem,
        vazao=vazao,
        profundidade=profundidade,
        ult_manutencao=ult_manutencao,
        ult_limpeza=ult_limpeza,
        id_empresa=id_empresa,
        id_local_equipamento=id_local_equipamento
    )
    db.add(equipamento)
    db.commit()
    db.refresh(equipamento)
    return equipamento


def listar_equipamentos_com_local(db: Session, id_empresa: int = None) -> pd.DataFrame:
    """
    Lista equipamentos com informações do local.
    Retorna um DataFrame com as colunas:
    equipamento.id, tipo, situacao, voltagem, vazao, profundidade,
    ult_manutencao, ult_limpeza,
    local.municipio, local.bairro, local.area, local.latitude, local.longitude
    """
    query = db.query(
        models.Equipamento.id,
        models.Equipamento.nome,
        models.Equipamento.tipo,
        models.Equipamento.situacao,
        models.Equipamento.voltagem,
        models.Equipamento.vazao,
        models.Equipamento.profundidade,
        models.Equipamento.ult_manutencao,
        models.Equipamento.ult_limpeza,
        models.LocalEquipamento.municipio,
        models.LocalEquipamento.bairro,
        models.LocalEquipamento.latitude,
        models.LocalEquipamento.longitude
    ).join(
        models.LocalEquipamento,
        models.Equipamento.id_local_equipamento == models.LocalEquipamento.id
    )

    if id_empresa:
        query = query.filter(models.Equipamento.id_empresa == id_empresa)

    resultados = query.all()

    df = pd.DataFrame(resultados, columns=[
        "id_equipamento", "nome", "tipo", "situacao", "voltagem", "vazao", "profundidade",
        "ult_manutencao", "ult_limpeza",
        "municipio", "bairro", "latitude", "longitude"
    ])

    return df


def registrar_log(db: Session, id_usuario: int, acao: str, id_equipamento: int = None):
    """
    Registra uma ação realizada pelo usuário no sistema.

    Parâmetros:
        db (Session): Sessão ativa do banco de dados
        id_usuario (int): ID do usuário que realizou a ação
        acao (str): Descrição da ação ('criar', 'editar', 'excluir', 'modificar', etc.)
        id_equipamento (int, opcional): ID do equipamento relacionado à ação

    Retorna:
        Log (objeto): Instância do log criado
    """
    log = models.Log(
        acao=acao,
        id_usuario=id_usuario,
        id_equipamento=id_equipamento
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


# ==========================================================
# 🔹 LOGS DE AÇÕES
# ==========================================================

def registrar_log(db: Session, id_usuario: int, acao: str, id_equipamento: int = None):
    """
    Registra uma ação realizada pelo usuário no sistema.

    Parâmetros:
        db (Session): Sessão ativa do banco de dados
        id_usuario (int): ID do usuário que realizou a ação
        acao (str): Descrição da ação ('criar', 'editar', 'excluir', 'modificar', etc.)
        id_equipamento (int, opcional): ID do equipamento relacionado à ação

    Retorna:
        Log (objeto): Instância do log criado
    """
    log = models.Log(
        acao=acao,
        id_usuario=id_usuario,
        id_equipamento=id_equipamento
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def listar_logs_usuario(db: Session) -> pd.DataFrame:
    """
    Retorna um DataFrame com todas as ações (logs) realizadas por todos os usuários.

    Inclui:
      - ID do log
      - ID e nome do usuário
      - Ação e data/hora
      - Informações do equipamento (id, nome, tipo)
      - Local do equipamento (município e bairro)
    """
    query = (
        db.query(
            models.Log.id.label("id_log"),
            models.Usuario.id.label("id_usuario"),
            models.Usuario.nome.label("nome_usuario"),
            models.Log.acao,
            models.Log.created_at.label("data"),
            models.Equipamento.id.label("id_equipamento"),
            models.Equipamento.nome.label("nome_equipamento"),
            models.Equipamento.tipo.label("tipo"),
            models.LocalEquipamento.municipio.label("municipio"),
            models.LocalEquipamento.bairro.label("bairro"),
        )
        .join(models.Usuario, models.Log.id_usuario == models.Usuario.id)
        .join(models.Equipamento, models.Log.id_equipamento == models.Equipamento.id, isouter=True)
        .join(models.LocalEquipamento, models.Equipamento.id_local_equipamento == models.LocalEquipamento.id, isouter=True)
        .order_by(models.Log.created_at.desc())
    )

    resultados = query.all()

    df = pd.DataFrame(
        resultados,
        columns=[
            "id_log", "id_usuario", "nome_usuario",
            "acao", "data",
            "id_equipamento", "nome_equipamento", "tipo",
            "municipio", "bairro"
        ],
    )

    return df

