# models/refeicao_alimento.py
from sqlalchemy import Column, Integer, ForeignKey,Date
from models.aadeclarative_base import Base

class RefeicaoAlimento(Base):
    __tablename__ = 'refeicoes_alimentos'
    id = Column(Integer, primary_key=True, index=True)
    id_refeicao = Column(Integer, ForeignKey('refeicoes.id'), nullable=False)
    id_alimento = Column(Integer, ForeignKey('alimento_usuario.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    data= Column(Date,nullable=False)
    