# models.eventos.py
from sqlalchemy import Column, Integer,ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Participantes(Base):
    __tablename__ = "participantes_evento"
    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    participante_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    evento = relationship("Eventos", back_populates="participantes")
    participante = relationship("Usuario") 
    