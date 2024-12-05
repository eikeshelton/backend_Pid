from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.treinamento.treinamento import Treinamento 
from models.schema.schema import TreinamentoCreate  # Schema de entrada para criação de treinamento
from models.exercicio.exercicio_personalizado import ExercicioPersonalizado  # Para acessar os exercícios do banco de dados
from controllers.exercicios.exercicios import criar_exercicio_personalizado
from models.exercicio.exercicio import Exercicio

# Função para buscar um treinamento específico no banco de dados
def buscar_treinamento_banco(db: Session, treinamento_id: int):
    db_treinamento = db.query(Treinamento).filter(Treinamento.id == treinamento_id).first()
    if db_treinamento is None:
        raise HTTPException(status_code=404, detail="Treinamento não encontrado")
    
    # Buscando os IDs dos exercícios relacionados ao treinamento
    db_treinamento.exercicios = [exercicio.id for exercicio in db_treinamento.exercicios]
    return db_treinamento

def buscar_treinamentos_por_usuario(usuario_id: int, db: Session):
    # Buscar treinamentos associados ao usuário
    treinamentos = db.query(Treinamento).filter(Treinamento.usuario_id == usuario_id).all()

    if not treinamentos:
        raise HTTPException(status_code=404, detail="Nenhum treinamento encontrado para este usuário")

    # Obter os IDs dos treinamentos encontrados
    treinamento_ids = [treinamento.id for treinamento in treinamentos]

    # Buscar exercícios personalizados associados aos IDs dos treinamentos
    exercicios_personalizados = (
        db.query(ExercicioPersonalizado)
        .filter(ExercicioPersonalizado.treinamento_id.in_(treinamento_ids))
        .all()
    )

    if not exercicios_personalizados:
        raise HTTPException(status_code=404, detail="Nenhum exercício personalizado encontrado")

    # Obter os IDs dos exercícios
    exercicio_ids = [exercicio.api_exercicio_id for exercicio in exercicios_personalizados]

    # Buscar descrições dos exercícios na tabela Exercicios
    exercicios_base = (
        db.query(Exercicio)
        .filter(Exercicio.id.in_(exercicio_ids))
        .all()
    )

    # Criar um dicionário para mapear id -> descrição
    exercicio_descricao_map = {exercicio.id: exercicio.descricao for exercicio in exercicios_base}

    # Mapear os exercícios personalizados para seus respectivos treinamentos
    treinamentos_com_detalhes = []
    for treinamento in treinamentos:
        exercicios_associados = []
        for exercicio_personalizado in exercicios_personalizados:
            if exercicio_personalizado.treinamento_id == treinamento.id:
                # Adiciona a descrição diretamente no objeto de exercício personalizado
                exercicio_personalizado.descricao = exercicio_descricao_map.get(
                    exercicio_personalizado.api_exercicio_id, "Descrição não encontrada"
                )
                # Remove os campos `api_exercicio_id` e `treinamento_id`
                del exercicio_personalizado.api_exercicio_id
                del exercicio_personalizado.treinamento_id
                exercicios_associados.append(exercicio_personalizado)

        treinamentos_com_detalhes.append({
            "treinamento": treinamento,
            "exercicios": exercicios_associados
        })

    return treinamentos_com_detalhes




def atualizar_treinamento(db: Session, treinamento_id: int, treinamento):
    db_treinamento = db.query(Treinamento).filter(Treinamento.id == treinamento_id).first()
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
    return db.query(Treinamento).all()

# Função para criar um novo treinamento no banco de dados
def criar_treinamento(db: Session, treinamento: TreinamentoCreate,id_usuario):
    # Criar o treinamento
    db_treinamento = Treinamento(
        nome=treinamento.nome,
        usuario_id=id_usuario,
        descricao=treinamento.descricao,
        dia_da_semana=treinamento.dia_da_semana
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
                "api_exercicio_id": exercicio.id_exercicio,  # Se não existir integração, pode ser None
                "nome_exercicio": exercicio.nome,
                "notas": exercicio.nota,  # Pode ser adicionado se necessário
                "repeticoes": exercicio.repeticoes,
                "series": exercicio.series,
                "carga_kg": exercicio.carga,
                "tempo_descanso_seg": exercicio.tempoDescanso
            }
        )

    return db_treinamento

# Função para excluir um treinamento no banco de dados
def excluir_treinamento(db: Session, treinamento_id: int):
    db_treinamento = db.query(Treinamento).filter(Treinamento.id == treinamento_id).first()
    if db_treinamento is None:
        raise HTTPException(status_code=404, detail="Treinamento não encontrado")
    
    db.delete(db_treinamento)
    db.commit()
    return db_treinamento

