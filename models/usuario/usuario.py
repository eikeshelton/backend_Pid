# models/usuario.py
from sqlalchemy import Column, String, Date, BINARY, Integer
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True)
    email = Column(String)
    nome_usuario = Column(String)
    login = Column(String)
    senha = Column(String)
    tipo_usuario = Column(String)
    data_nascimento = Column(Date)
    foto_perfil = Column(BINARY)
    bio = Column(String)
    seguidores = Column(Integer, default=0)
    seguidos = Column(Integer, default=0)
    token_reset_senha = Column(String)
    sexo = Column(String(50))  
    pesquisas = relationship("HistoricoPesquisa", back_populates="usuario", foreign_keys="HistoricoPesquisa.usuario_id")
    pesquisas_pesquisado = relationship("HistoricoPesquisa", back_populates="pesquisado", foreign_keys="HistoricoPesquisa.pesquisado_id")

