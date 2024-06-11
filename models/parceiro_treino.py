from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
from models.usuario import Usuario

class ParceiroTreino(Base):
    __tablename__ = "parceiro_treino"

    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String(100), nullable=False)
    dia_da_semana = Column(String(50))
    estado = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    local = Column(String(250))
    agrupamento_muscular = Column(Text)
    observacoes = Column(String(250))
    tempo_treino = Column(Integer)
    sexo = Column(String(50))
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="parceiros_treino")
