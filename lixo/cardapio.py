# ====================================RODRIGO COMMIT 1========================================
import json
import os


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


#=====================================CAIO COMMIT 1======================================== 

def adicionar_item():
    cardapio = carregar_cardapio()
    novo_item = {
        'id': len(cardapio) + 1,
        'nome': input("Nome do prato/bebida: "),
        'descricao': input("Descrição: "),
        'ingredientes': input("Ingredientes (separados por vírgula): "),
        'preco': float(input("Preço: R$ ").replace(',', '.')),
        'categoria': input("Categoria (entrada, prato principal, sobremesa, bebida): ").lower()

    }
    cardapio.append(novo_item)
    salvar_cardapio(cardapio)
    print("Item adicionado com sucesso!")

# =====================================CAIO COMMIT 2========================================
def listar_cardapio():
    cardapio = carregar_cardapio()
    if not cardapio:
        print("Cardápio vazio.")
    else:
        print("\nCARDÁPIO ATUAL:")
        for item in cardapio:
            print("-" * 40)
            print(f"ID: {item['id']}")
            print(f"Nome: {item['nome']}")
            print(f"Descrição: {item['descricao']}")
            print(f"Ingredientes: {item['ingredientes']}")
            print(f"Preço: R${item['preco']:.2f}")
            print(f"Categoria: {item['categoria']}")


def filtrar_por_categoria():
    cardapio = carregar_cardapio()
    categoria = input("Digite a categoria: ").lower()
    filtrados = [p for p in cardapio if p['categoria'].lower() == categoria]
    if filtrados:
        print("Produtos na categoria:", categoria)
        for p in filtrados:
            print(f"{p['nome']} - R${p['preco']:.2f}")
    else:
        print("Nenhum produto nessa categoria.")   

# =====================================RODRIGO COMMIT 2========================================
def atualizar_item():
    cardapio = carregar_cardapio()
    id_item = int(input("Informe o ID do item que deseja atualizar: "))
    for item in cardapio:
        if item['id'] == id_item:
            print(">>>Deixei em branco para manter o valor atual<<<")
            nome = input(f"Novo nome {item['nome']}: ") or item['nome']
            descricao = input(f"Nova descrição ({item['descricao']}): ") or item['descricao']
            ingredientes = input(f"Novo ingrediente ({item['ingredientes']}): ") or item['ingredientes']
            preco_input = input(f"Novo preço ({item['preco']}): ")
            preco = float(preco_input) if preco_input else item['preco']
            categoria = input(f"Nova categoria ({item['categoria']}): ") or item['categoria']

            item.update({
                'nome': nome,
                'descricao': descricao,
                'ingredientes': ingredientes,
                'preco': preco,
                'categoria': categoria
            })
            salvar_cardapio(cardapio)
            print("Item atualizado com sucesso!")
            return
    print("Item não encontrado.")

# =====================================RODRIGO COMMIT 3========================================
def remover_item():
    cardapio = carregar_cardapio()
    id_item = int(input("Digite o ID do item que deseja remover: "))
    for item in cardapio:
        if item['id'] == id_item:
            cardapio.remove(item)
            salvar_cardapio(cardapio)
            print("Item removido com sucesso!")
            return