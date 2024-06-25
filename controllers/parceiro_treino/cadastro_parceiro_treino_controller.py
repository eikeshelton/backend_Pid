from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino
from models.estado import Estado
from models.municipio import Municipio
from fastapi import HTTPException

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

def cadastrar_preferencia_parceiro_treino(db: Session, preferencia_parceiro_treino: ParceiroTreino):
    estado_id = get_estado_id(db, preferencia_parceiro_treino.estado_codigo_ibge)
    municipio_id = get_municipio_id(db, preferencia_parceiro_treino.municipio_codigo_ibge, preferencia_parceiro_treino.estado_codigo_ibge)
    try:
        novo_parceiro_treino = ParceiroTreino(
            modalidade=preferencia_parceiro_treino.modalidade,
            estado_codigo_ibge=estado_id,
            municipio_codigo_ibge=municipio_id,
            id_usuario=preferencia_parceiro_treino.id_usuario,
            dia_da_semana=preferencia_parceiro_treino.dia_da_semana if preferencia_parceiro_treino.dia_da_semana else None,
            local=preferencia_parceiro_treino.local if preferencia_parceiro_treino.local else '',
            agrupamento_muscular=preferencia_parceiro_treino.agrupamento_muscular if preferencia_parceiro_treino.agrupamento_muscular else None,
            observacoes=preferencia_parceiro_treino.observacoes if preferencia_parceiro_treino.observacoes else None,
            horario=preferencia_parceiro_treino.horario if preferencia_parceiro_treino.horario else None,
            tempo_treino=preferencia_parceiro_treino.tempo_treino if preferencia_parceiro_treino.tempo_treino else None
            
        )
        db.add(novo_parceiro_treino)
        db.commit()
        db.refresh(novo_parceiro_treino)
        return novo_parceiro_treino
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadatrar sua preferencias: {str(e)}")
