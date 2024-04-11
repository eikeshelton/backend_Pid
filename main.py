# app.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from controllers.usuario_controller import criar_usuario, login_usuario,atualizar_usuario
from dependencies import get_db
from pydantic import BaseModel
from datetime import date
from typing import Optional

app = FastAPI()

# Modelo Pydantic para entrada de dados de cadastro de usuário
class UsuarioCreate(BaseModel):
    email: str
    nome_usuario: str
    login: str
    senha: str
    tipo_usuario: str
    data_nascimento: date
    foto_perfil: bytes
    bio: str
class Login(BaseModel):
    login: str
    senha: str

class UsuarioUpdate(BaseModel):
    nome_usuario: Optional[str] = None
    foto_perfil: Optional[bytes] = None
    bio: Optional[str] = None
    tipo_usuario: Optional[str] = None
# Rota para criar um novo usuário
@app.post("/usuarios/")
def criar_novo_usuario(usuario_create: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, usuario_create)

# Rota para login de usuário
@app.post("/login/")
def fazer_login(login_data: Login, db: Session = Depends(get_db)):
    usuario = login_usuario(db, login_data.login, login_data.senha)
    return login_usuario(db, login_data.login, login_data.senha)

@app.put("/usuarios/{email}")
def atualizar_dados_usuario(email: str, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    return atualizar_usuario(db, email, usuario_update)