# models/treinamento.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from typing import Optional
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Treinamento(Base):
    __tablename__ = 'treinamento'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Optional[str] = Column(Text, default=None)
    dia_da_semana = Optional[str] = Column(String(20), default=None)
    is_publico = Column(Boolean, default=False)

    usuario = relationship('Usuario', back_populates='treinamentos')
    exercicios = relationship('ExercicioPersonalizado', back_populates='treinamento', cascade='all, delete-orphan')