# models.eventos.py
from sqlalchemy import Column, Integer, String,ForeignKey,Date,Time
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
class Eventos(Base):
    __tablename__ = "eventos"
    
    id = Column(Integer, primary_key=True, index=True)
    organizador_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    nome = Column(String(250), nullable=False)
    descricao = Column(String)
    data_inicio = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    localizacao = Column(String)
    municipio_id = Column(Integer, ForeignKey('municipio.codigo_ibge'), nullable=False)
    quantidade_participantes = Column(Integer, default=0)
    # Referência como string para evitar problemas de inicialização 
    organizador = relationship("Usuario")