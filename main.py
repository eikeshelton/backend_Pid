# main.py
from typing import List
from fastapi import FastAPI, Depends,HTTPException,WebSocket,WebSocketDisconnect
from sqlalchemy.orm import Session
from controllers.usuario.usuario_controller import criar_usuario,upload_login,verificar_credenciais,login_usuario,atualizar_usuario,obter_dados_usuario, buscar_usuarios_por_nome,buscar_pesquisado,registrar_pesquisado, adicionar_token_reset_senha, obter_token_reset_senha, alterar_senha, limpar_token_reset_senha
from controllers.chat.chat_controller import cadastrar_mensagem,recuperar_conversas_usuario,recuperar_nova_mensagem
from controllers.parceiro_treino.cadastro_parceiro_treino_controller import cadastrar_preferencia_parceiro_treino
from controllers.parceiro_treino.busca_parceiro_treino_controller import buscar_parceiros_treino
from dependencies import get_db
from pydantic import BaseModel
from datetime import  time, datetime
from typing import Optional,Dict
from models.schema.schema import UsuarioCreate,MensagemRecebida,Login,LoginUpdate,Mensagem,UsuarioUpdate,Credenciais,UserResetPassword,UserSearch,RegistrarBusca
from typing import Dict
import json
from starlette.websockets import WebSocketState
app = FastAPI()

connections = {}
# Modelo Pydantic para entrada de dados de cadastro de usuário


class ParceiroTreino(BaseModel):
    modalidade: str
    dia_da_semana: str
    estado_codigo_ibge: int
    municipio_codigo_ibge: int
    local: Optional[str] = None
    agrupamento_muscular: Optional[str] = None
    observacoes: Optional[str] = None
    horario: time
    tempo_treino: Optional[time] = None
    sexo: Optional[str] = None
    datetime_registro: Optional[datetime] = None
    id_usuario: int

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

# Rota para buscar usuários por nome de acordo com o que o usuario digita
@app.post("/usuarios/buscar/")
def buscar_usuarios(usersearch:UserSearch,db: Session = Depends(get_db)):
    usuarios = buscar_usuarios_por_nome(db, usersearch.login)
    return usuarios

# Rota para registrar algum outro perfil que foi pesquisado pelo usuário
@app.post("/usuarios/registra-buscar/")
def buscar_usuarios(registrar_busca:RegistrarBusca,db: Session = Depends(get_db)):
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
        if user_id not in connections:
            connections[user_id] = {}
        connections[user_id][user_id] = websocket
        
        while True:
            data = await websocket.receive_text()
            mensagem_data = json.loads(data)
            mensagem = MensagemRecebida(**mensagem_data)
            destinatario_id = mensagem.destinatario_id
            
            cadastrar_mensagem(mensagem, db)
            
            ultima_mensagem = recuperar_nova_mensagem(db, mensagem.remetente_id, destinatario_id)
            
            if ultima_mensagem:
                ultima_mensagem_json = json.dumps({
                    "id": ultima_mensagem.id,
                    "remetente_id": ultima_mensagem.remetente_id,
                    "destinatario_id": ultima_mensagem.destinatario_id,
                    "texto": ultima_mensagem.texto
                })
                
                # Enviar a última mensagem ao destinatário se ele estiver conectado
                if destinatario_id in connections and user_id in connections[destinatario_id]:
                    destinatario_websocket = connections[destinatario_id][user_id]
                    await destinatario_websocket.send_text(ultima_mensagem_json)
                
                # Enviar a última mensagem ao remetente
                if user_id in connections and destinatario_id in connections[user_id]:
                    remetente_websocket = connections[user_id][destinatario_id]
                    await remetente_websocket.send_text(ultima_mensagem_json)
                elif user_id in connections:
                    remetente_websocket = connections[user_id][user_id]
                    await remetente_websocket.send_text(ultima_mensagem_json)
    
    except WebSocketDisconnect:
        print(f"WebSocket desconectado para o usuário {user_id}")
    except Exception as e:
        print("Erro durante a comunicação WebSocket:", e)
    finally:
        # Remover a conexão do usuário ao encerrar
        if websocket.application_state == WebSocketState.CONNECTED:
            del connections[user_id]
            await websocket.close()

#Endpoint do cadastro de preferências do Parceiro de Treino
@app.post("/parceiros_treino/cadastro")
def cadastra_preferencia_parceiro_treino(parceiro_treino: ParceiroTreino, db: Session = Depends(get_db)):
    return cadastrar_preferencia_parceiro_treino(db, parceiro_treino)

#Endpoint da busca pelo Parceiro de Treino, com os filtros definidos.
@app.post("/parceiros_treino/busca")
def buscar_parceiros_treino_endpoint(filtros: ParceiroTreino, db: Session = Depends(get_db)):
    parceiros = buscar_parceiros_treino(db, filtros)
    
    if not parceiros:
        raise HTTPException(status_code=404, detail="Nenhum parceiro de treino encontrado com os filtros fornecidos")
    
    return parceiros