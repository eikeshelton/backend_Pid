# controler.seguidores_seguidos
from firebase_admin import messaging
from google.auth.transport.requests import Request
from FCMManager import get_access_token
from fastapi import HTTPException
from models.seguidores_seguidos.seguidores_seguidos import SeguidoresSeguidos
from models.usuario.usuario import Usuario
from sqlalchemy import  and_,func
from sqlalchemy.orm import Session
def registrar_seguidores(seguidores, db: Session):
    relacao_existente = db.query(SeguidoresSeguidos).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == seguidores.id_seguidor,
            SeguidoresSeguidos.id_seguido == seguidores.id_seguido
        )
    ).first()
    
    if relacao_existente:
        return False
    usuario_seguido= db.query(Usuario).filter(Usuario.id== seguidores.id_seguido).first()
    # Criar nova relação com status pendente
    nova_relacao = SeguidoresSeguidos(
        id_seguidor=seguidores.id_seguidor,
        id_seguido=seguidores.id_seguido,
        status='pendente' if usuario_seguido.tipo_usuario == 'Entusiasta' else 'aceito'
    )
    db.add(nova_relacao)
    db.commit()
    db.refresh(nova_relacao)
    
    if nova_relacao.status == 'pendente':
        enviar_notificacao_seguir(seguidores.id_seguidor, seguidores.id_seguido, db, pendente=True)
    else:
        contar_seguidores_e_seguidos(seguidores.id_seguidor, seguidores.id_seguido, db)
        enviar_notificacao_seguir(seguidores.id_seguidor, seguidores.id_seguido, db)

    return True
   

def contar_seguidores_e_seguidos(id_seguidor: int, id_seguido: int, db: Session):
    usuario = db.query(Usuario.tipo_usuario).filter(Usuario.id == id_seguido).first()
    
    if usuario and usuario.tipo_usuario == "Entusiasta":
        # Contagem para "Entusiasta" (apenas status "aceito")
        status_condicao = "aceito"
    else:
        # Contagem para outros tipos de usuário (todos os pendentes)
        status_condicao = "pendente"

    # Contar quantos seguidores o usuário seguidor tem com o status especificado
    seguidores_count_seguidor = db.query(func.count(SeguidoresSeguidos.id)).filter(
        and_(
            SeguidoresSeguidos.id_seguido == id_seguidor,
            SeguidoresSeguidos.status == status_condicao
        )
    ).scalar()

    # Contar quantos usuários o usuário seguidor está seguindo com o status especificado
    seguidos_count_seguidor = db.query(func.count(SeguidoresSeguidos.id)).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == id_seguidor,
            SeguidoresSeguidos.status == status_condicao
        )
    ).scalar()

    # Contar quantos seguidores o usuário seguido tem com o status especificado
    seguidores_count_seguido = db.query(func.count(SeguidoresSeguidos.id)).filter(
        and_(
            SeguidoresSeguidos.id_seguido == id_seguido,
            SeguidoresSeguidos.status == status_condicao
        )
    ).scalar()

    # Contar quantos usuários o usuário seguido está seguindo com o status especificado
    seguidos_count_seguido = db.query(func.count(SeguidoresSeguidos.id)).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == id_seguido,
            SeguidoresSeguidos.status == status_condicao
        )
    ).scalar()

    # Atualizar os valores na tabela Usuario para o seguidor
    usuario_seguidor = db.query(Usuario).filter(Usuario.id == id_seguidor).first()
    if usuario_seguidor:
        usuario_seguidor.seguidores = seguidores_count_seguidor
        usuario_seguidor.seguidos = seguidos_count_seguidor

    # Atualizar os valores na tabela Usuario para o seguido
    usuario_seguido = db.query(Usuario).filter(Usuario.id == id_seguido).first()
    if usuario_seguido:
        usuario_seguido.seguidores = seguidores_count_seguido
        usuario_seguido.seguidos = seguidos_count_seguido

    db.commit()

def lista_usuarios_seguidos(id_usuario: int, db: Session):
    ids_seguidos = db.query(SeguidoresSeguidos.id_seguido).filter(
    SeguidoresSeguidos.id_seguidor == id_usuario
    ).all()
    
    # Extrai os IDs em uma lista simples
    ids_seguidos = [id_[0] for id_ in ids_seguidos]

    # Consulta para obter informações dos usuários seguidos
    usuarios_seguidos = db.query(Usuario).filter(
        Usuario.id.in_(ids_seguidos)
    ).all()

    # Formatação dos dados para retorno
    lista_usuarios = []
    for usuario in usuarios_seguidos:
        lista_usuarios.append({
            "id_usuario": usuario.id,
            "nome_usuario": usuario.nome_usuario,
            "foto_perfil": usuario.foto_perfil,
            "tipo_usuario": usuario.tipo_usuario
        })

    return lista_usuarios

def lista_usuarios_seguidores(id_usuario: int, db: Session):
    ids_seguidores = db.query(SeguidoresSeguidos.id_seguidor).filter(
    SeguidoresSeguidos.id_seguido == id_usuario
    ).all()
    
    # Extrai os IDs em uma lista simples
    ids_seguidores = [id_[0] for id_ in ids_seguidores]

    # Consulta para obter informações dos usuários seguidos
    usuarios_seguidos = db.query(Usuario).filter(
        Usuario.id.in_(ids_seguidores)
    ).all()

    # Formatação dos dados para retorno
    lista_usuarios = []
    for usuario in usuarios_seguidos:
        lista_usuarios.append({
            "id_usuario": usuario.id,
            "nome_usuario": usuario.nome_usuario,
            "foto_perfil": usuario.foto_perfil,
            "tipo_usuario": usuario.tipo_usuario
        })

    return lista_usuarios

