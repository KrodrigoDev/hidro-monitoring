from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.model.database import Base


class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    usuarios = relationship("Usuario", back_populates="empresa")
    equipamentos = relationship("Equipamento", back_populates="empresa")


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String)
    cpf = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    id_empresa = Column(Integer, ForeignKey("empresa.id"))

    empresa = relationship("Empresa", back_populates="usuarios")
    logs = relationship("Log", back_populates="usuario")


class LocalEquipamento(Base):
    __tablename__ = "local_equipamento"

    id = Column(Integer, primary_key=True, index=True)
    municipio = Column(String)
    bairro = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    equipamentos = relationship("Equipamento", back_populates="local_equipamento")


class Equipamento(Base):
    __tablename__ = "equipamento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    tipo = Column(String)
    situacao = Column(String)
    voltagem = Column(String)
    vazao = Column(Float)
    profundidade = Column(Float)
    ult_manutencao = Column(Date)
    ult_limpeza = Column(Date)
    id_empresa = Column(Integer, ForeignKey("empresa.id"))
    id_local_equipamento = Column(Integer, ForeignKey("local_equipamento.id"))

    empresa = relationship("Empresa", back_populates="equipamentos")
    local_equipamento = relationship("LocalEquipamento", back_populates="equipamentos")
    logs = relationship("Log", back_populates="equipamento")  # ✅ ligação com Log


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    acao = Column(String, nullable=False)  # criar, alterar, editar, excluir
    id_usuario = Column(Integer, ForeignKey("usuario.id"))
    id_equipamento = Column(Integer, ForeignKey("equipamento.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    usuario = relationship("Usuario", back_populates="logs")
    equipamento = relationship("Equipamento", back_populates="logs")
