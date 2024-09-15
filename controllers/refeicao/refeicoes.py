# controllers/refeicao_controller.py
from sqlalchemy.orm import Session
from models.refeicao.refeicao import Refeicao
from models.refeicao_alimento.refeicao_alimento import RefeicaoAlimento
from models.alimento_usuario.alimento_usuario import *
from models.schema.schema import *
from datetime import date
from models.alimentos.alimentos import *



def adicionar_alimentos(alimento:AlimentoSchema, db: Session):
    alimento_usuario = AlimentoUsuario(
        id_usuario=alimento.id_usuario,
        id_alimento=alimento.alimento_id,
        quantidade_g=alimento.quantidade
    )

    db.add(alimento_usuario)
    db.commit()
    db.refresh(alimento_usuario)
    refeicoes_alimento = RefeicaoAlimento(
        id_refeicao= alimento.refeicao_id,
        id_usuario=alimento.id_usuario,
        id_alimento=alimento_usuario.id,
        data = date.today()
    )

    db.add(refeicoes_alimento)
    db.commit()
    db.refresh(refeicoes_alimento)
    return "feito"

def listar_refeicoes(usuario_id: int, data: date, db: Session):
    # Busca as refeições do usuário na data específica
    refeicoes_alimentos = db.query(RefeicaoAlimento).filter(
        RefeicaoAlimento.id_usuario == usuario_id,
        RefeicaoAlimento.data == data
    ).all()

    total_energia_kcal = 0
    total_proteina_g = 0
    total_carboidrato_g = 0
    total_lipideos_g = 0

    # Percorre cada alimento na lista de refeições
    for refeicao_alimento in refeicoes_alimentos:
        # Busca a relação do alimento do usuário para obter a quantidade
        alimento_usuario = db.query(AlimentoUsuario).filter(
            AlimentoUsuario.id == refeicao_alimento.id_alimento
        ).first()

        # Verifica se encontrou o alimento na tabela do usuário
        if alimento_usuario:
            quantidade_g = alimento_usuario.quantidade_g

            # Busca o alimento na tabela de alimentos gerais
            alimento = db.query(Alimento).filter(
                Alimento.id == alimento_usuario.id_alimento
            ).first()

            # Calcula os totais com base na quantidade e valores nutricionais do alimento
            if alimento:
                
                
                
                total_energia_kcal += (alimento.energia_kcal * quantidade_g) / 100
                total_proteina_g += (alimento.proteina_g * quantidade_g) / 100
                total_carboidrato_g += (alimento.carboidrato_g * quantidade_g) / 100
                total_lipideos_g += (alimento.lipideos_g * quantidade_g) / 100

    return RefeicaoResponseList (
        total_energia_kcal=total_energia_kcal,
        total_proteina_g=total_proteina_g,
        total_carboidrato_g=total_carboidrato_g,
        total_lipideos_g=total_lipideos_g
    )
    

def buscar_info_alimento(buscarAlimento, db: Session):
    # Passo 1: Buscar na tabela RefeicaoAlimento usando o id_usuario e data fornecidos
    refeicoes_alimentos = db.query(RefeicaoAlimento).filter(
        RefeicaoAlimento.id_usuario == buscarAlimento.id_usuario,
        RefeicaoAlimento.data == buscarAlimento.data
    ).all()
    
    
    # Passo 2: Obter os ids_alimentos da tabela RefeicaoAlimento
    ids_alimentos = [item.id_alimento for item in refeicoes_alimentos]
    ids_refeicao = [item.id_refeicao for item in refeicoes_alimentos]
    
    
    # Passo 3: Buscar na tabela AlimentoUsuario usando os ids_alimentos
    alimentos_usuario = db.query(AlimentoUsuario).filter(
        AlimentoUsuario.id.in_(ids_alimentos)
    ).all()
    
    
    ids_alimentos_usuario = [item.id_alimento for item in alimentos_usuario]
    
    # Criar um dicionário para acessar rapidamente os alimentos do usuário
    alimentos_usuario_map = {item.id: item for item in alimentos_usuario}
    
    # Passo 4: Buscar na tabela Alimento usando os ids_alimentos
    alimentos = db.query(Alimento).filter(
        Alimento.id.in_(ids_alimentos_usuario)
    ).all()
    
    
    # Criar um dicionário para acessar rapidamente os detalhes dos alimentos
    alimentos_map = {item.id: item for item in alimentos}
    
    # Construir o resultado final associando os alimentos com as refeições
    result = []
    for refeicao_alimento in refeicoes_alimentos:
        alimento_usuario = alimentos_usuario_map.get(refeicao_alimento.id_alimento)
        
        if alimento_usuario is None:
            print(f"Alimento usuário não encontrado para id_alimento {refeicao_alimento.id_alimento}")
            continue
        
        alimento = alimentos_map.get(alimento_usuario.id_alimento)
        
        if alimento is None:
            print(f"Alimento não encontrado para id_alimento {alimento_usuario.id_alimento}")
            continue
        
        result.append({
            "id_refeicao": refeicao_alimento.id_refeicao,
            "alimento_usuario_id": alimento_usuario.id,
            "id_alimento": alimento_usuario.id_alimento,
            "calories": (alimento.energia_kcal * alimento_usuario.quantidade_g) / 100,
            "id": alimento.id,
            "carbs": (alimento.carboidrato_g * alimento_usuario.quantidade_g) / 100,
            "grams": alimento_usuario.quantidade_g,
            "name": alimento.descricao,
            "protein": (alimento.proteina_g * alimento_usuario.quantidade_g) / 100,
            "fats": (alimento.lipideos_g * alimento_usuario.quantidade_g) / 100
        })
    
    
    return result




