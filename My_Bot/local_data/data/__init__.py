from pathlib import Path

# Define o caminho base para os arquivos de dados
BASE_DATA_PATH = Path(__file__).resolve().parent

# Exporta BASE_DATA_PATH para ser usado em imports absolutos
__all__ = ['BASE_DATA_PATH']