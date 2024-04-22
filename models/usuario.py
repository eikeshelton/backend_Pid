# models/usuario.py

from sqlalchemy import Column, String, Date, BINARY,INTEGER
from sqlalchemy.ext.declarative import declarative_base

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
