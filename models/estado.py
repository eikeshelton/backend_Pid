# models.estado.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Estado(Base):
    __tablename__ = "estado"

    codigo_ibge = Column(Integer, primary_key=True, index=True)  # Definindo codigo_ibge como chave primária
    nome = Column(String(100), nullable=False)
    sigla = Column(String(2), nullable=False)

    municipios = relationship("Municipio", back_populates="estado")
    parceiros_treino = relationship("ParceiroTreino", back_populates="estado_relacionamento")
