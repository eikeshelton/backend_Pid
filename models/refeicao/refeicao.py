# models/refeicao.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Refeicao(Base):
    __tablename__ = "refeicoes"
    
    nome = Column(String)
    descricao = Column(Text)
    
    alimentos = relationship("Alimento",
                             secondary="refeicoes_alimentos",
                             back_populates="refeicoes")
