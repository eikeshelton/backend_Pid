from models.guias.guias import Guia
from sqlalchemy.orm import Session

def cadastrar_guia(guia,db:Session):
    db_guia = Guia(**guia.dict())
    db.add(db_guia)
    db.commit()
    db.refresh(db_guia)
    return db_guia
def buscar_guias(id_usuario:int,db:Session):
    db_guia= db.query(Guia).filter(Guia.id_usuario == id_usuario).all()
    return db_guia