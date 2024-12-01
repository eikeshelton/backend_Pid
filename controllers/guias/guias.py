from models.guias.capa_guias import *
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.usuario.usuario import Usuario
from models.schema.schema import GuiaCreate
from fastapi import HTTPException
import boto3
import os
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
logger = logging.getLogger(__name__)

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")

s3_client = boto3.client('s3',
aws_access_key_id= aws_access_key_id,
aws_secret_access_key=aws_secret_access_key,
region_name='us-east-1'  # Ex: 'us-west-1'
)
BUCKET_NAME = bucket_name  # substitua pelo nome do seu bucket S3

def cadastrar_guia_completo(guia: GuiaCreate, db: Session):
    # Criando e salvando CapaGuia
    db_capa_guia = CapaGuia(
        titulo=guia.titulo,
        foto_url=guia.foto_url,
        id_usuario=guia.id_usuario
    )
    db.add(db_capa_guia)
    db.commit()
    db.refresh(db_capa_guia)

    # Criando e salvando Guia associado à CapaGuia
    db_guia = Guia(
        id_guia=db_capa_guia.id_guias,
        id_usuario=guia.id_usuario,
        foto_guia=guia.foto_guia,
        titulo_guia=guia.titulo_guia,
        texto_guia=guia.texto_guia
    )
    db.add(db_guia)
    db.commit()
    db.refresh(db_guia)

    return True

def buscar_capas_guias(id_usuario:int,db:Session):
    db_capa_guia= db.query(CapaGuia).filter(CapaGuia.id_usuario == id_usuario).all()
    return db_capa_guia

def busca_guia_id (id_guia:int,db:Session):
    db_guia = db.query(Guia).filter(Guia.id_guia==id_guia).first()
    return db_guia


def contar_capas_guias(id_usuario: int, db: Session) -> int:
    # Faz a contagem de quantas vezes o id_usuario aparece na tabela capa_guias
    count = db.query(func.count(CapaGuia.id_usuario)).filter(CapaGuia.id_usuario == id_usuario).scalar()
    
    # Atualiza a coluna 'publicacoes' na tabela usuario com o valor da contagem
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if usuario:
        usuario.publicacoes = count
        db.commit()  # Confirma a alteração no banco de dados

    return count


def deletar_guia_completo(id_guia: int, db: Session):
    # Primeiro, recupera o registro do Guia para verificar se ele existe
    db_guia = db.query(Guia).filter(Guia.id_guia == id_guia).first()
    if not db_guia:
        raise HTTPException(status_code=404, detail="Guia não encontrado.")

    # Recupera a CapaGuia associada para exclusão
    db_capa_guia = db.query(CapaGuia).filter(CapaGuia.id_guias == id_guia).first()
    if not db_capa_guia:
        raise HTTPException(status_code=404, detail="CapaGuia não encontrada.")

    try:
        # Delete as imagens do S3
        if db_guia.foto_guia:
            try:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=db_guia.foto_guia)
            except Exception as e:
                logger.error(f"Erro ao deletar a foto do guia {id_guia} no S3: {str(e)}")
                raise HTTPException(status_code=500, detail="Erro ao deletar a foto do guia no S3.")

        if db_capa_guia.foto_url:
            try:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=db_capa_guia.foto_url)
            except Exception as e:
                logger.error(f"Erro ao deletar a CapaGuia {id_guia} no S3: {str(e)}")
                raise HTTPException(status_code=500, detail="Erro ao deletar a CapaGuia no S3.")

        # Remove os registros em ordem correta (Guia → CapaGuia)
        db.delete(db_guia)
        db.delete(db_capa_guia)
        db.commit()

    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        logger.error(f"Erro ao deletar guia {id_guia}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição.")

    return {"detail": "Guia e CapaGuia deletados com sucesso."}
