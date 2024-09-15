# models/alimento_usuario.py
from sqlalchemy import Column, Integer, String, Text,ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class AlimentoUsuario(Base):
    __tablename__ = "alimento_usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_alimento = Column(Integer, ForeignKey('alimentos.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    quantidade_g=Column(Integer, nullable=False)