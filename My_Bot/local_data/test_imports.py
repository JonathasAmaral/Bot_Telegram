"""
Arquivo de teste para verificar se as importações funcionam corretamente
após a refatoração do diretório utils.
"""

import os
import sys
from pathlib import Path

print("=== Teste de importações do pacote utils ===")
print(f"Diretório atual: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    from utils.json_manager import JsonManager
    print("✓ Importação do JsonManager bem-sucedida!")
except Exception as e:
    print(f"❌ Erro ao importar JsonManager: {e}")

try:
    from utils.data_editor import TeamEditor, PlayersEditor
    print("✓ Importação do TeamEditor e PlayersEditor bem-sucedida!")
except Exception as e:
    print(f"❌ Erro ao importar editores de dados: {e}")

print("\nTeste concluído!")