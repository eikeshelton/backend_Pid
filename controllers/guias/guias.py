from models.guias.guias import *
from sqlalchemy.orm import Session

def cadastrar_guia(guia,db:Session):
    db_guia = CapaGuia(**guia.dict())
    db.add(db_guia)
    db.commit()
    db.refresh(db_guia)
    return db_guia
def buscar_capas_guias(id_usuario:int,db:Session):
    db_capa_guia= db.query(CapaGuia).filter(CapaGuia.id_usuario == id_usuario).all()
    return db_capa_guia

def busca_guia_id (id_guia:int,db:Session):
    db_guia = db.query(Guia).filter(Guia.id_guia==id_guia).all()
    return db_guia