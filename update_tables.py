import requests
import psycopg2

def fetch_and_store_states(cursor):
    response = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    states = response.json()

    for state in states:
        cursor.execute("""
            INSERT INTO estado (nome, sigla, codigo_ibge)
            VALUES (%s, %s, %s)
            ON CONFLICT (codigo_ibge) DO NOTHING
        """, (state['nome'], state['sigla'], state['id']))

def fetch_and_store_cities(cursor):
    cursor.execute("SELECT codigo_ibge, sigla FROM estado")
    states = cursor.fetchall()

    for state in states:
        state_id, state_sigla = state
        response = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_sigla}/municipios")
        cities = response.json()

        for city in cities:
            cursor.execute("""
                INSERT INTO municipio (nome, codigo_ibge, estado_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (codigo_ibge) DO NOTHING
            """, (city['nome'], city['id'], state_id))

def main():
    connection = psycopg2.connect(
        dbname="projeto_pid",
        user="esfs",
        password="999178058Eike",
        host="projetopid.cjs6ku6kun0r.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cursor = connection.cursor()

    fetch_and_store_states(cursor)
    fetch_and_store_cities(cursor)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
