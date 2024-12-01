import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.exercicio.exercicio import Exercicio  # Certifique-se de importar o modelo Exercicio

# Caminho do arquivo CSV
csv_file_path = "C:\\Users\\ander\\Downloads\\csv_combinado.csv"

# Lendo o arquivo CSV
df = pd.read_csv(csv_file_path)

# Verifique se as colunas essenciais estão presentes
if 'nome' not in df.columns or 'descricao' not in df.columns:
    raise ValueError("O CSV precisa ter as colunas 'nome' e 'descricao'.")

# Conexão com o banco de dados
DATABASE_URL = "postgresql://esfs:999178058Eike@projetopid.cjs6ku6kun0r.us-east-1.rds.amazonaws.com/projeto_pid"
engine = create_engine(DATABASE_URL)

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo os dados do CSV na tabela 'exercicios'
for index, row in df.iterrows():
    exercicio = Exercicio(nome=row['nome'], descricao=row['descricao'])
    session.add(exercicio)

# Comitando as alterações no banco
session.commit()
session.close()

print("Dados inseridos com sucesso!")
