from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino, Estado, Municipio
from fastapi import HTTPException
from datetime import datetime, timedelta

def get_estado_id(db: Session, nome_estado: str):
    estado = db.query(Estado).filter(Estado.nome == nome_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail=f"Estado {nome_estado} não encontrado")
    return estado.id

def get_municipio_id(db: Session, nome_cidade: str, estado_id: int):
    municipio = db.query(Municipio).filter(Municipio.nome == nome_cidade, Municipio.estado_id == estado_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail=f"Município {nome_cidade} não encontrado no estado {estado_id}")
    return municipio.id

def buscar_parceiros_treino(db: Session, filtros: ParceiroTreino):
    estado_id = get_estado_id(db, filtros.estado)
    municipio_id = get_municipio_id(db, filtros.cidade, estado_id)
    data_limite = datetime.UTC() - timedelta(days=7)
    
    query = db.query(ParceiroTreino).filter(
        ParceiroTreino.modalidade == filtros.modalidade,
        ParceiroTreino.dia_da_semana == filtros.dia_da_semana,
        ParceiroTreino.estado_id == estado_id,
        ParceiroTreino.municipio_id == municipio_id,
        ParceiroTreino.local == filtros.local,
        ParceiroTreino.horario == filtros.horario,
        ParceiroTreino.datetime_registro >= data_limite
    )
    
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