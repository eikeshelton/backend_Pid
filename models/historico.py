from sqlalchemy import Column, String,INTEGER,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.usuario import Base


class HistoricoPesquisa(Base):
    __tablename__ = 'historico_pesquisa'

    id = Column(INTEGER, primary_key=True, index=True)
    usuario_id = Column(INTEGER, ForeignKey('usuario.id'))  # Verifique se o nome da tabela está correto
    texto_pesquisa = Column(String, index=True)
    data_pesquisa = Column(DateTime, default=datetime.now)

    # Relacionamento com a tabela de usuários
    usuario = relationship("Usuario", back_populates="pesquisas")