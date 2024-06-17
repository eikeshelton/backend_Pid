from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Municipio(Base):
    __tablename__ = "municipio"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo_ibge = Column(Integer, nullable=False, unique=True)
    estado_id = Column(Integer, ForeignKey("estado.codigo_ibge"), nullable=False)

    estado = relationship("Estado", back_populates="municipios")
    parceiros_treino = relationship("ParceiroTreino", back_populates="municipio")
