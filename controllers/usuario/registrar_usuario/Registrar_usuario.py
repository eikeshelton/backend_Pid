import bcrypt
from sqlalchemy.orm import Session
from models.usuario import Usuario

# Cria o usuário com a senha hash
def criptografar(senha:str)->str:
    senha_bytes = senha.encode('utf-8')
    hashed_password = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def criar_usuario(db: Session, usuario_create):
    hashed_password = criptografar(usuario_create.senha)
    
    
    db_usuario = Usuario(
        email=usuario_create.email,
        nome_usuario=usuario_create.nome_usuario,
        login=usuario_create.login,
        senha=hashed_password,
        tipo_usuario=usuario_create.tipo_usuario,
        data_nascimento=usuario_create.data_nascimento,
        bio=usuario_create.bio,
        
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

