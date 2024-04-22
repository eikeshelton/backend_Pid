# controllers/usuario_controller.py
import bcrypt
import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends
from models.usuario import Usuario
from dependencies import get_db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    # Procura o usuário pelo email
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario is None:
        # Se o usuário não for encontrado, levanta uma exceção HTTP 404
        raise HTTPException(status_code=404, detail="Email fornecido incorreto")
    
    # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        # Se a senha estiver incorreta, levanta uma exceção HTTP 401
        raise HTTPException(status_code=401, detail="Senha incorreta")

    # Se as credenciais estiverem corretas, retorna o ID do usuário
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

def adicionar_token_reset_senha(db: Session, email: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        token = secrets.token_urlsafe(32)
        usuario.token_reset_senha = token
        db.commit()

        # Enviar e-mail
        enviar_email(usuario.email, token)
        return token
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

def obter_token_reset_senha(db: Session, email: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return usuario.token_reset_senha
    else:
        return None

def limpar_token_reset_senha(db: Session, email: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        usuario.token_reset_senha = None
        db.commit()
        return True
    else:
        return False
    
def alterar_senha(db: Session, email: str, nova_senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        # Hash da nova senha
        nova_senha_hashed = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
        
        # Atualiza a senha do usuário
        usuario.senha = nova_senha_hashed.decode("utf-8")
        
        # Commit e refresh no banco de dados
        db.commit()
        db.refresh(usuario)
        
        return usuario
    else:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
def enviar_email(destinatario: str, token: str):
    remetente = "weactivebsb@outlook.com"  # Insira seu endereço de e-mail
    senha = "Fitness123"  # Insira sua senha

    # Configurar mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = "Redefinição de Senha"

    corpo_email = f"""
    Olá,

    Você solicitou uma redefinição de senha. Use o seguinte token para redefinir sua senha:

    Token: {token}

    Se você não solicitou esta alteração, ignore este e-mail.

    Atenciosamente,
    WeActive
    """

    msg.attach(MIMEText(corpo_email, 'plain'))

    # Conectar ao servidor SMTP
    servidor_smtp = smtplib.SMTP('smtp-mail.outlook.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente, senha)

    # Enviar e-mail
    servidor_smtp.sendmail(remetente, destinatario, msg.as_string())

    # Desconectar do servidor SMTP
    servidor_smtp.quit()

