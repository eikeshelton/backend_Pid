# controllers/usuario_controller.py
import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.usuario.usuario import Usuario




def login_usuario(db: Session, login: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.login == login).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    

    # Verifica se a senha fornecida corresponde à armazenada
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    return usuario