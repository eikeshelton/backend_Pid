# models.municipio.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Municipio(Base):
    __tablename__ = "municipio"

    codigo_ibge = Column(Integer, primary_key=True, index=True)  # Definindo codigo_ibge como chave primária
    nome = Column(String(100), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.codigo_ibge"), nullable=False)

    estado = relationship("Estado", back_populates="municipios")
    parceiros_treino = relationship("ParceiroTreino", back_populates="municipio_relacionamento")
