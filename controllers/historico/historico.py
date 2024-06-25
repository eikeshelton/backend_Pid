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

def buscar_pesquisado(db: Session, usuario_id: int,limite: int = 4)-> list[Usuario]:
    # Busca os primeiros 5 registros em HistoricoPesquisa que correspondem ao usuario_id
    pesquisas = db.query(HistoricoPesquisa).filter(HistoricoPesquisa.usuario_id == usuario_id).limit(limite).all()

    # Coleta os IDs dos pesquisados
    pesquisado_ids = [pesquisa.pesquisado_id for pesquisa in pesquisas]

    # Busca os usuários correspondentes aos pesquisado_ids
    usuarios = db.query(Usuario).filter(Usuario.id.in_(pesquisado_ids)).all()
    
    return usuarios