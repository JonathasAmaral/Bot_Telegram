from pathlib import Path
from ..import ASSETS_DIR

# Define o caminho para assets específicos de fan wallet
FAN_WALLET_DIR = ASSETS_DIR / 'fan_wallet'

# Exporta os diretórios para serem usados em imports absolutos
__all__ = ['ASSETS_DIR', 'FAN_WALLET_DIR']