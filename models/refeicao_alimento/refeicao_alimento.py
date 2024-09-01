# models/refeicao_alimento.py
from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from models.aadeclarative_base import Base

class RefeicaoAlimento(Base):
    __tablename__ = 'refeicoes_alimentos'
    
    refeicao_id = Column(Integer, ForeignKey('refeicoes.id'), nullable=False)
    alimento_id = Column(Integer, ForeignKey('alimentos.id'), nullable=False)
    quantidade = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('refeicao_id', 'alimento_id', name='unique_refeicao_alimento'),
    )