from sqlalchemy.orm import Session
from src.model.database import Base, engine
from src.model import models, crud

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)


def criar_dados_padrao():
    db = Session(bind=engine)

    empresa_existente = db.query(models.Empresa).first()
    if not empresa_existente:
        empresa_padrao = models.Empresa(
            nome="Daesc",
            descricao='Departamento de água e esgoto de coruripe'
        )
        db.add(empresa_padrao)
        db.commit()
        db.refresh(empresa_padrao)
    else:
        empresa_padrao = empresa_existente

    usuario_existente = db.query(models.Usuario).first()
    if not usuario_existente:
        crud.criar_usuario(
            db,
            nome="Admin",
            sobrenome="Sistema",
            cpf="00000000000",
            senha=f"senha123",
            id_empresa=empresa_padrao.id
        )

    db.close()


if __name__ == "__main__":
    criar_dados_padrao()
