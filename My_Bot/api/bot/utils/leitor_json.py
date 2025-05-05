import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("telegram-bot")

from My_Bot.local_data.data import BASE_DATA_PATH

if 'BASE_DATA_PATH' not in locals():
    BASE_DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent / "local_data" / "data"

logger.info(f"Diretório base de dados: {BASE_DATA_PATH}")

class JsonDataReader:
    
    def __init__(self):
        # Initialize cache for storing loaded data
        self.cache = {}
        
    def _normalize_game_name(self, game: str) -> str:
        # Normalize game name for file path and cache consistency
        game_lower = game.lower()
        
        if game_lower == "cs:go" or game_lower == "cs2" or game_lower == "counter-strike 2":
            return "csgo"
        if game_lower == "league of legends":
            return "leagueoflegends"
        if game_lower == "rainbow six" or game_lower == "rainbow six siege":
            return "rainbowsix"
        if game_lower == "rocket league":
            return "rocketleague"
        if game_lower == "super smash bros" or game_lower == "super smash bros. ultimate" or game_lower == "super smash bros ultimate":
            return "smashbros"
        if game_lower == "apex legends":
            return "apexlegends"
        if game_lower == "free fire":
            return "freefile"
        # Remove any special characters for other games
        return game_lower.replace(":", "").replace(" ", "")
        
    def _get_file_path(self, game: str, data_type: str) -> Path:
        # Get the path for a specific game and data type JSON file
        normalized_game = self._normalize_game_name(game)
        filename = f"{normalized_game}_{data_type}.json"
        file_path = BASE_DATA_PATH / normalized_game / filename
        logger.info(f"Caminho do arquivo para {game}: {file_path} (existe: {file_path.exists()})")
        return file_path
        
    def _load_json_file(self, file_path: Path) -> Any:

        if not file_path.exists():
            logger.error(f"JSON file not found: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Arquivo JSON carregado com sucesso: {file_path}")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def _get_cached_or_load(self, game: str, data_type: str) -> Any:
        # Get data from cache or load it from file"""
        normalized_game = self._normalize_game_name(game)
        cache_key = f"{normalized_game}_{data_type}"
        logger.info(f"Buscando dados para cache_key: {cache_key}")
        
        # Return from cache if available
        if cache_key in self.cache:
            logger.info(f"Dados encontrados no cache para {cache_key}")
            return self.cache[cache_key]
        
        # Load from file if not in cache
        file_path = self._get_file_path(game, data_type)
        data = self._load_json_file(file_path)
        
        # Update cache
        if data is not None:
            self.cache[cache_key] = data
            logger.info(f"Dados adicionados ao cache para {cache_key}")
            
        return data
    
    def get_team_info(self, game: str) -> Dict[str, Any]:
        # Get team information for a specific game
        data = self._get_cached_or_load(game, "team")
        if not data:
            # Return default values if file not found
            return {
                "name": "FURIA",
                "country": "Brazil",
                "region": "Americas",
                "world_ranking": "N/A",
                "ranking": "N/A"
            }
        return data
    
    def get_players(self, game: str) -> List[Dict[str, str]]:

        data = self._get_cached_or_load(game, "players")
        if not data:
            return []
        return data
    
    def get_upcoming_matches(self, game: str) -> List[Dict[str, str]]:

        data = self._get_cached_or_load(game, "upcoming_matches")
        if not data:
            return []
        return data
    
    def get_past_matches(self, game: str) -> List[Dict[str, str]]:

        data = self._get_cached_or_load(game, "past_matches")
        if not data:
            return []
        return data
    
    def get_tournaments(self, game: str) -> List[Dict[str, str]]:
        data = self._get_cached_or_load(game, "tournaments")
        if not data:
            return []
        return data
    
    def get_supported_games(self) -> List[str]:
        # Get list of supported games by checking available subfolders"""
        # Return the specific list of games requested
        return [
            "Counter-Strike 2",
            "VALORANT",
            "League of Legends", 
            "Rocket League",
            "Rainbow Six Siege",
            "PUBG",
            "Apex Legends",
            "Free Fire",
            "Super Smash Bros. Ultimate"
        ]
    
    def clear_cache(self, game: Optional[str] = None):
        
        if game:
            # Clear cache for specific game
            normalized_game = self._normalize_game_name(game)
            for key in list(self.cache.keys()):
                if key.startswith(normalized_game):
                    del self.cache[key]
        else:
    
            self.cache = {}

# Create a single instance to be used throughout the application
json_reader = JsonDataReader()