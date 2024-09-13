# models/refeicao.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Refeicao(Base):
    __tablename__ = "refeicoes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(Text)
