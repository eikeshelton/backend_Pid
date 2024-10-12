# models/usuario.py
from sqlalchemy import Column, String, Date,Integer,ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True)
    email = Column(String)
    nome_usuario = Column(String)
    login = Column(String)
    senha = Column(String)
    tipo_usuario_id = Column(Integer, ForeignKey("tipo_usuario.id"))
    data_nascimento = Column(Date)
    foto_perfil = Column(String)
    bio = Column(String)
    seguidores = Column(Integer, default=0)
    seguidos = Column(Integer, default=0)
    publicacoes = Column(Integer, default=0)
    token_reset_senha = Column(String)
    sexo = Column(String(50))
    fcm_token = Column(String, nullable=True)  
    pesquisas = relationship("HistoricoPesquisa", back_populates="usuario", foreign_keys="HistoricoPesquisa.usuario_id")
    pesquisas_pesquisado = relationship("HistoricoPesquisa", back_populates="pesquisado", foreign_keys="HistoricoPesquisa.pesquisado_id")
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")

class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"
    id = Column(Integer, primary_key=True)
    tipo= Column(String)
    usuarios = relationship("Usuario", back_populates="tipo_usuario")
