from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino

def buscar_parceiros_treino(db: Session, filtros: ParceiroTreino):
    query = db.query(ParceiroTreino)
    
    query = query.filter(ParceiroTreino.modalidade == filtros.modalidade)
    query = query.filter(ParceiroTreino.dia_da_semana == filtros.dia_da_semana)
    query = query.filter(ParceiroTreino.estado == filtros.estado)
    query = query.filter(ParceiroTreino.cidade == filtros.cidade)
    query = query.filter(ParceiroTreino.local == filtros.local)
    query = query.filter(ParceiroTreino.horario == filtros.horario)
    
    if filtros.agrupamento_muscular:
        query = query.filter(ParceiroTreino.agrupamento_muscular == filtros.agrupamento_muscular)
    if filtros.observacoes:
        query = query.filter(ParceiroTreino.observacoes == filtros.observacoes)
    if filtros.tempo_treino:
        query = query.filter(ParceiroTreino.tempo_treino == filtros.tempo_treino)
    if filtros.sexo:
        query = query.filter(ParceiroTreino.sexo == filtros.sexo)
    
    parceiros = query.all()
    return parceiros