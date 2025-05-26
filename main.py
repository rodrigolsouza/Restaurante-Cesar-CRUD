from fastapi import FastAPI
from cardapio_misto import router as cardapio_router
from lixo.cardapio import *
from lixo.cardapio_mongo import *
from cardapio_misto import *
from fastapi.middleware.cors import CORSMiddleware



# ========================= Configuração do CORS =================================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique: ["http://127.0.0.1:5500"] se quiser mais seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================= Configuração do FastAPI(FrontEnd) =================================


# Conecta as rotas do cardápio
app.include_router(cardapio_router)

@app.get("/")
def home():
    return {"mensagem": "API do Restaurante está funcionando"}


# from ficha import *

# def menu_fichas():
#     while True:
#         fichas = carregar_fichas()
        
#         print("\n--- MENU FICHAS ---")
#         print("1. Adicionar Ficha")
#         print("2. Visualizar Fichas")
#         print("3. Editar Ficha")
#         print("4. Excluir Ficha")
#         print("0. Voltar")
        
#         opcao = input("Escolha uma opção: ")
        
#         if opcao == "1":
#             fichas = adicionar_ficha(fichas)
#         elif opcao == "2":
#             visualizar_fichas(fichas)
#         elif opcao == "3":
#             editar_fichas(fichas)
#         elif opcao == "4":
#             excluir_fichas(fichas)
#         elif opcao == "0":
#             return
#         else:
#             print("\nOpção inválida!")

def menu_cardapio():
    while True:
        while True:
            print("\n--- CARDÁPIO ---")
            print("1. Listar")
            print("2. Adicionar")
            print("3. Atualizar")
            print("4. Remover")
            print("5. Filtrar")
            print("0. Voltar")
            op = input("Escolha: ")

            if op == "1":
                listar_cardapio()
                break
            elif op == "2":
                adicionar_item()
                break
            elif op == "3":
                atualizar_item()
                break
            elif op == "4":
                remover_item()
                break
            elif op == "5":
                filtrar_por_categoria()
                break
            elif op == "0":
                break    
            else:
                print("Opção inválida.")
                break

        continuar = input("Deseja continuar? (s/n): ")
        if continuar.lower() == 'n':
            break
        else:
            continue

def main():
    while True:
        print("\n==== SISTEMA DO RESTAURANTE ====")
        print("1. Gerenciar Cardápio")
        print("2. Gerenciar Pedidos")
        print("3. Gerenciar Fichas Técnicas")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_cardapio()

        elif opcao == "2":
            # menu_pedidos()
            print("Funcionalidade de pedidos ainda não implementada.")
            break
        elif opcao == "3":
            # menu_fichas()
            print("Funcionalidade de fichas técnicas ainda não implementada.")
            break
        elif opcao == "0":
            print("Saindo do sistema.")
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
