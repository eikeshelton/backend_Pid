from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino

def cadastrar_preferencia_parceiro_treino(db: Session, preferencia_parceiro_treino: ParceiroTreino):
    novo_parceiro_treino = ParceiroTreino(**preferencia_parceiro_treino.dict())
    db.add(novo_parceiro_treino)
    db.commit()
    db.refresh(novo_parceiro_treino)
    return novo_parceiro_treino