
import json
import os

def carregar_dados(repositorio):
    if not os.path.exists(repositorio):
        return []
    
    with open(repositorio, 'r', encoding='utf-8') as file:
        return json.load(file)

def salvar_dados(repositorio, dados):
    with open(repositorio, 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)