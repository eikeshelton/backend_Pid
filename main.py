# app.py

from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session
from controllers.usuario_controller import criar_usuario,upload_login,verificar_credenciais, login_usuario,atualizar_usuario,obter_dados_usuario, adicionar_token_reset_senha, obter_token_reset_senha, alterar_senha, limpar_token_reset_senha
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
class UsuarioSelect(BaseModel):
    nome_usuario: str
    tipo_usuario: str
    foto_perfil: bytes
    bio: str
    seguidores:int
    seguidos:int
class LoginUpdate(BaseModel):
    login: str
    senha: str
    email: str
    id:int
class Credenciais(BaseModel):
    email: str
    senha: str
class UserResetPassword(BaseModel):
    email: str
    token: Optional[str]=None
    new_password:Optional[str]=None
@app.post("/usuarios/")
def criar_novo_usuario(usuario_create: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, usuario_create)

# Rota para login de usuário
@app.post("/login/")
def fazer_login(login_data: Login, db: Session = Depends(get_db)):
    return login_usuario(db, login_data.login, login_data.senha)



# Rota para atualizar as informações do perfil
@app.put("/usuarios/{email}")
def atualizar_dados_usuario(email: str, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    return atualizar_usuario(db, email, usuario_update)



# Rota para atualizar o usuario
@app.get("/usuarios/{email}")
def obter_dados_usuario_view(email: str, db: Session = Depends(get_db)):

    usuario = obter_dados_usuario(email, db)
    return usuario


@app.post("/check-credentials/")
def verificar_credenciais_endpoint(credenciais: Credenciais, db: Session = Depends(get_db)):
    
    # Chama a função verificar_credenciais para obter o ID do usuário
    usuario = verificar_credenciais(db, credenciais.email, credenciais.senha)
        
    # Retorna o ID do usuário
    return usuario
    
@app.put("/Uploadlogin/")
def upload_login_endpoint(LoginUpdate: LoginUpdate, db: Session = Depends(get_db)):
    # Chama a função verificar_email_senha do controlador
    usuario = upload_login(db, LoginUpdate.login, LoginUpdate.senha, LoginUpdate.email, LoginUpdate.id)
    
    # Retorna uma resposta indicando se as credenciais são válidas
    if not usuario:
        raise HTTPException(status_code=401, detail="não cadastrado")

    return usuario

# Rota para solicitar redefinição de senha
@app.post("/usuarios/request-password-reset/")
def request_password_reset(UserResetPassword: UserResetPassword, db: Session = Depends(get_db)):
    token = adicionar_token_reset_senha(db, UserResetPassword.email)
    if token:
        return {"message": "Token de redefinição de senha enviado por email."}
    else:
        raise HTTPException(status_code=404, detail="Email não encontrado")

# Rota para redefinir senha
@app.post("/usuarios/reset-password/")
def reset_password(UserResetPassword:UserResetPassword, db: Session = Depends(get_db)):
    token_db = obter_token_reset_senha(db, UserResetPassword.email)
    if token_db == UserResetPassword.token:
        # Aqui você precisa definir a nova senha para o usuário
        alterar_senha(db, UserResetPassword.email, UserResetPassword.new_password)
        # e limpar o token de redefinição de senha
        limpar_token_reset_senha(db, UserResetPassword.email)
        return {"message": "Senha redefinida com sucesso."}
    else:
        raise HTTPException(status_code=400, detail="Token inválido")