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
    __tablename__ = "guia"
    
    id = Column(Integer, primary_key=True, index=True)
    id_capa_guia = Column(Integer, ForeignKey("capa_guias.id_guias"))  # Relacionamento correto
    id_usuario = Column(Integer)
    foto_guia = Column(String)
    titulo_guia = Column(String)
    texto_guia = Column(String)

    capa_guia = relationship("CapaGuia")