def verifica_seguidor(id_usuario: int, id_usuario2: int, db: Session):
    seguimento_existente = db.query(SeguidoresSeguidos).filter(
        SeguidoresSeguidos.id_seguidor == id_usuario,
        SeguidoresSeguidos.id_seguido == id_usuario2
    ).first()

    if seguimento_existente:
        return True
    else:
        return False
    
def cancelar_seguir(seguidores, db: Session):
    # Crie uma query para selecionar o registro a ser deletado
    deletar_seguidor = db.query(SeguidoresSeguidos).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == seguidores.id_seguidor,
            SeguidoresSeguidos.id_seguido == seguidores.id_seguido
        )
    ).first()
    
    # Verifique se o registro existe
    if deletar_seguidor:
        db.delete(deletar_seguidor)
        db.commit()
        contar_seguidores_e_seguidos(seguidores.id_seguidor,seguidores.id_seguido,db)
        return False
    else:
        return True

def buscar_seguidores_seguidos(id_usuario:int,db: Session):
    usuario =db.query(Usuario).filter(
        and_(
            Usuario.id ==id_usuario
        )
    ).first()
    if usuario:
        return {
            "seguidores": usuario.seguidores,
            "seguidos": usuario.seguidos 

        }
    
FCM_ENDPOINT = "https://fcm.googleapis.com/v1/projects/app-pid/messages:send"

def enviar_notificacao_seguir(id_seguidor: int, id_seguido: int, db: Session, pendente: bool = False):
    seguidor = db.query(Usuario).filter(Usuario.id == id_seguidor).first()
    seguido = db.query(Usuario).filter(Usuario.id == id_seguido).first()

    if not seguidor or not seguido:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    title = "Solicitação de Seguimento" if pendente else "Novo Seguidor!"
    body = f"{seguidor.nome_usuario} quer seguir você." if pendente else f"{seguidor.nome_usuario} começou a seguir você."

    # Construindo a mensagem de notificação
    message = messaging.Message(
        token=seguido.fcm_token,
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                sound="default",
                click_action="FLUTTER_NOTIFICATION_CLICK",
            )
        ),
        data={
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "id": str(id_seguidor),
            "status": "pendente" if pendente else "aceito"
        }
    )

    try:
        # Enviando a mensagem usando o SDK do Firebase Admin
        response = messaging.send(message)
        print("Notificação enviada com sucesso:", response)
    except Exception as e:
        print("Erro ao enviar notificação:", e)


        
def atualizar_fcmToken(fcm_token_update: str, db: Session ):
    usuario = db.query(Usuario).filter(Usuario.id == fcm_token_update.id_usuario).first()
    if usuario:
        usuario.fcm_token = fcm_token_update.fcm_token
        db.commit()
        return {"message": "Token FCM atualizado com sucesso"}
    return {"message": "Usuário não encontrado"}, 404

def solicitacoes(id_usuario: int, db: Session):
    solicitacoes = db.query(
        SeguidoresSeguidos, Usuario.nome_usuario,
        Usuario.foto_perfil,Usuario.login,
        Usuario.tipo_usuario,Usuario.bio,
        Usuario.seguidores,Usuario.seguidos
        ).join(
        Usuario, SeguidoresSeguidos.id_seguidor == Usuario.id
    ).filter(
        SeguidoresSeguidos.id_seguido == id_usuario,
        SeguidoresSeguidos.status == 'pendente'
    ).all()

    # Estruturação dos dados de retorno
    lista_solicitacoes = []
    for solicitacao, nome_usuario,foto_perfil,login,tipo_usuario,bio,seguidores,seguidos in solicitacoes:
        lista_solicitacoes.append({
            "id": solicitacao.id,
            "id_usuario": solicitacao.id_seguidor,
            "id_seguido": solicitacao.id_seguido,
            "status": solicitacao.status,
            "nome_usuario": nome_usuario,
            "foto_perfil":foto_perfil,
            "login":login,
            "tipo_usuario":tipo_usuario,
            "bio":bio,
            "seguidores":seguidores,
            "seguidos":seguidos
        })

    return lista_solicitacoes
def acao_seguir(seguidores,db:Session):
    relacao = db.query(SeguidoresSeguidos).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == seguidores.id_seguidor,
            SeguidoresSeguidos.id_seguido == seguidores.id_seguido,
            SeguidoresSeguidos.status == 'pendente'
        )
    ).first()
    
    if not relacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    if seguidores.acao == 'aceito':
        relacao.status = 'aceito'
        db.commit()
        contar_seguidores_e_seguidos(seguidores.id_seguidor, seguidores.id_seguido, db)
        return {"message": "Solicitação de seguimento aceita com sucesso"}
    
    elif seguidores.acao == 'rejeitar':
        db.delete(relacao)
        db.commit()
        return {"message": "Solicitação de seguimento rejeitada com sucesso"}
    
    else:
        raise HTTPException(status_code=400, detail="Ação inválida")