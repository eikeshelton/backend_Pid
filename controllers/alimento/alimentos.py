# controllers/alimento_controller.py
from sqlalchemy.orm import Session
from models.alimentos import Alimento
from models.schema import AlimentoResponse
from fastapi import HTTPException

def listar_alimentos(db: Session):
    alimentos = db.query(Alimento).all()
    return [AlimentoResponse.from_orm(alimento) for alimento in alimentos]

def obter_alimento(alimento_id: int, db: Session) -> AlimentoResponse:
    alimento = db.query(Alimento).filter(Alimento.id == alimento_id).first()
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")
    return AlimentoResponse.from_orm(alimento)
