from pathlib import Path

# Define o caminho base para os assets
ASSETS_DIR = Path(__file__).resolve().parent

# Exporta o diretório de assets
__all__ = ['ASSETS_DIR']