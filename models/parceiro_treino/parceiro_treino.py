# models.parceiro_treino.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
from ..usuario.usuario import Usuario 
class ParceiroTreino(Base):
    __tablename__ = "parceiro_treino"

    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String(100), nullable=False)
    dia_da_semana = Column(String(50))
    estado_codigo_ibge = Column(Integer, ForeignKey("estado.codigo_ibge"), nullable=False)
    municipio_codigo_ibge = Column(Integer, ForeignKey("municipio.codigo_ibge"), nullable=False)
    local = Column(String(250))
    agrupamento_muscular = Column(Text)
    observacoes = Column(String(250))
    horario = Column(Time)
    tempo_treino = Column(Time)
    datetime_registro = Column(DateTime, default=datetime.now(timezone.utc))
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario")
    estado_relacionamento = relationship("Estado", back_populates="parceiros_treino")
    municipio_relacionamento = relationship("Municipio", back_populates="parceiros_treino")
