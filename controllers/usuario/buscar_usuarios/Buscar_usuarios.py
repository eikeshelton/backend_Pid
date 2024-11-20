# controllers/usuario_controller.py
from sqlalchemy.orm import Session
from models.usuario.usuario import *
from sqlalchemy import join,func

def buscar_usuarios_por_nome(db: Session, login: str, limite: int = 5) -> list[dict]:
    # Faz JOIN explícito entre Usuario e TipoUsuario
    resultado = (
        db.query(
            Usuario.id,
            Usuario.login,
            TipoUsuario.tipo.label("tipo_usuario"),  # Campo do tipo de usuário
            Usuario.foto_perfil,
            Usuario.nome_usuario,
            Usuario.bio,
            Usuario.seguidores,
            Usuario.seguidos
        )
        .join(TipoUsuario, Usuario.tipo_usuario_id == TipoUsuario.id)  # JOIN explícito
        .filter(func.lower(Usuario.login).startswith(func.lower(login)))
        .order_by(Usuario.login)
        .limit(limite)
        .all()
    )

    # Converte para lista de dicionários
    usuarios = [
        dict(
            zip(
                [
                    "id_usuario", 
                    "login", 
                    "tipo_usuario", 
                    "foto_perfil", 
                    "nome_usuario", 
                    "bio", 
                    "seguidores", 
                    "seguidos"
                ],
                res
            )
        )
        for res in resultado
    ]

    return usuarios
def buscar_usuario_por_tipo(tipo: str, db: Session) -> list[dict]:
    # Query com JOIN entre Usuario e TipoUsuario
    resultado = (
        db.query(
            Usuario.id,
            Usuario.login,
            TipoUsuario.tipo.label("tipo_usuario"),  # Nome do tipo
            Usuario.foto_perfil,
            Usuario.nome_usuario,
            Usuario.bio,
            Usuario.seguidores,
            Usuario.seguidos
        )
        .join(TipoUsuario, Usuario.tipo_usuario_id == TipoUsuario.id)
        .filter(TipoUsuario.tipo == tipo)
        .all()
    )

    # Converter resultado em lista de dicionários
    usuarios = [
        dict(zip(
            ["id_usuario", "login", "tipo_usuario", "foto_perfil", "nome_usuario", "bio", "seguidores", "seguidos"],
            res
        )) 
        for res in resultado
    ]
    return usuarios