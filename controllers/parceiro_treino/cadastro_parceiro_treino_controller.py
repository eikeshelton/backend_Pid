from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino
from models.estado import Estado
from models.municipio import Municipio
from fastapi import HTTPException

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

def cadastrar_preferencia_parceiro_treino(db: Session, preferencia_parceiro_treino: ParceiroTreino):
    estado_id = get_estado_id(db, preferencia_parceiro_treino.estado)
    municipio_id = get_municipio_id(db, preferencia_parceiro_treino.municipio, preferencia_parceiro_treino.estado_id)
    
    novo_parceiro_treino = ParceiroTreino(
        modalidade=preferencia_parceiro_treino.modalidade,
        dia_da_semana=preferencia_parceiro_treino.dia_da_semana,
        estado_id=estado_id,
        municipio_id=municipio_id,
        local=preferencia_parceiro_treino.local,
        agrupamento_muscular=preferencia_parceiro_treino.agrupamento_muscular,
        observacoes=preferencia_parceiro_treino.observacoes,
        horario=preferencia_parceiro_treino.horario,
        tempo_treino=preferencia_parceiro_treino.tempo_treino,
        sexo=preferencia_parceiro_treino.sexo,
        id_usuario=preferencia_parceiro_treino.id_usuario
    )
    db.add(novo_parceiro_treino)
    db.commit()
    db.refresh(novo_parceiro_treino)
    return novo_parceiro_treino