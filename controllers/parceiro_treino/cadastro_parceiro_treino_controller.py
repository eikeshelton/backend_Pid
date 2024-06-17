from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino, Estado, Municipio
from fastapi import HTTPException

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

def cadastrar_preferencia_parceiro_treino(db: Session, preferencia_parceiro_treino: ParceiroTreino):
    estado_id = get_estado_id(db, preferencia_parceiro_treino.estado)
    municipio_id = get_municipio_id(db, preferencia_parceiro_treino.cidade, estado_id)
    
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