# models/usuario.py
from sqlalchemy import Column, String, Date, BINARY, INTEGER
from sqlalchemy.orm import relationship
from models.declarative_base import Base

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

    pesquisas = relationship("HistoricoPesquisa", back_populates="usuario", foreign_keys="HistoricoPesquisa.usuario_id")
    pesquisas_pesquisado = relationship("HistoricoPesquisa", back_populates="pesquisado", foreign_keys="HistoricoPesquisa.pesquisado_id")
