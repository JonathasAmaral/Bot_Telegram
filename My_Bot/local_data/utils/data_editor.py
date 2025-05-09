# Classes para edição de tipos específicos de dados da FURIA

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Import usando caminho relativo para compatibilidade com o ambiente existente
from .json_manager import JsonManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("data-editor")

class BaseEditor:
    """Classe base para editores de dados"""
    
    def __init__(self, json_manager: JsonManager, game: str, data_type: str):

        self.json_manager = json_manager
        self.game = game
        self.data_type = data_type
        self.data = None
        
    def load(self) -> bool:

        self.data = self.json_manager.load(self.game, self.data_type)
        if self.data is None:
            # Se não conseguir carregar, inicializa com dados padrão
            self._init_default_data()
        return self.data is not None
    
    def save(self) -> bool:

        if self.data is None:
            logger.error("Tentativa de salvar dados que não foram carregados")
            return False
        
        return self.json_manager.save(self.game, self.data_type, self.data)
    
    def _init_default_data(self):
        """Inicializa dados padrão - deve ser sobrescrito pelas subclasses"""
        pass


class TeamEditor(BaseEditor):
    """Editor para informações do time"""
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "team")
    
    def _init_default_data(self):
        """Inicializa com dados padrão do time"""
        self.data = {
            "name": "FURIA",
            "country": "Brazil",
            "region": "Americas",
            "world_ranking": "N/A",
            "ranking": "N/A",
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat(),
            "acronym": "FURIA",
            "logo_url": ""
        }
    
    def edit_field(self, field: str, value: str) -> bool:

        if field not in self.data:
            logger.error(f"Campo inválido: {field}")
            return False
        
        # Atualizar timestamp de modificação
        if field not in ["created_at", "modified_at"]:
            self.data[field] = value
            self.data["modified_at"] = datetime.now().isoformat()
            logger.info(f"Campo {field} atualizado para {value}")
            return True
            
        return False


class PlayersEditor(BaseEditor):
    """Editor para lista de jogadores"""
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "players")
    
    def _init_default_data(self):
        """Inicializa com lista vazia de jogadores"""
        self.data = []
    
    def get_players(self) -> List[Dict]:

        if not self.data:
            return []
        return self.data
    
    def add_player(self, player_data: Dict) -> bool:

        # Gerar ID para o novo jogador se não estiver definido
        if "id" not in player_data:
            next_id = len(self.data) + 101  # Para csgo começa em 101, valorant em 201
            if self.game == "valorant":
                next_id += 100
            player_data["id"] = str(next_id)
        
        self.data.append(player_data)
        logger.info(f"Jogador {player_data.get('nickname')} adicionado com sucesso")
        return True
    
    def update_player(self, index: int, player_data: Dict) -> bool:

        if 0 <= index < len(self.data):
            # Preservar ID original
            original_id = self.data[index]["id"]
            player_data["id"] = original_id
            
            self.data[index] = player_data
            logger.info(f"Jogador {player_data.get('nickname')} atualizado com sucesso")
            return True
        else:
            logger.error(f"Índice de jogador inválido: {index}")
            return False
    
    def remove_player(self, index: int) -> Optional[Dict]:
        # Remove um jogador da lista

        if 0 <= index < len(self.data):
            removed_player = self.data.pop(index)
            logger.info(f"Jogador {removed_player.get('nickname')} removido com sucesso")
            return removed_player
        else:
            logger.error(f"Índice de jogador inválido: {index}")
            return None


class MatchesEditor(BaseEditor):
    """Classe base para editores de partidas"""
    
    def get_matches(self) -> List[Dict]:
        # Obtém a lista de partidas
        if not self.data:
            return []
        return self.data
    
    def add_match(self, match_data: Dict) -> bool:

        self.data.append(match_data)
        logger.info(f"Partida contra {match_data.get('opponent')} adicionada com sucesso")
        return True
    
    def update_match(self, index: int, match_data: Dict) -> bool:

        if 0 <= index < len(self.data):
            self.data[index] = match_data
            logger.info(f"Partida contra {match_data.get('opponent')} atualizada com sucesso")
            return True
        else:
            logger.error(f"Índice de partida inválido: {index}")
            return False
    
    def remove_match(self, index: int) -> Optional[Dict]:

        if 0 <= index < len(self.data):
            removed_match = self.data.pop(index)
            logger.info(f"Partida contra {removed_match.get('opponent')} removida com sucesso")
            return removed_match
        else:
            logger.error(f"Índice de partida inválido: {index}")
            return None
    
    def _init_default_data(self):
        """Inicializa com lista vazia de partidas"""
        self.data = []


class UpcomingMatchesEditor(MatchesEditor):
    # Editor para partidas futuras
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "upcoming_matches")


class PastMatchesEditor(MatchesEditor):
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "past_matches")


class TournamentsEditor(BaseEditor):
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "tournaments")
    
    def _init_default_data(self):
        self.data = []
    
    def get_tournaments(self) -> List[Dict]:

        if not self.data:
            return []
        return self.data
    
    def add_tournament(self, tournament_data: Dict) -> bool:

        self.data.append(tournament_data)
        logger.info(f"Torneio {tournament_data.get('name')} adicionado com sucesso")
        return True
    
    def update_tournament(self, index: int, tournament_data: Dict) -> bool:

        if 0 <= index < len(self.data):
            self.data[index] = tournament_data
            logger.info(f"Torneio {tournament_data.get('name')} atualizado com sucesso")
            return True
        else:
            logger.error(f"Índice de torneio inválido: {index}")
            return False
    
    def remove_tournament(self, index: int) -> Optional[Dict]:

        if 0 <= index < len(self.data):
            removed_tournament = self.data.pop(index)
            logger.info(f"Torneio {removed_tournament.get('name')} removido com sucesso")
            return removed_tournament
        else:
            logger.error(f"Índice de torneio inválido: {index}")
            return None