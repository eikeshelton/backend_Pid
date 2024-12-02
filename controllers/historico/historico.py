from models.historico.historico import HistoricoPesquisa
from models.usuario.usuario import Usuario
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime,timezone


    
def registrar_pesquisado(db: Session, registrar_busca):
    # Verifica se usuario_id é igual ao pesquisado_id
    if registrar_busca.usuario_id == registrar_busca.pesquisado_id:
        return None  # Não registra e retorna None

    # Verifica se a pesquisa já existe
    pesquisa_existente = db.query(HistoricoPesquisa).filter(
        and_(
            HistoricoPesquisa.usuario_id == registrar_busca.usuario_id,
            HistoricoPesquisa.pesquisado_id == registrar_busca.pesquisado_id
        )
    ).first()

    if pesquisa_existente:
        # Atualiza o campo 'data_verificacao' com o horário atual
        pesquisa_existente.data_verificacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(pesquisa_existente)
        return pesquisa_existente

    # Registra a nova pesquisa com a data_verificacao
    pesquisa = HistoricoPesquisa(
        usuario_id=registrar_busca.usuario_id,
        pesquisado_id=registrar_busca.pesquisado_id,
        data_verificacao=datetime.now(timezone.utc)  # Define o horário atual
    )
    db.add(pesquisa)
    db.commit()
    db.refresh(pesquisa)
    return pesquisa

def buscar_pesquisado(db: Session, usuario_id: int, limite: int = 4) -> list[dict]:
    # Busca os registros ordenados pela data_verificacao mais recente (maior data)
    pesquisas = (
        db.query(HistoricoPesquisa)
        .filter(HistoricoPesquisa.usuario_id == usuario_id)
        .order_by(HistoricoPesquisa.data_verificacao.desc())  # Ordena pela maior data_verificacao
        .limit(limite)
        .all()
    )

    # Coleta os IDs dos pesquisados
    pesquisado_ids = [pesquisa.pesquisado_id for pesquisa in pesquisas]

    # Busca os usuários correspondentes aos pesquisado_ids
    usuarios = db.query(Usuario).filter(Usuario.id.in_(pesquisado_ids)).all()

    # Cria um dicionário de usuários para acessar facilmente pelo id
    usuarios_dict = {usuario.id: usuario for usuario in usuarios}

    # Estrutura o resultado no formato de lista de dicionários, incluindo a data_verificacao
    resultado = []
    for pesquisa in pesquisas:
        usuario = usuarios_dict.get(pesquisa.pesquisado_id)  # Pega o usuário correspondente
        if usuario:
            resultado.append({
                "id_usuario": usuario.id,
                "login": usuario.login,
                "tipo_usuario": {
                    "id": usuario.tipo_usuario.id,
                    "tipo": usuario.tipo_usuario.tipo
                },
                "foto_perfil": usuario.foto_perfil,
                "nome_usuario": usuario.nome_usuario,
                "bio": usuario.bio,
                "seguidores": usuario.seguidores,
                "seguidos": usuario.seguidos,
                "data_verificacao": pesquisa.data_verificacao  # Inclui a data de verificação da pesquisa
            })

    return resultado

