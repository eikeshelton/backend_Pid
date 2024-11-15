# models/exercicio_personalizado.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class ExercicioPersonalizado(Base):
    __tablename__ = 'exercicio_personalizado'
    id = Column(Integer, primary_key=True)
    treinamento_id = Column(Integer, ForeignKey('treinamento.id', ondelete='CASCADE'), nullable=False)
    api_exercicio_id = Column(Integer, nullable=False)
    nome_exercicio = Column(String(100), nullable=False)
    notas = Column(Text)
    repeticoes = Column(Integer)
    series = Column(Integer)
    carga_kg = Column(Integer)
    tempo_descanso_seg = Column(Integer)

    treinamento = relationship('Treinamento', back_populates='exercicios')