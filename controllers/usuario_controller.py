# controllers/usuario_controller.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.usuario import Usuario
from dependencies import get_db


def criar_usuario(db: Session, usuario_create):
    db_usuario = Usuario(**usuario_create.dict())


    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def login_usuario(db: Session, login: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.login == login, Usuario.senha == senha).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


def atualizar_usuario(db: Session, email: str, usuario_update: Usuario):
    db_usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if db_usuario:
        # Atualizar os campos do usuário com base nos dados fornecidos
        for key, value in usuario_update.dict(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    