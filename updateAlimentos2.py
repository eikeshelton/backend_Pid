import requests
import csv

# URL base da API
base_url = "https://wger.de/api/v2/ingredient/"

# Parâmetros de consulta
params = {
    "language": 7,  # Código para português
    "limit": 20,     # Número de resultados por solicitação
    "offset": 0     # Começar do primeiro ingrediente
}

# Lista para armazenar os resultados
all_ingredients = []

# Função para salvar os resultados em um arquivo CSV
def save_to_csv(ingredients):
    # Definir os cabeçalhos do CSV
    headers = ['id', 'name', 'energy', 'protein', 'carbohydrates', 'carbohydrates_sugar', 'fat', 'fat_saturated', 'fiber', 'sodium', 'source_name', 'source_url']
    
    # Abrir o arquivo CSV em modo de escrita
    with open('ingredients.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Escrever os cabeçalhos no CSV
        writer.writeheader()

        # Escrever os ingredientes no CSV
        for ingredient in ingredients:
            writer.writerow({
                'id': ingredient['id'],
                'name': ingredient['name'],
                'energy': ingredient['energy'],
                'protein': ingredient['protein'],
                'carbohydrates': ingredient['carbohydrates'],
                'carbohydrates_sugar': ingredient['carbohydrates_sugar'],
                'fat': ingredient['fat'],
                'fat_saturated': ingredient['fat_saturated'],
                'fiber': ingredient['fiber'],
                'sodium': ingredient['sodium'],
                'source_name': ingredient['source_name'],
                'source_url': ingredient['source_url']
            })

# Enviar solicitações até obter todos os ingredientes
while True:
    # Fazendo a solicitação GET para a API
    response = requests.get(base_url, params=params)

    # Verificar se a resposta foi bem-sucedida (status 200)
    if response.status_code == 200:
        data = response.json()

        # Adicionar os resultados à lista
        all_ingredients.extend(data['results'])

        # Verificar se há mais ingredientes
        if data['next'] is None:
            break

        # Atualizar o offset para buscar a próxima página
        params['offset'] += 20  # Ajuste o valor conforme necessário
    else:
        print(f"Erro ao acessar a API. Status Code: {response.status_code}")
        break

# Exibir quantos ingredientes foram encontrados
print(f"Total de ingredientes encontrados: {len(all_ingredients)}")

# Salvar todos os ingredientes em um arquivo CSV
save_to_csv(all_ingredients)

# Exibir alguns dos ingredientes encontrados
for ingredient in all_ingredients[:5]:  # Exibe os primeiros 5 ingredientes
    print(ingredient['name'])
