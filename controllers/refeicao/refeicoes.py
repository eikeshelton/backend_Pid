# controllers/refeicao_controller.py
from sqlalchemy.orm import Session
from models.refeicao import Refeicao
from models.schemas import RefeicaoCreate, RefeicaoResponse
from fastapi import HTTPException

def criar_refeicao(refeicao_create: RefeicaoCreate, db: Session) -> RefeicaoResponse:
    refeicao_db = Refeicao(**refeicao_create.dict())
    db.add(refeicao_db)
    db.commit()
    db.refresh(refeicao_db)
    return RefeicaoResponse.from_orm(refeicao_db)

def adicionar_alimentos(refeicao_id: int, alimentos_ids: list[int], db: Session):
    refeicao = db.query(Refeicao).filter(Refeicao.id == refeicao_id).first()
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")

    for alimento_id in alimentos_ids:
        alimento = db.query(Alimento).filter(Alimento.id == alimento_id).first()
        if alimento:
            refeicao.alimentos.append(alimento)
    
    db.commit()
    db.refresh(refeicao)
    return RefeicaoResponse.from_orm(refeicao)

def listar_refeicoes(db: Session):
    refeicoes = db.query(Refeicao).all()
    return [RefeicaoResponse.from_orm(refeicao) for refeicao in refeicoes]
