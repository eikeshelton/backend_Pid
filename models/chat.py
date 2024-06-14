# models/chat.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from models.aadeclarative_base import Base

class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    remetente_id = Column(Integer, ForeignKey("usuario.id"))
    destinatario_id = Column(Integer, ForeignKey("usuario.id"))
    texto = Column (String)
    data_envio = Column(DateTime, default=datetime.now(timezone.utc))
    id_conversa=Column(Integer)

    remetente = relationship("Usuario", foreign_keys=[remetente_id])
    destinatario = relationship("Usuario", foreign_keys=[destinatario_id])
    def to_dict(self):
        return {
            "id": self.id,
            "remetente_id": self.remetente_id,
            "destinatario_id": self.destinatario_id,
            "texto": self.texto,
            # Outros campos que você deseja incluir no dicionário...
        }