from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
from models.usuario import Usuario

class ParceiroTreino(Base):
    __tablename__ = "parceiro_treino"

    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String(100), nullable=False)
    dia_da_semana = Column(String(50))
    estado_id = Column(Integer, ForeignKey("estado.id"), nullable=False)
    cidade_id = Column(Integer, ForeignKey("municipio.id"), nullable=False)
    local = Column(String(250))
    agrupamento_muscular = Column(Text)
    observacoes = Column(String(250))
    horario = Column(Time)
    tempo_treino = Column(Integer)
    sexo = Column(String(50))
    datetime_registro = Column(DateTime, default=datetime.UTC)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", foreign_keys=[id_usuario])
    estado = relationship("Estado")
    cidade = relationship("Municipio")
