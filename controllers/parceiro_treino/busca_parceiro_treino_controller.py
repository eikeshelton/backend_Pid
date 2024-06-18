from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino
from models.estado import Estado
from models.municipio import Municipio
from models.usuario import Usuario
from fastapi import HTTPException
from datetime import datetime, timedelta,timezone

def get_estado_id(db: Session, id_estado: int):
    estado = db.query(Estado).filter(Estado.codigo_ibge == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail=f"Estado {id_estado} não encontrado")
    return estado.codigo_ibge

def get_municipio_id(db: Session, id_cidade: int, estado_id: int):
    municipio = db.query(Municipio).filter(Municipio.codigo_ibge == id_cidade, Municipio.estado_id == estado_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail=f"Município {id_cidade} não encontrado no estado {estado_id}")
    return municipio.codigo_ibge

def buscar_parceiros_treino(db: Session, filtros: ParceiroTreino):
    estado_id = get_estado_id(db, filtros.estado_codigo_ibge)
    municipio_id = get_municipio_id(db, filtros.municipio_codigo_ibge, filtros.estado_codigo_ibge)
    data_limite = datetime.now(timezone.utc) - timedelta(days=7)
    
    query = db.query(ParceiroTreino).filter(
        ParceiroTreino.modalidade == filtros.modalidade,
        ParceiroTreino.estado_codigo_ibge == estado_id,
        ParceiroTreino.municipio_codigo_ibge == municipio_id,
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
    if filtros.dia_da_semana:
        query = query.filter(ParceiroTreino.dia_da_semana == filtros.dia_da_semana)
    if filtros.local:
        query = query.filter(ParceiroTreino.local == filtros.local)
    if filtros.horario:
        query = query.filter(ParceiroTreino.horario == filtros.horario)
    if filtros.sexo:
        query = query.filter(Usuario.sexo == filtros.sexo)
    
    parceiros = query.all()
    return parceiros