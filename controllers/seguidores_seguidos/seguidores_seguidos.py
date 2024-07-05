from firebase_admin import messaging
from google.auth.transport.requests import Request
from FCMManager import get_access_token
from fastapi import HTTPException
from models.seguidores_seguidos.seguidores_seguidos import SeguidoresSeguidos
from models.usuario.usuario import Usuario
from sqlalchemy import  and_,func
from sqlalchemy.orm import Session
def registrar_seguidores(seguidores, db:Session):
    relacao_existente = db.query(SeguidoresSeguidos).filter(
        and_(
            SeguidoresSeguidos.id_seguidor == seguidores.id_seguidor,
            SeguidoresSeguidos.id_seguido == seguidores.id_seguido
        )
    ).first()
    
    if relacao_existente:
            return False

    # Criar nova relação
    nova_relacao = SeguidoresSeguidos(
        id_seguidor=seguidores.id_seguidor,
        id_seguido=seguidores.id_seguido
    )
    db.add(nova_relacao)
    db.commit()
    db.refresh(nova_relacao)
    contar_seguidores_e_seguidos(seguidores.id_seguidor,seguidores.id_seguido,db)
    if nova_relacao:
        enviar_notificacao_seguir(seguidores.id_seguidor, seguidores.id_seguido, db)
        return True
   

def contar_seguidores_e_seguidos(id_seguidor: int, id_seguido: int, db: Session):
    # Contar quantos seguidores o usuário seguidor tem
    seguidores_count_seguidor = db.query(func.count(SeguidoresSeguidos.id)).filter(
        SeguidoresSeguidos.id_seguido == id_seguidor
    ).scalar()

    # Contar quantos usuários o usuário seguidor está seguindo
    seguidos_count_seguidor = db.query(func.count(SeguidoresSeguidos.id)).filter(
        SeguidoresSeguidos.id_seguidor == id_seguidor
    ).scalar()

    # Contar quantos seguidores o usuário seguido tem
    seguidores_count_seguido = db.query(func.count(SeguidoresSeguidos.id)).filter(
        SeguidoresSeguidos.id_seguido == id_seguido
    ).scalar()

    # Contar quantos usuários o usuário seguido está seguindo
    seguidos_count_seguido = db.query(func.count(SeguidoresSeguidos.id)).filter(
        SeguidoresSeguidos.id_seguidor == id_seguido
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

def enviar_notificacao_seguir(id_seguidor: int, id_seguido: int, db: Session):
    seguidor = db.query(Usuario).filter(Usuario.id == id_seguidor).first()
    seguido = db.query(Usuario).filter(Usuario.id == id_seguido).first()

    if not seguidor or not seguido:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Construindo a mensagem de notificação
    message = messaging.Message(
        token=seguido.fcm_token,
        notification=messaging.Notification(
            title="Novo Seguidor!",
            body=f"{seguidor.nome_usuario} começou a seguir você."
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
            "status": "done"
        }
    )

    try:
        # Enviando a mensagem usando o SDK do Firebase Admin
        response = messaging.send(message)
        print("Notificação enviada com sucesso:", response)
        print("Notificação enviada com sucesso:", message)
    except Exception as e:
        print("Erro ao enviar notificação:", e)
def atualizar_fcmToken(fcm_token_update: str, db: Session ):
    usuario = db.query(Usuario).filter(Usuario.id == fcm_token_update.id_usuario).first()
    if usuario:
        usuario.fcm_token = fcm_token_update.fcm_token
        db.commit()
        return {"message": "Token FCM atualizado com sucesso"}
    return {"message": "Usuário não encontrado"}, 404