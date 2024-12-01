import requests
import csv

# URL base da API
base_url = "https://wger.de/api/v2/exercise/"

# Parâmetros de consulta
params = {
    "language": 7,  # Código para português
    "limit": 20,    # Número de resultados por solicitação
    "offset": 0     # Começar do primeiro exercício
}

# Lista para armazenar os resultados
all_exercises = []

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(exercises):
    # Definir os cabeçalhos do CSV
    headers = ['id', 'name', 'description', 'category', 'license', 'license_author', 'muscles', 'equipment', 'author_history']
    
    # Abrir o arquivo CSV em modo de escrita
    with open('exercises_in_portuguese.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Escrever os cabeçalhos no CSV
        writer.writeheader()

        # Escrever os exercícios no CSV
        for exercise in exercises:
            writer.writerow({
                'id': exercise['id'],
                'name': exercise['name'],
                'description': exercise['description'],
                'category': exercise['category'],
                'license': exercise['license'],
                'license_author': exercise['license_author'],
                'muscles': ', '.join(map(str, exercise['muscles'])),
                'equipment': ', '.join(map(str, exercise['equipment'])),
                'author_history': ', '.join(exercise['author_history'])
            })

# Enviar solicitações até obter todos os exercícios
while True:
    # Fazendo a solicitação GET para a API
    response = requests.get(base_url, params=params)

    # Verificar se a resposta foi bem-sucedida (status 200)
    if response.status_code == 200:
        data = response.json()

        # Adicionar os resultados à lista
        all_exercises.extend(data['results'])

        # Verificar se há mais exercícios
        if data['next'] is None:
            break

        # Atualizar o offset para buscar a próxima página
        params['offset'] += 20
    else:
        print(f"Erro ao acessar a API. Status Code: {response.status_code}")
        break

# Exibir quantos exercícios foram encontrados
print(f"Total de exercícios encontrados: {len(all_exercises)}")

# Salvar todos os exercícios em um arquivo CSV
save_to_csv(all_exercises)

# Exibir alguns dos exercícios encontrados
for exercise in all_exercises[:5]:  # Exibe os primeiros 5 exercícios
    print(exercise['name'])
