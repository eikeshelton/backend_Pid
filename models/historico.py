# models/historico.py
from sqlalchemy import Column, INTEGER, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class HistoricoPesquisa(Base):
    __tablename__ = 'historico_pesquisa'

    id = Column(INTEGER, primary_key=True, index=True)
    usuario_id = Column(INTEGER, ForeignKey("usuario.id"))
    pesquisado_id = Column(INTEGER, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="pesquisas")
    pesquisado = relationship("Usuario", foreign_keys=[pesquisado_id], back_populates="pesquisas_pesquisado")
