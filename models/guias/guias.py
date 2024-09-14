from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base
class CapaGuia(Base):
    __tablename__ = "capa_guias"

    id_guias = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    foto_url = Column(String)
    id_usuario = Column(Integer, ForeignKey("usuario.id"))

    user = relationship("Usuario")

class Guia(Base):
    __tablename__ = "guias"
    id=Column(Integer, primary_key=True, index=True)
    id_guia = Column(Integer)
    id_usuario = Column(Integer)
    foto_guia = Column(String)
    titulo_guia = Column(String)
    texto_guia = Column(String)