# controllers/usuario_controller.py
import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from models.usuario import Usuario
from dependencies import get_db


def criar_usuario(db: Session, usuario_create):

    senha = usuario_create.senha.encode('utf-8')

    hashed_password = bcrypt.hashpw(senha, bcrypt.gensalt())
    
    # Cria o usuário com a senha hash
    db_usuario = Usuario(
        email=usuario_create.email,
        nome_usuario=usuario_create.nome_usuario,
        login=usuario_create.login,
        senha=hashed_password.decode("utf-8"),
        tipo_usuario=usuario_create.tipo_usuario,
        data_nascimento=usuario_create.data_nascimento,
        
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def login_usuario(db: Session, login: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.login == login).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    

    # Verifica se a senha fornecida corresponde à armazenada
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    return usuario



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

def obter_dados_usuario(email: str, db: Session = Depends(get_db)):
    # Buscar o usuário com o login fornecido
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    # Verificar se o usuário existe
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar os dados do usuário
    return usuario


def verificar_credenciais(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Email fornecido incorreto")
    
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    return True
def upload_login(db: Session, email: str, senha_atual: str, login_update: str, senha_update: str, email_update: str):
    # Busca o usuário no banco de dados pelo e-mail fornecido
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    # Verifica se o usuário foi encontrado
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verifica se a senha atual fornecida corresponde à senha armazenada
    if not bcrypt.checkpw(senha_atual.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Senha atual incorreta")
    
    # Atualiza o login, senha e e-mail do usuário se a senha atual for válida
    usuario.login = login_update
    usuario.senha = bcrypt.hashpw(senha_update.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuario.email = email_update
    
    # Salva as alterações no banco de dados
    db.commit()
    db.refresh(usuario)
    
    # Retorna o usuário atualizado
    return usuario

