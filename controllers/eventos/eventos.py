from models.eventos.eventos import Eventos
from models.eventos.participantes import Participantes
from models.schema.schema import *
from models.usuario.usuario import Usuario
from sqlalchemy import func
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException, status
def cadastrar_evento(cadastro: CadastrarEvento, db: Session):
    try:
        db_cadastro = Eventos(
            organizador_id=cadastro.organizador_id,
            nome=cadastro.nome,
            descricao=cadastro.descricao,
            data_inicio=cadastro.data_inicio,
            hora_inicio=cadastro.hora_inicio,
            localizacao=cadastro.localizacao,
            municipio_id=cadastro.municipio_id,
        )
        db.add(db_cadastro)
        db.commit()
        db.refresh(db_cadastro)
        return {"message": "Evento cadastrado com sucesso", "evento": db_cadastro}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao cadastrar evento: {str(e)}"
        )
    
def buscar_eventos(municipio_id: int, usuario_id: int, db: Session):
    # Realiza a busca por eventos e carrega os dados do organizador
    eventos = (
        db.query(Eventos)
        .options(joinedload(Eventos.organizador))  # Supondo que o relacionamento está definido
        .filter(Eventos.municipio_id == municipio_id)
        .all()
    )
    
    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado para este município.")
    
    # Monta a resposta com as informações do organizador e a verificação do interesse
    eventos_com_detalhes = []
    for evento in eventos:
        # Verifica se o usuário declarou interesse no evento
        interesse_declarado = db.query(Participantes).filter(
            Participantes.evento_id == evento.id,
            Participantes.participante_id == usuario_id
        ).first() is not None
        
        eventos_com_detalhes.append({
            "id": evento.id,
            "organizador_id": evento.organizador_id,
            "nome": evento.nome,
            "descricao": evento.descricao,
            "data_inicio": evento.data_inicio,
            "hora_inicio": evento.hora_inicio,
            "localizacao": evento.localizacao,
            "municipio_id": evento.municipio_id,
            "organizador": {
                "nome": evento.organizador.nome_usuario,  # Obtendo o nome do organizador
                "foto_perfil": evento.organizador.foto_perfil  # Obtendo a foto do organizador
            },
            "quantidade_participantes": evento.quantidade_participantes,
            "interesse_declarado": interesse_declarado  # Campo que indica se o interesse foi declarado
        })
    
    return eventos_com_detalhes

def cadastrar_usuario_evento(evento_id: int, participante_id: int,db: Session):
    # Verificar se o usuário já está cadastrado no evento
    participante_existente = db.query(Participantes).filter(
        Participantes.evento_id == evento_id,
        Participantes.participante_id == participante_id
    ).first()

    if participante_existente:
        return False

    # Adicionar o usuário ao evento
    novo_participante = Participantes(evento_id=evento_id, participante_id=participante_id)
    db.add(novo_participante)
    db.commit()
    db.refresh(novo_participante)
    
    # Atualizar a quantidade de participantes
    atualizar_quantidade_participantes(evento_id,db)
    
    return True

def descadastrar_usuario_evento(evento_id: int, participante_id: int,db: Session):
    # Procurar o registro do participante no evento
    participante = db.query(Participantes).filter(
        Participantes.evento_id == evento_id,
        Participantes.participante_id == participante_id
    ).first()

    if not participante:
        return False

    # Remover o participante do evento
    db.delete(participante)
    db.commit()
    
    # Atualizar a quantidade de participantes
    atualizar_quantidade_participantes(evento_id,db)
    
    return False

def atualizar_quantidade_participantes(evento_id: int,db: Session):
    # Contar o número de participantes para o evento específico
    quantidade = db.query(func.count(Participantes.id)).filter(Participantes.evento_id == evento_id).scalar()
    
    # Atualizar o campo quantidade_participantes na tabela de eventos
    db.query(Eventos).filter(Eventos.id == evento_id).update({"quantidade_participantes": quantidade})
    
    # Confirmar a transação
    db.commit()


def atualizar_interesse_evento(evento_id,interesse,db: Session):
    evento = db.query(Eventos).filter(Eventos.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    # Verifica se o participante já declarou interesse no evento
    interesse_atual = db.query(Participantes).filter(
        Participantes.evento_id == evento_id,
        Participantes.participante_id == interesse.participante_id
    ).first()

    if interesse.interesse_declarado:
        # Adiciona interesse se ainda não existe
        if not interesse_atual:
            novo_participante = Participantes(evento_id=evento_id, participante_id=interesse.participante_id)
            db.add(novo_participante)
            evento.quantidade_participantes += 1
    else:
        # Remove interesse se existe
        if interesse_atual:
            db.delete(interesse_atual)
            evento.quantidade_participantes -= 1

    # Salva as mudanças
    db.commit()
    db.refresh(evento)

    # Retorna o evento atualizado
    return evento


def listar_participantes_evento(evento_id: int, db: Session):
    # Localiza os participantes do evento
    participantes = db.query(Participantes).filter(Participantes.evento_id == evento_id).all()
    
    if not participantes:
        return []  # Retorna uma lista vazia se não houver participantes

    # Pega os IDs dos participantes
    participante_ids = [p.participante_id for p in participantes]

    # Busca os detalhes dos usuários e seleciona apenas os campos desejados
    usuarios = (
        db.query(Usuario.id, Usuario.nome_usuario, Usuario.foto_perfil)
        .filter(Usuario.id.in_(participante_ids))
        .all()
    )

    # Converte os resultados para um dicionário
    return [{"id": usuario.id, "nome_usuario": usuario.nome_usuario, "foto_perfil": usuario.foto_perfil} for usuario in usuarios]