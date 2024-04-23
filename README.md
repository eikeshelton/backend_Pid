# Configurando o Backend FastAPI

Este guia irá ajudá-lo a configurar um servidor FastAPI para o seu projeto.

## Pré-requisitos

- Python 3.6 ou superior
- PostgreSQL instalado

## Passos

1. **Crie e ative o ambiente virtual Crie um ambiente virtual Python.**
   **Obs: esse processo só precisa ser feito uma vez, se já tiver um ambiente virtual configurado, apenas inicialize ele, com o segundo comando abaixo:**

   ```bash
   python3 -m venv venv
   .\venv\Scripts\Activate

2. **Instale as dependências necessárias com o seguinte comando:**

      ```bash
      pip install -r requirements.txt

3. **Configure o banco de dados Substitua user, password e dbname pelas suas credenciais do PostgreSQL no arquivo app.py:**

      ```bash
      DATABASE_URL = "postgresql://user:password@localhost/dbname"

4. **Inicie o servidor Inicie o servidor FastAPI com o seguinte comando**

      ```bash
      uvicorn main:app --reload
