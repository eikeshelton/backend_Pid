# main.py
from typing import List
from fastapi import FastAPI, Depends,HTTPException,WebSocket
from sqlalchemy.orm import Session
from controllers.usuario.atualizar_usuario.atualizar_usuario import atualizar_usuario,obter_dados_usuario,upload_login
from controllers.usuario.buscar_usuarios.Buscar_usuarios import buscar_usuarios_por_nome
from controllers.usuario.logar_usuario.Logar_usuario import login_usuario
from controllers.usuario.registrar_usuario.Registrar_usuario import criar_usuario
from controllers.usuario.verificar_senhas.Verificar_senhas import adicionar_token_reset_senha,alterar_senha,limpar_token_reset_senha,obter_token_reset_senha,verificar_credenciais
from controllers.historico.historico import registrar_pesquisado,buscar_pesquisado
from controllers.chat.chat_controller import cadastrar_mensagem,recuperar_conversas_usuario,recuperar_nova_mensagem,conversas_chat
from controllers.parceiro_treino.cadastro_parceiro_treino_controller import cadastrar_preferencia_parceiro_treino
from controllers.parceiro_treino.busca_parceiro_treino_controller import buscar_parceiros_treino
from controllers.seguidores_seguidos.seguidores_seguidos import registrar_seguidores,lista_usuarios_seguidos,lista_usuarios_seguidores,contar_seguidores_e_seguidos,buscar_seguidores_seguidos,verifica_seguidor,cancelar_seguir,atualizar_fcmToken,acao_seguir,solicitacoes
from dependencies import get_db
from typing import Dict
from models.schema.schema import UsuarioCreate,SeguidoresCreate,MensagemRecebida,ParceiroTreino,Login,LoginUpdate,Mensagem,UsuarioUpdate,Credenciais,UserResetPassword,UserSearch,RegistrarBusca,FCMTokenUpdate,Conversas,SeguidoresAcao
from typing import Dict
import json
from starlette.websockets import WebSocketState

app = FastAPI()

connections: Dict[int, WebSocket] = {}
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

@app.websocket("/ws/{user_id}/{user_id2}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, user_id2: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        # Registrar a conexão do usuário
        connections[(user_id, user_id2)] = websocket
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
                    "texto": ultima_mensagem.texto,
                    "id_conversa":ultima_mensagem.id_conversa
                })
                
                # Obter o WebSocket do destinatário
                destinatario_websocket = connections.get((mensagem.destinatario_id, mensagem.remetente_id))
                remetente_websocket = connections.get((mensagem.remetente_id, mensagem.destinatario_id))
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
        if websocket.application_state == WebSocketState.CONNECTED:
            try:
                await websocket.close()
            except Exception as e:
                print("Erro ao fechar WebSocket:", e)
            finally:
                del connections[(user_id, user_id2)]
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
# registra quando um usuario segue outro
@app.post("/seguidores/")
def registrar_seguidor(seguidores: SeguidoresCreate, db: Session = Depends(get_db)):
   seguir = registrar_seguidores(seguidores,db)
   return seguir
# verifica quais usuarios o usuario segue
@app.get("/usuarios_seguidos/{id_usuario}")
async def usuarios_seguidos(id_usuario: int, db: Session = Depends(get_db)) -> List[dict]:
        usuarios = lista_usuarios_seguidos(id_usuario,db)
        return usuarios
# verifica quais usuarios seguem o usuario
@app.get("/usuarios_seguidores/{id_usuario}")
async def usuarios_seguidos(id_usuario: int, db: Session = Depends(get_db)) -> List[dict]:
        usuarios = lista_usuarios_seguidores(id_usuario,db)
        return usuarios
#verifica se um usuario segue outro
@app.get("/verificar_seguimento/{id_usuario}/{id_usuario2}")
async def verificar_seguimento(id_usuario: int,id_usuario2:int, db: Session = Depends(get_db)):
        verificacao = verifica_seguidor(id_usuario,id_usuario2,db)
        return verificacao
# cancela o seguir de um usuario
@app.delete("/seguidores/")
def cancelar_seguidor(seguidores: SeguidoresCreate, db: Session = Depends(get_db)) :
     cancelar= cancelar_seguir(seguidores, db)
     return cancelar

# busca a quantidade de seguidores e seguidos do usuario
@app.get("/seguidores_seguidos/{id_usuario}")
def seguidores_seguidos(id_usuario:int,db:Session=Depends(get_db)):
    usuario=buscar_seguidores_seguidos(id_usuario,db)
    return usuario

# receber token do celular para notificaçao
@app.post("/atualizar-fcm-token/")
def fcm_token(fcm_token_update:FCMTokenUpdate, db: Session = Depends(get_db)):
   atualizar_fcmToken(fcm_token_update,db)
#lista de todas as conversas do usuario
@app.get("/conversas_usuario/{id_usuario}")
def conversas_usuario(id_usuario:int,db:Session=Depends(get_db)):
    conversas_usuario=conversas_chat(id_usuario,db)
    return conversas_usuario

#lista de todas as solicitaçoes pendentes do usuario
@app.get("/lista_solicitacoes_pendentes/{id_usuario}")
def lista_solicitacoes(id_usuario,db:Session=Depends(get_db)):
    lista = solicitacoes(id_usuario,db)
    return lista

@app.post("/seguidores/acao/")
def seguimento(seguidores: SeguidoresAcao, db: Session = Depends(get_db)):
    relacao= acao_seguir(seguidores,db)
    return relacao