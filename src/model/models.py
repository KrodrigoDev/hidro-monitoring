from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


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


class LocalEquipamento(Base):
    __tablename__ = "local_equipamento"
    id = Column(Integer, primary_key=True, index=True)
    municipio = Column(String)
    bairro = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    equipamentos = relationship("Equipamento", back_populates="local_equipamento")
