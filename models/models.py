# models/usuario.py
from sqlalchemy import Column, String, Date, BINARY, INTEGER,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(INTEGER, primary_key=True)
    email = Column(String)
    nome_usuario = Column(String)
    login = Column(String)
    senha = Column(String)
    tipo_usuario = Column(String)
    data_nascimento = Column(Date)
    foto_perfil = Column(BINARY)
    bio = Column(String)
    seguidores = Column(INTEGER, default=0)
    seguidos = Column(INTEGER, default=0)
    token_reset_senha = Column(String)
    pesquisas = relationship("HistoricoPesquisa", back_populates="usuario")

class HistoricoPesquisa(Base):
    __tablename__ = 'historico_pesquisa'

    id = Column(INTEGER, primary_key=True, index=True)
    usuario_id = Column(INTEGER, ForeignKey('usuario.id'))  # Verifique se o nome da tabela está correto
    texto_pesquisa = Column(String, index=True)
    data_pesquisa = Column(DateTime, default=datetime.now)

    # Relacionamento com a tabela de usuários
    usuario = relationship("Usuario", back_populates="pesquisas")