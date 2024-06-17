from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino
from models.estado import Estado
from models.municipio import Municipio
from fastapi import HTTPException
from datetime import datetime, timedelta

def get_estado_id(db: Session, id_estado: int):
    estado = db.query(Estado).filter(Estado.codigo_ibge == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail=f"Estado {id_estado} não encontrado")
    return estado.id

def get_municipio_id(db: Session, id_cidade: int, estado_id: int):
    municipio = db.query(Municipio).filter(Municipio.codigo_ibge == id_cidade, Municipio.estado_id == estado_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail=f"Município {id_cidade} não encontrado no estado {estado_id}")
    return municipio.id

def buscar_parceiros_treino(db: Session, filtros: ParceiroTreino):
    estado_id = get_estado_id(db, filtros.estado)
    municipio_id = get_municipio_id(db, filtros.municipio, filtros.estado_id)
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