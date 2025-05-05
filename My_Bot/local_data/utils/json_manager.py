# Gerenciador de operações JSON para os dados locais da FURIA

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("json-manager")

# Definição do caminho base para dados locais
BASE_LOCAL_DATA = Path(__file__).resolve().parent.parent / "data"

class JsonManager:
    """Classe para gerenciar operações com arquivos JSON de dados locais"""
    
    def __init__(self, base_path: Optional[Path] = None):
        # Inicializa o gerenciador de JSON
        if base_path is None:
            # Usa o diretório data como base
            self.base_path = BASE_LOCAL_DATA
        else:
            self.base_path = base_path
        
        logger.info(f"Inicializado JsonManager com diretório base: {self.base_path}")
    
    def get_file_path(self, game: str, data_type: str) -> Path:

        return self.base_path / game / f"{game}_{data_type}.json"
    
    def load(self, game: str, data_type: str) -> Optional[Union[Dict, List]]:
        
        # Carrega dados de um arquivo JSON

        file_path = self.get_file_path(game, data_type)
        
        if not file_path.exists():
            logger.warning(f"Arquivo não encontrado: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Dados carregados com sucesso: {file_path}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON do arquivo {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {file_path}: {e}")
            return None
    
    def save(self, game: str, data_type: str, data: Union[Dict, List]) -> bool:
    
    # Salva dados em um arquivo JSON
        
        # Verifica se o diretório existe e cria se necessário
        game_dir = self.base_path / game
        game_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = self.get_file_path(game, data_type)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Dados salvos com sucesso: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {file_path}: {e}")
            return False
    
    def get_games(self) -> List[str]:

        games = []
        for path in self.base_path.iterdir():
            if path.is_dir() and path.name not in ["utils", "__pycache__"]:
                games.append(path.name)
                
        logger.info(f"Jogos disponíveis: {games}")
        return games
        
    def get_data_types(self) -> List[str]:

        return ["team", "players", "upcoming_matches", "past_matches", "tournaments"]
