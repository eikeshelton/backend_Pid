# controllers/alimento_controller.py
from sqlalchemy.orm import Session
from models.alimentos import Alimento
from models.schema import AlimentoResponse
from fastapi import HTTPException

def listar_alimentos(db: Session):
    alimentos = db.query(Alimento).all()
    return alimentos

def obter_alimento(descricao: int, db: Session) -> AlimentoResponse:
    alimento = db.query(Alimento).filter(Alimento.descricao == descricao).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return alimento
