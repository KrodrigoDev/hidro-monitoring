import bcrypt
from sqlalchemy.orm import Session

from src.model import models


def verificar_senha(senha_informada: str, senha_hash: str) -> bool:
    """Verifica se a senha informada confere com o hash armazenado."""
    return bcrypt.checkpw(senha_informada.encode('utf-8'), senha_hash.encode('utf-8'))


def validar_login(db: Session, nome: str, senha: str):
    """
    Valida o login de um usuário pelo nome e senha.
    Retorna o objeto Usuario se válido, senão None.
    """
    usuario = db.query(models.Usuario).filter(models.Usuario.nome == nome).first()
    if not usuario:
        return None

    if verificar_senha(senha, usuario.senha):
        return usuario
    return None
