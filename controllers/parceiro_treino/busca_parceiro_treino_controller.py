from sqlalchemy.orm import Session
from models.parceiro_treino import ParceiroTreino
from models.usuario import Usuario
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from models.estado import Estado
from models.municipio import Municipio
from models.schema.schema import ParceiroTreinoResponse
from typing import List


def get_estado_id(db: Session, id_estado: int):
    estado = db.query(Estado).filter(Estado.codigo_ibge == id_estado).first()
    if not estado:
        raise HTTPException(status_code=404, detail=f"Estado {id_estado} não encontrado")
    return estado.codigo_ibge

def get_municipio_id(db: Session, id_cidade: int, estado_id: int):
    municipio = db.query(Municipio).filter(Municipio.codigo_ibge == id_cidade, Municipio.estado_id == estado_id).first()
    if not municipio:
        raise HTTPException(status_code=404, detail=f"Município {id_cidade} não encontrado no estado {estado_id}")
    return municipio.codigo_ibge

def buscar_parceiros_treino(db: Session, filtros) -> List[ParceiroTreinoResponse]:
    estado_id = get_estado_id(db, filtros.estado_codigo_ibge)
    municipio_id = get_municipio_id(db, filtros.municipio_codigo_ibge, filtros.estado_codigo_ibge)
    data_limite = datetime.now(timezone.utc) - timedelta(days=7)
    
    try:
        query = db.query(
            ParceiroTreino, Usuario.nome_usuario, Usuario.foto_perfil, Usuario.sexo,Usuario.seguidos,
            Usuario.seguidores,Usuario.bio,Usuario.login
        ).join(
            Usuario, ParceiroTreino.id_usuario == Usuario.id
        ).filter(
            ParceiroTreino.modalidade == filtros.modalidade,
            ParceiroTreino.estado_codigo_ibge == estado_id,
            ParceiroTreino.municipio_codigo_ibge == municipio_id,
            ParceiroTreino.datetime_registro >= data_limite
        )
        
        # Filtros opcionais
        if filtros.dia_da_semana:
            query = query.filter(ParceiroTreino.dia_da_semana == filtros.dia_da_semana)
        if filtros.local:
            query = query.filter(ParceiroTreino.local == filtros.local)
        if filtros.agrupamento_muscular:
            query = query.filter(ParceiroTreino.agrupamento_muscular == filtros.agrupamento_muscular)
        if filtros.horario:
            query = query.filter(ParceiroTreino.horario == filtros.horario)
        if filtros.tempo_treino:
            query = query.filter(ParceiroTreino.tempo_treino == filtros.tempo_treino)
        if filtros.sexo:
            query = query.filter(Usuario.sexo == filtros.sexo)

        parceiros = []
        for parceiro_treino, nome, foto_perfil, sexo, seguindo, seguidores, bio,login in query.all():
            local = parceiro_treino.local if parceiro_treino.local else ""
            horario = parceiro_treino.horario.strftime('%H:%M') if parceiro_treino.horario else ""
            sexo_usuario = sexo if sexo else ""
            
            parceiro = ParceiroTreinoResponse(
                id=parceiro_treino.id,
                id_usuario= parceiro_treino.id_usuario,
                modalidade=parceiro_treino.modalidade,
                estado_codigo_ibge=parceiro_treino.estado_codigo_ibge,
                municipio_codigo_ibge=parceiro_treino.municipio_codigo_ibge,
                local=local,
                horario=horario,
                datetime_registro=parceiro_treino.datetime_registro,
                nome_usuario=nome,
                foto_perfil=foto_perfil,
                seguidores=seguidores,
                seguidos=seguindo,
                bio=bio,
                login=login,
                sexo_usuario=sexo_usuario
            )
            parceiros.append(parceiro)
        
        return parceiros
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar parceiros de treino: {str(e)}")