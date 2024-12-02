from sqlalchemy import Column, Integer, String
from models.aadeclarative_base import Base
from sqlalchemy.orm import relationship
# Definindo o modelo com SQLAlchemy


class Exercicio(Base):
    __tablename__ = 'exercicios'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Aqui o `id` será autoincrementado automaticamente pelo PostgreSQL
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    personalizar_exercicio = relationship('ExercicioPersonalizado', back_populates='exercicio')