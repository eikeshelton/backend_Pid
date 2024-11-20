import bcrypt
from sqlalchemy.orm import Session
from models.usuario.usuario import Usuario,TipoUsuario
from fastapi import HTTPException
# Cria o usuário com a senha hash
def criptografar(senha:str)->str:
    senha_bytes = senha.encode('utf-8')
    hashed_password = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def criar_usuario(db: Session, usuario_create):
    # Verifica se o email, nome de usuário ou login já existe
    usuario_existente = db.query(Usuario).filter(
        (Usuario.email == usuario_create.email) |
        (Usuario.nome_usuario == usuario_create.nome_usuario) |
        (Usuario.login == usuario_create.login)
    ).first()

    # Se algum usuário com o mesmo email, nome ou login já existir, lançar um erro
    if usuario_existente:
        if usuario_existente.email == usuario_create.email:
            raise HTTPException(status_code=400, detail="O email informado já está em uso.")
        if usuario_existente.nome_usuario == usuario_create.nome_usuario:
            raise HTTPException(status_code=400, detail="O nome de usuário informado já está em uso.")
        if usuario_existente.login == usuario_create.login:
            raise HTTPException(status_code=400, detail="O login informado já está em uso.")

    # Criptografa a senha do usuário
    hashed_password = criptografar(usuario_create.senha)

    # Busca o tipo de usuário
    tipo_usuario = db.query(TipoUsuario).filter(TipoUsuario.tipo == usuario_create.tipo_usuario).first()

    # Se o tipo de usuário não for encontrado, lançar um erro
    if tipo_usuario is None:
        raise HTTPException(status_code=400, detail="Tipo de usuário não encontrado")

    # Cria o novo usuário
    db_usuario = Usuario(
        email=usuario_create.email,
        nome_usuario=usuario_create.nome_usuario,
        login=usuario_create.login,
        senha=hashed_password,
        tipo_usuario=tipo_usuario,
        data_nascimento=usuario_create.data_nascimento,
        bio=usuario_create.bio,
    )
    
    # Adiciona o usuário ao banco de dados
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario

