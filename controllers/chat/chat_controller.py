#controllers/chat_controller.py
from models.chat.chat import Chat
from sqlalchemy.orm import Session,aliased
from sqlalchemy import or_, and_,func,desc
from models.usuario.usuario import Usuario



def cadastrar_mensagem(mensagem,db: Session):
    # Verifica se já existe uma conversa entre remetente e destinatário
    conversa = db.query(Chat).filter(
        or_(
            and_(Chat.remetente_id == mensagem.remetente_id, Chat.destinatario_id == mensagem.destinatario_id),
            and_(Chat.remetente_id == mensagem.destinatario_id, Chat.destinatario_id == mensagem.remetente_id)
        )
    ).first()

    if conversa:
        id_conversa = conversa.id_conversa
        nova_mensagem =Chat(remetente_id=mensagem.remetente_id, destinatario_id=mensagem.destinatario_id, texto=mensagem.texto, id_conversa=id_conversa)
        db.add(nova_mensagem)
        db.commit()
        db.refresh(nova_mensagem)
    else:
        maior_id_conversa = db.query(func.max(Chat.id_conversa)).scalar() or 0
        novo_id_conversa = maior_id_conversa + 1
        nova_conversa = Chat(remetente_id=mensagem.remetente_id, destinatario_id=mensagem.destinatario_id, texto=mensagem.texto, id_conversa=novo_id_conversa)
        db.add(nova_conversa)
        db.commit()
        db.refresh(nova_conversa)

def recuperar_nova_mensagem(db: Session, remetente_id: int, destinatario_id: int):
    # Consulta para recuperar a última mensagem da conversa entre remetente e destinatário
    ultima_mensagem = db.query(Chat).filter(
        or_(
            and_(Chat.remetente_id == remetente_id, Chat.destinatario_id == destinatario_id),
            and_(Chat.remetente_id == destinatario_id, Chat.destinatario_id == remetente_id)
        )
    ).order_by(Chat.id.desc()).first()
    
    return ultima_mensagem
def recuperar_conversas_usuario(db: Session, remetente_id: int, destinatario_id: int):
    UsuarioRemetente = aliased(Usuario)
    UsuarioDestinatario = aliased(Usuario)
    conversas = (
        db.query(
            Chat,
            UsuarioRemetente.nome_usuario.label('nome_remetente'),
            UsuarioDestinatario.nome_usuario.label('nome_destinatario'),
            
        )
        .join(UsuarioRemetente, Chat.remetente_id == UsuarioRemetente.id)
        .join(UsuarioDestinatario, Chat.destinatario_id == UsuarioDestinatario.id)
        .filter(
            or_(
                and_(Chat.remetente_id == remetente_id, Chat.destinatario_id == destinatario_id),
                and_(Chat.remetente_id == destinatario_id, Chat.destinatario_id == remetente_id)
            )
        )
        .all()
    )

    # Converting to dictionary manually
    conversas_dict = []
    for chat, nome_remetente, nome_destinatario, in conversas:
        chat_dict = chat.to_dict()
        chat_dict.update({
            "nome_remetente": nome_remetente,
            "nome_destinatario": nome_destinatario,
            "id_conversa": chat.id_conversa,
        })
        conversas_dict.append(chat_dict)

    return conversas_dict


def conversas_chat(id_usuario, db: Session):
    UsuarioRemetente = aliased(Usuario)
    UsuarioDestinatario = aliased(Usuario)
    
    # Subquery para obter a última mensagem trocada entre os usuários
    subquery = (
        db.query(
            Chat.id_conversa,
            func.max(Chat.id).label('ultima_mensagem_id'),
            
        )
        .filter(or_(Chat.remetente_id == id_usuario, Chat.destinatario_id == id_usuario))
        .group_by(Chat.id_conversa)
        .subquery()
    )

    # Query principal para obter as conversas e os detalhes dos usuários
    conversas = (
        db.query(
            Chat,
            UsuarioRemetente.nome_usuario.label('nome_remetente'),
            UsuarioDestinatario.nome_usuario.label('nome_destinatario'),
            UsuarioDestinatario.foto_perfil.label('foto_perfil'),
            UsuarioDestinatario.id.label("id_destinatario")
        )
        .join(UsuarioRemetente, Chat.remetente_id == UsuarioRemetente.id)
        .join(UsuarioDestinatario, Chat.destinatario_id == UsuarioDestinatario.id)
        .join(subquery, Chat.id == subquery.c.ultima_mensagem_id)
        .filter(or_(Chat.remetente_id == id_usuario, Chat.destinatario_id == id_usuario))
        .order_by(desc(Chat.data_envio))
        .all()
    )

    # Converting to dictionary manually
    conversas_dict = []
    for chat, nome_remetente, nome_destinatario, foto_perfil,id_destinatario in conversas:
        chat_dict = chat.to_dict_conversations()
        chat_dict.update({
            "nome_remetente": nome_remetente,
            "nome_destinatario": nome_destinatario,
            "foto_perfil":foto_perfil,
            "id_usuario":id_destinatario,
            "ultima_mensagem": chat.texto  # Assumindo que o campo de texto da mensagem é 'texto'
        })
        conversas_dict.append(chat_dict)

    return conversas_dict