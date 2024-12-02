from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.treinamento.treinamento import Treinamento as ModeloTreinamento  # Assumindo que a model do treinamento está em models/treinamento
from models.schema.schema import TreinamentoCreate  # Schema de entrada para criação de treinamento
from models.exercicio.exercicio_personalizado import ExercicioPersonalizado  # Para acessar os exercícios do banco de dados
from controllers.exercicios.exercicios import criar_exercicio_personalizado

# Função para buscar um treinamento específico no banco de dados
def buscar_treinamento_banco(db: Session, treinamento_id: int):
    db_treinamento = db.query(ModeloTreinamento).filter(ModeloTreinamento.id == treinamento_id).first()
    if db_treinamento is None:
        raise HTTPException(status_code=404, detail="Treinamento não encontrado")
    
    # Buscando os IDs dos exercícios relacionados ao treinamento
    db_treinamento.exercicios = [exercicio.id for exercicio in db_treinamento.exercicios]
    return db_treinamento

def buscar_treinamentos_por_usuario(usuario_id: int, db: Session):

    treinamentos = db.query(ModeloTreinamento).filter(ModeloTreinamento.usuario_id == usuario_id).all()

    if not treinamentos:
        raise HTTPException(status_code=404, detail="Nenhum treinamento encontrado para este usuário")

    return treinamentos

def atualizar_treinamento(db: Session, treinamento_id: int, treinamento):
    db_treinamento = db.query(ModeloTreinamento).filter(ModeloTreinamento.id == treinamento_id).first()
    if db_treinamento is None:
        raise HTTPException(status_code=404, detail="Treinamento não encontrado")

    # Atualizando campos fornecidos
    if treinamento.nome:
        db_treinamento.nome = treinamento.nome
    if treinamento.descricao:
        db_treinamento.descricao = treinamento.descricao
    if treinamento.dia_da_semana:
        db_treinamento.dia_da_semana = treinamento.dia_da_semana

    db.commit()
    db.refresh(db_treinamento)
    return db_treinamento

# Função para buscar todos os treinamentos no banco de dados
def buscar_treinamentos_banco(db: Session):
    return db.query(ModeloTreinamento).all()

# Função para criar um novo treinamento no banco de dados
def criar_treinamento(db: Session, treinamento: TreinamentoCreate):
    # Criar o treinamento
    db_treinamento = ModeloTreinamento(
        nome=treinamento.nome,
        usuario_id=treinamento.usuario_id,
        descricao=treinamento.descricao,
        dia_semana=treinamento.dia_da_semana
    )
    db.add(db_treinamento)
    db.commit()
    db.refresh(db_treinamento)

    # Criar os exercícios personalizados associados
    for exercicio in treinamento.exercicios:
        criar_exercicio_personalizado(
            db=db,
            exercicio={
                "treinamento_id": db_treinamento.id,
                "api_exercicio_id": exercicio.api_exercicio_id,  # Se não existir integração, pode ser None
                "nome_exercicio": exercicio.nome,
                "notas": exercicio.notas,  # Pode ser adicionado se necessário
                "repeticoes": exercicio.repeticoes,
                "series": exercicio.series,
                "carga_kg": exercicio.carga,
                "tempo_descanso_seg": exercicio.tempoDescanso
            }
        )

    return db_treinamento

    # Criar os exercícios personalizados associados
    for exercicio in treinamento.exercicios:
        criar_exercicio_personalizado(
            db=db,
            exercicio={
                "treinamento_id": db_treinamento.id,
                "api_exercicio_id": exercicio.api_exercicio_id,  # Se não existir integração, pode ser None
                "nome_exercicio": exercicio.nome,
                "notas": exercicio.notas,  # Pode ser adicionado se necessário
                "repeticoes": exercicio.repeticoes,
                "series": exercicio.series,
                "carga_kg": exercicio.carga,
                "tempo_descanso_seg": exercicio.tempoDescanso
            }
        )

    return db_treinamento

# Função para excluir um treinamento no banco de dados
def excluir_treinamento(db: Session, treinamento_id: int):
    db_treinamento = db.query(ModeloTreinamento).filter(ModeloTreinamento.id == treinamento_id).first()
    if db_treinamento is None:
        raise HTTPException(status_code=404, detail="Treinamento não encontrado")
    
    db.delete(db_treinamento)
    db.commit()
    return db_treinamento

