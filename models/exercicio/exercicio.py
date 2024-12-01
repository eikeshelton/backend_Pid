from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Definindo o modelo com SQLAlchemy
Base = declarative_base()

class Exercicio(Base):
    __tablename__ = 'exercicios'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Aqui o `id` será autoincrementado automaticamente pelo PostgreSQL
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)