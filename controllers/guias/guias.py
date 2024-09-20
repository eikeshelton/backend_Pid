from models.guias.capa_guias import *
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.usuario.usuario import Usuario
from models.schema.schema import GuiaCreate

def cadastrar_guia(guia: GuiaCreate, db: Session):
    # Criando CapaGuia apenas com campos relevantes
    db_capa_guia = CapaGuia(
        titulo=guia.titulo,
        foto_url=guia.foto_url,
        id_usuario=guia.id_usuario
    )
    db.add(db_capa_guia)
    db.commit()
    db.refresh(db_capa_guia)
    
    # Inserindo dados no modelo Guia
    cadastrar_guia_teste(db_capa_guia.id_guias, guia, db)
    return db_capa_guia

def cadastrar_guia_teste(id_capa_guia: int, guia: GuiaCreate, db: Session):
    db_guia = Guia(
        id_capa_guia=id_capa_guia,
        id_usuario=guia.id_usuario,
        foto_guia=guia.foto_guia,
        titulo_guia=guia.titulo_guia,
        texto_guia=guia.texto_guia
    )
    db.add(db_guia)
    db.commit()
    db.refresh(db_guia)
    return db_guia

def buscar_capas_guias(id_usuario:int,db:Session):
    db_capa_guia= db.query(CapaGuia).filter(CapaGuia.id_usuario == id_usuario).all()
    return db_capa_guia

def busca_guia_id (id_guia:int,db:Session):
    db_guia = db.query(Guia).filter(Guia.id_guia==id_guia).first()
    return db_guia


def contar_capas_guias(id_usuario: int, db: Session) -> int:
    # Faz a contagem de quantas vezes o id_usuario aparece na tabela capa_guias
    count = db.query(func.count(CapaGuia.id_usuario)).filter(CapaGuia.id_usuario == id_usuario).scalar()
    
    # Atualiza a coluna 'publicacoes' na tabela usuario com o valor da contagem
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if usuario:
        usuario.publicacoes = count
        db.commit()  # Confirma a alteração no banco de dados

    return count