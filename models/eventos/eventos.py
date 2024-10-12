# models.eventos.py
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
from datetime import date,time
class Eventos(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    organizador_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    nome = Column(String(250), nullable=False)
    descricao = Column (String)
    data_inicio = Column(date,nullable=False)
    hora_inicio = Column(time,nullable=False)
    localizacao =Column (String)
    participantes = relationship("Participantes", back_populates="evento")
    organizador = relationship("Usuario") 