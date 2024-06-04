# main.py
from typing import List
from fastapi import FastAPI, Depends,HTTPException,WebSocket
from sqlalchemy.orm import Session
from controllers.usuario_controller import criar_usuario, deletar_foto_perfil,upload_login,verificar_credenciais,login_usuario,atualizar_usuario,obter_dados_usuario, buscar_usuarios_por_nome, registrar_pesquisa,buscar_pesquisado,registrar_pesquisado
from controllers.chat_controller import cadastrar_mensagem,recuperar_conversas_usuario,recuperar_nova_mensagem
from dependencies import get_db
from pydantic import BaseModel
from datetime import date
from typing import Optional,Dict
import json
from starlette.websockets import WebSocketState
app = FastAPI()

connections: Dict[int, WebSocket] = {}
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
class UserSearch(BaseModel):
    login:str
class Registrar_Busca(BaseModel):
    usuario_id:int
    pesquisado_id:int 
    
class MensagemRecebida(BaseModel):
    remetente_id:int
    destinatario_id:int
    texto:str
class Mensagem(BaseModel):
    id:int
    remetente_id:int
    destinatario_id:int
    texto:str

@app.post("/usuarios/")
def criar_novo_usuario(usuario_create: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, usuario_create)

# Rota para login de usuário
@app.post("/login/")
def fazer_login(login_data: Login, db: Session = Depends(get_db)):
    return login_usuario(db, login_data.login, login_data.senha)
@app.delete("/usuario/foto/delete/{usuario_id}")
def usuario_foto_delete(usuario_id: int,db: Session = Depends(get_db)):
    deletar_foto_perfil(db,usuario_id)

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

# Rota para buscar usuários por parte do nome e ordenar alfabeticamente
@app.post("/usuarios/buscar/")
def buscar_usuarios(usersearch:UserSearch,db: Session = Depends(get_db)):
    usuarios = buscar_usuarios_por_nome(db, usersearch.login)
    return usuarios

@app.post("/usuarios/registra-buscar/")
def buscar_usuarios(registrar_busca:Registrar_Busca,db: Session = Depends(get_db)):
    registrar_pesquisado(db, registrar_busca)
    usuarios = buscar_pesquisado(db, registrar_busca.usuario_id)
    if usuarios is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuarios 
@app.get("/usuarios-pesquisados/{usuario_id}")
def pesquisados(usuario_id,db: Session = Depends(get_db)):
    usuarios = buscar_pesquisado(db, usuario_id)
    if usuarios is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuarios
   

@app.get("/chat/mensagens/{remetente_id}/{destinatario_id}")
async def recuperar_mensagens(remetente_id: int, destinatario_id: int,db: Session = Depends(get_db)) -> List[Mensagem]:
    conversas = recuperar_conversas_usuario(db,remetente_id,destinatario_id)

    return conversas


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()

    try:
        # Registrar a conexão do usuário
        connections[user_id] = websocket

        while True:
            data = await websocket.receive_text()
            print("Dados recebidos:", data)  # Verificar os dados recebidos do cliente
            mensagem_data = json.loads(data)
            print("Mensagem recebida:", mensagem_data)  # Verificar a mensagem recebida do cliente
            mensagem = MensagemRecebida(**mensagem_data)
            cadastrar_mensagem(mensagem, db)
            
            # Recuperar a última mensagem cadastrada no banco de dados
            ultima_mensagem = recuperar_nova_mensagem(db, mensagem.remetente_id, mensagem.destinatario_id)
            
            if ultima_mensagem:
                # Converter a última mensagem para JSON, incluindo apenas os campos desejados
                ultima_mensagem_json = json.dumps({
                    "id": ultima_mensagem.id,
                    "remetente_id": ultima_mensagem.remetente_id,
                    "destinatario_id": ultima_mensagem.destinatario_id,
                    "texto": ultima_mensagem.texto
                })
                
                # Obter o WebSocket do destinatário
                destinatario_websocket = connections.get(mensagem.destinatario_id)
                remetente_websocket = connections.get(mensagem.remetente_id)
                # Enviar a última mensagem para o destinatário, se conectado
                if destinatario_websocket:
                    await destinatario_websocket.send_text(ultima_mensagem_json)
                
                # Enviar a última mensagem para o remetente, se conectado
                if remetente_websocket:
                    await remetente_websocket.send_text(ultima_mensagem_json)

    except HTTPException as e:
        print("Erro HTTP:", e)
    except Exception as e:
        print("Erro durante a comunicação WebSocket:", e)
    finally:
        # Remover a conexão do usuário ao encerrar
        if websocket.application_state == WebSocketState.CONNECTED:
            del connections[user_id]
            await websocket.close()
