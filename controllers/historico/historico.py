from models.historico.historico import HistoricoPesquisa
from models.usuario.usuario import Usuario
from sqlalchemy import and_
from sqlalchemy.orm import Session



    
def registrar_pesquisado(db: Session, registrar_busca):
    pesquisa_existente = db.query(HistoricoPesquisa).filter(
        and_(
            HistoricoPesquisa.usuario_id == registrar_busca.usuario_id,
            HistoricoPesquisa.pesquisado_id == registrar_busca.pesquisado_id
        )
    ).first()
    if pesquisa_existente:
        return pesquisa_existente
    pesquisa = HistoricoPesquisa(
        usuario_id=registrar_busca.usuario_id,
        pesquisado_id=registrar_busca.pesquisado_id
    )
    db.add(pesquisa)
    db.commit()
    db.refresh(pesquisa)
    return pesquisa

def buscar_pesquisado(db: Session, usuario_id: int, limite: int = 4) -> list[dict]:
    # Busca os últimos registros em HistoricoPesquisa que correspondem ao usuario_id, ordenados pelo id (incremental)
    pesquisas = (
        db.query(HistoricoPesquisa)
        .filter(HistoricoPesquisa.usuario_id == usuario_id)
        .order_by(HistoricoPesquisa.id.desc())  # Ordena pelos IDs mais recentes
        .limit(limite)
        .all()
    )

    # Coleta os IDs dos pesquisados
    pesquisado_ids = [pesquisa.pesquisado_id for pesquisa in pesquisas]

    # Busca os usuários correspondentes aos pesquisado_ids e mapeia para o formato desejado
    usuarios = db.query(Usuario).filter(Usuario.id.in_(pesquisado_ids)).all()

    # Estrutura o resultado no formato de lista de dicionários
    resultado = []
    for usuario in usuarios:
        resultado.append({
            "id_usuario": usuario.id,
            "login": usuario.login,
            "tipo_usuario": usuario.tipo_usuario,
            "foto_perfil": usuario.foto_perfil,
            "nome_usuario": usuario.nome_usuario,
            "bio": usuario.bio,
            "seguidores": usuario.seguidores,
            "seguidos": usuario.seguidos,
        })

    return resultado
