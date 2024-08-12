from models.estado.estado import Estado
from sqlalchemy.orm import Session
from fastapi import HTTPException

def get_estado_id(db: Session, id_estado: int):
    estado = db.query(Estado).filter(Estado.codigo_ibge == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail=f"Estado {id_estado} não encontrado")
    return estado.codigo_ibge