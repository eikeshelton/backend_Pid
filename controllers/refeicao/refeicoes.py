# controllers/refeicao_controller.py
from sqlalchemy.orm import Session
from models.refeicao.refeicao import Refeicao
from models.alimentos.alimentos import Alimento
from models.refeicao_alimento.refeicao_alimento import RefeicaoAlimento
from models.schema.schema import RefeicaoCreate, RefeicaoResponse
from fastapi import HTTPException

def criar_refeicao(refeicao_create: RefeicaoCreate, db: Session) -> RefeicaoResponse:
    refeicao_db = Refeicao(**refeicao_create.dict())
    db.add(refeicao_db)
    db.commit()
    db.refresh(refeicao_db)
    return RefeicaoResponse.from_orm(refeicao_db)

def adicionar_alimentos(refeicao_id: int, alimento_id: int, db: Session):
    refeicao = db.query(Refeicao).filter(Refeicao.id == refeicao_id).first()
    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")

    alimento = db.query(Alimento).filter(Alimento.id == alimento_id).first()
    if alimento:
        refeicao.alimentos.append(alimento)
        db.commit()
        db.refresh(refeicao)
    
    return refeicao

def listar_refeicoes(usuario_id: int, db: Session):
    refeicoesAlimentos = db.query(RefeicaoAlimento).filter(RefeicaoAlimento.usuario_id == usuario_id)

    refeicoes_ids = [refeicoesAlimentos.refeicao_id for refeicao in refeicoesAlimentos]

    refeicoes = db.query(Refeicao).filter(Refeicao.id.in_(refeicoes_ids)).all()
    
    return refeicoes

def calcular_valores_totais(db: Session, refeicao_id: int):
    refeicao = db.query(Refeicao).filter(Refeicao.id == refeicao_id).first()

    if not refeicao:
        raise HTTPException(status_code=404, detail="Refeição não encontrada")

    total_energia_kcal = 0
    total_proteina_g = 0
    total_carboidrato_g = 0

    for alimento_refeicao in refeicao.alimentos:
        quantidade_g = alimento_refeicao.quantidade_g
        alimento = alimento_refeicao.alimento

        total_energia_kcal += (alimento.energia_kcal * quantidade_g) / 100
        total_proteina_g += (alimento.proteina_g * quantidade_g) / 100
        total_carboidrato_g += (alimento.carboidrato_g * quantidade_g) / 100

    return {
        "total_energia_kcal": total_energia_kcal,
        "total_proteina_g": total_proteina_g,
        "total_carboidrato_g": total_carboidrato_g
    }
