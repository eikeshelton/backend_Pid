import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.alimentos.alimentos import Alimento
from sqlalchemy.exc import SQLAlchemyError

# Conexão com o banco PostgreSQL
DATABASE_URL = "postgresql://esfs:999178058Eike@projetopid.cjs6ku6kun0r.us-east-1.rds.amazonaws.com/projeto_pid"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Carregar os dados do Excel usando pandas
file_path = 'C:/Users/ander/Downloads/Taco.xlsx'
df = pd.read_excel(file_path)
print(df.columns)

# Renomear as colunas do dataframe para combinar com os nomes da tabela do banco
df = df.rename(columns={
    'Número': 'id',
    'Grupo': 'grupo',
    'Descrição do Alimento': 'descricao',
    'Energia(kcal)': 'energia_kcal',
    'Proteína(g)': 'proteina_g',
    'Carboidrato(g)': 'carboidrato_g',
    'Lipídeos(g)' : 'lipideos_g'
})

def processar_valores(valor):
    if valor in ['Tr', 'NA', None]:
        return 0
    try:
        return round(float(valor), 2)
    except ValueError:
        return 0

# Inserir os dados no banco de dados
try:
    for index, row in df.iterrows():
        alimento = Alimento(
            id=row['id'],
            grupo=row['grupo'],
            descricao=row['descricao'],
            energia_kcal=processar_valores(row['energia_kcal']),
            proteina_g=processar_valores(row['proteina_g']),
            carboidrato_g=processar_valores(row['carboidrato_g']),
            lipideos_g=processar_valores(row['lipideos_g']),
            quantidade_g=None  # Será preenchido pelo usuário posteriormente
            )
        session.add(alimento)
    
    session.commit()
    print("Dados importados com sucesso!")
except SQLAlchemyError as e:
    session.rollback()
    print(f"Erro ao importar dados: {e}")
finally:
    session.close()
