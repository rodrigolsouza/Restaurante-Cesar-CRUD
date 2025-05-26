
from pymongo import MongoClient

# ==== Configuração da conexão ======================
CONNECTION_STRING = "mongodb+srv://teste_restaurante:admin@clusterteste.vduediv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterTeste"

client = MongoClient(CONNECTION_STRING)
db = client['restaurante_teste']           # Nome do database
collection = db['cardapio']          # Nome da collection


def adicionar_item_mongo():
    nome = input("Nome do prato/bebida: ")
    descricao = input("Descrição: ")
    ingredientes = input("Ingredientes (separados por vírgula): ")
    preco = float(input("Preço: R$ ").replace(',', '.'))
    categoria = input("Categoria (entrada, prato principal, sobremesa, bebida): ").lower()

    novo_item = {
        'nome': nome,
        'descricao': descricao,
        'ingredientes': ingredientes,
        'preco': preco,
        'categoria': categoria
    }

    result = collection.insert_one(novo_item)
    print(f"Item adicionado com sucesso! ID: {result.inserted_id}")