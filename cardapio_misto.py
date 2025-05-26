from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from typing import Optional
import json
import os
from pymongo import MongoClient

#=============================transformando em API(FRONTEND)=============================== 

router = APIRouter(prefix="/cardapio")


# ======================= Configuração da conexão(BANCO DE DADOS) ==========================
CONNECTION_STRING = "mongodb+srv://teste_restaurante:admin@clusterteste.vduediv.mongodb.net/?retryWrites=true&w=majority&appName=ClusterTeste"

client = MongoClient(CONNECTION_STRING)
db = client['restaurante_teste']           # Nome do database
collection = db['cardapio']          # Nome da collection

# ==================== Configuração do arquivo JSON(REPOSITÓRIO LOCAL) ===================

ARQUIVO_CARDAPIO = os.path.join(os.path.dirname(__file__), 'cardapio.json')



def carregar_cardapio():
    if not os.path.exists(ARQUIVO_CARDAPIO):
        with open(ARQUIVO_CARDAPIO, 'r', encoding='utf-8') as f:
            json.dump([], f, indent=4)
    with open(ARQUIVO_CARDAPIO, 'r' , encoding='utf-8') as f:
        return json.load(f)
    
def salvar_cardapio(cardapio):
    with open(ARQUIVO_CARDAPIO, 'w', encoding='utf-8') as f:
        json.dump(cardapio, f, indent=4, ensure_ascii=False)


# =========================== Definição do modelo de dados(FRONTEND) =========================
class Item(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    ingredientes: str
    preco: float
    categoria: str
    foto:str
# =========================== Funções de manipulação do cardápio(CRUD) ====================



# =========Funções auxiliares================================================================

def gerar_novo_id():
    # Carrega o cardápio atual do JSON
    cardapio = carregar_cardapio()

    # Busca o maior ID no JSON
    ids_json = [item['id'] for item in cardapio] if cardapio else []

    # Busca o maior ID no MongoDB
    ids_mongo = [doc.get('id') for doc in collection.find({}, {"id": 1})]
    ids_mongo = [id for id in ids_mongo if id is not None]

    # Calcula o maior ID encontrado
    maior_id = 0
    if ids_json:
        maior_id = max(maior_id, max(ids_json))
    if ids_mongo:
        maior_id = max(maior_id, max(ids_mongo))

    # Retorna o novo ID sequencial
    return maior_id + 1

# =========CREATE =========================================================================
@router.post("/")
def adicionar_item(item:Item):

    #ETAPA calculo do id sequencial
    cardapio = carregar_cardapio()
    novo_id= gerar_novo_id()

    # transformando o item(basel model) em dicionário e inserção do id calculado
    itemDB=item.model_dump()
    itemDB['id'] = novo_id
    
    #ETAPA Adicionar o item ao arquivo JSON
    cardapio.append(itemDB)
    salvar_cardapio(cardapio)

    #ETAPA Adicionar o item ao MongoDB
    result = collection.insert_one(itemDB)

    # Exibe o ID do item adicionado
    print(f"Item adicionado com sucesso! ID: {result.inserted_id}")
    
# =========READ ==========================================================================
@router.get("/")
def listar_cardapio():
    cardapio = list(collection.find({}, {"_id": 0}))
    return cardapio

@router.get("/categoria/{categoria}")
def filtrar_por_categoria(categoria: str):
    itens = list(collection.find({"categoria": categoria.lower()}, {"_id": 0}))
    if not itens:
        return {"mensagem": f"Não há itens na categoria '{categoria}'."}
    return itens

# =========UPDATE ==========================================================================
@router.put("/{id}")
def atualizar_item(id: int, item: Item):
    itemDB = item.model_dump()
    itemDB['id'] = id

    # Atualizar no MongoDB
    resultado = collection.update_one({"id": id}, {"$set": itemDB})

    if resultado.matched_count == 0:
        return {"mensagem": "Item não encontrado"}

    # Atualizar no JSON
    cardapio = carregar_cardapio()
    encontrado = False
    for idx, i in enumerate(cardapio):
        if i['id'] == id:
            cardapio[idx] = itemDB
            encontrado = True
            break
    if encontrado:
        salvar_cardapio(cardapio)
    else:
        return {"mensagem": "Item não encontrado no JSON"}

    return {"mensagem": "Item atualizado com sucesso"}

# =========DELETE ==========================================================================
@router.delete("/{id}")
def remover_item(id: int):
    # Deletar do MongoDB
    resultado = collection.delete_one({"id": id})

    # Deletar do JSON
    cardapio = carregar_cardapio()
    novo_cardapio = [i for i in cardapio if i['id'] != id]

    if len(cardapio) == len(novo_cardapio):
        return {"mensagem": "Item não encontrado"}

    salvar_cardapio(novo_cardapio)

    if resultado.deleted_count == 0:
        return {"mensagem": "Item não encontrado no MongoDB"}

    return {"mensagem": "Item excluído com sucesso"}

