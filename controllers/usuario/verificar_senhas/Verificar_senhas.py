import bcrypt
import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.usuario import Usuario
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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
    remetente = ""  # Insira seu endereço de e-mail
    senha = ""  # Insira sua senha

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