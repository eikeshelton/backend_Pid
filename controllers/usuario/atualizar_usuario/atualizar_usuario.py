import bcrypt
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from models.usuario.usuario import Usuario
from controllers.guias.guias import contar_capas_guias



def atualizar_usuario(db: Session, email: str, usuario_update):
    db_usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if db_usuario:
        # Atualizar os campos do usuário com base nos dados fornecidos
        for key, value in usuario_update.dict(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

def obter_dados_usuario(id_usuario: int, db: Session):
    contar_capas_guias(id_usuario, db)
    
    # Buscar o usuário com o tipo_usuario carregado
    usuario = (
        db.query(Usuario)
        .options(joinedload(Usuario.tipo_usuario))  # Carrega a relação
        .filter(Usuario.id == id_usuario)
        .first()
    )
    
    # Verificar se o usuário existe
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar os dados do usuário com o tipo de usuário
    return {
        "bio": usuario.bio,
        "email": usuario.email,
        "foto_perfil": usuario.foto_perfil,
        "id": usuario.id,
        "login": usuario.login,
        "nome_usuario": usuario.nome_usuario,
        "publicacoes": usuario.publicacoes,
        "seguidores": usuario.seguidores,
        "seguidos": usuario.seguidos,
        "senha": usuario.senha,
        "sexo": usuario.sexo,
        "tipo_usuario": usuario.tipo_usuario.tipo,
        "token": usuario.token_reset_senha
        
          # Acesso à descrição
    }
    
def upload_login(db: Session, login_update: Usuario, senha_update: str, email_update: str, id: int):
    # Busca o usuário no banco de dados pelo id atual fornecido
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    
    # Verifica se o usuário foi encontrado
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualiza o login se fornecido
    if login_update is not None:
        usuario.login = login_update
    
    # Atualiza a senha se fornecida
    if senha_update is not None:
        usuario.senha = bcrypt.hashpw(senha_update.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Atualiza o e-mail se fornecido
    if email_update is not None:
        usuario.email = email_update
    
    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(usuario)
    
    # Retorna o usuário atualizado
    return usuario
