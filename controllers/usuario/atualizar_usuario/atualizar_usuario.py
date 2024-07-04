import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from models.usuario.usuario import Usuario
from dependencies import get_db
from controllers.seguidores_seguidos.seguidores_seguidos import contar_seguidores_e_seguidos


def atualizar_usuario(db: Session, email: str, usuario_update: Usuario):
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

def obter_dados_usuario(email: str, db: Session):
    # Buscar o usuário com o login fornecido
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    # Verificar se o usuário existe
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar os dados do usuário
    return usuario
    
def upload_login(db: Session,login_update: Usuario, senha_update: Usuario.senha, email_update: Usuario.email,id:Usuario.id):
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
