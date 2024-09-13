# models/alimentos.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Alimento(Base):
    __tablename__ = "alimentos"
    
    numero = Column(Integer)
    grupo = Column(String)
    descricao = Column(String)
    energia_kcal = Column(Float)
    proteina_g = Column(Float)
    carboidrato_g = Column(Float)
    quantidade_g = Column(Float)
    
    refeicoes = relationship("Refeicao",
                             secondary="refeicoes_alimentos",
                             back_populates="alimentos")