# controllers/alimento_controller.py
from sqlalchemy.orm import Session
from models.alimentos.alimentos import Alimento
from models.schema.schema import AlimentoResponse
from fastapi import HTTPException

def obter_alimento(descricao: str, db: Session) -> AlimentoResponse:
    alimentos = db.query(Alimento).filter(Alimento.descricao.ilike(f'{descricao.lower()}%')).order_by(Alimento.descricao).all()
    if not alimentos:
        raise HTTPException(status_code=404, detail="Alimento não encontrado")  
    return alimentos
