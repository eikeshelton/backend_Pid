# controllers/exercicio_personalizado_controller.py
from sqlalchemy.orm import Session
from models.exercicio.exercicio_personalizado import ExercicioPersonalizado
from fastapi import HTTPException
import requests

# Função para buscar um exercício no banco de dados pelo ID
def buscar_exercicio_banco(db: Session, exercicio_id: int):
    db_exercicio = db.query(ExercicioPersonalizado).filter(ExercicioPersonalizado.id == exercicio_id).first()
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado no banco")
    return db_exercicio

# Função para buscar todos os exercícios do banco
def buscar_exercicios_banco(db: Session):
    return db.query(ExercicioPersonalizado).all()

# Função para buscar dados do exercício por nome
def buscar_exercicios_por_nome(db: Session, nome_exercicio: str):
    exercicios = db.query(ExercicioPersonalizado).filter(
        ExercicioPersonalizado.nome_exercicio.ilike(f"%{nome_exercicio}%")
    ).all()

    if not exercicios:
        raise HTTPException(status_code=404, detail="Nenhum exercício encontrado com esse nome")

    return exercicios

# Função para buscar todos os exercícios na API externa
def buscar_exercicios_api():
    url = "https://wger.de/api/v2/exercise/"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Erro ao buscar exercícios na API externa")
    return response.json()

# Função para criar um exercício personalizado
def criar_exercicio_personalizado(db: Session, exercicio):
    db_exercicio = ExercicioPersonalizado(
        treinamento_id=exercicio.treinamento_id,
        api_exercicio_id=exercicio.api_exercicio_id,
        nome_exercicio=exercicio.nome_exercicio,
        notas=exercicio.notas,
        repeticoes=exercicio.repeticoes,
        series=exercicio.series,
        carga_kg=exercicio.carga_kg,
        tempo_descanso_seg=exercicio.tempo_descanso_seg
    )
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

# Função para atualizar um exercício personalizado
def atualizar_exercicio_personalizado(db: Session, exercicio_id: int, exercicio):
    db_exercicio = db.query(ExercicioPersonalizado).filter(ExercicioPersonalizado.id == exercicio_id).first()
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    db_exercicio.nome_exercicio = exercicio.nome_exercicio
    db_exercicio.notas = exercicio.notas
    db_exercicio.repeticoes = exercicio.repeticoes
    db_exercicio.series = exercicio.series
    db_exercicio.carga_kg = exercicio.carga_kg
    db_exercicio.tempo_descanso_seg = exercicio.tempo_descanso_seg

    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

# Função para deletar um exercício personalizado
def deletar_exercicio_personalizado(db: Session, exercicio_id: int):
    db_exercicio = db.query(ExercicioPersonalizado).filter(ExercicioPersonalizado.id == exercicio_id).first()
    if db_exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    db.delete(db_exercicio)
    db.commit()
    return {"msg": "Exercício deletado com sucesso"}