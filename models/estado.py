from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sigla = Column(String(2), nullable=False)
    codigo_ibge = Column(Integer, nullable=False, unique=True)

    municipios = relationship("Municipio", back_populates="estado")
    parceiros_treino = relationship("ParceiroTreino", back_populates="estado")