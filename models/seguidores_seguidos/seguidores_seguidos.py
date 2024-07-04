from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from models.aadeclarative_base import Base


class SeguidoresSeguidos(Base):
    __tablename__ = 'seguidores_seguidos'
    id = Column(Integer, primary_key=True, index=True)
    id_seguidor = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_seguido = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    __table_args__ = (UniqueConstraint('id_seguidor', 'id_seguido', name='unique_seguir'),)
    
    