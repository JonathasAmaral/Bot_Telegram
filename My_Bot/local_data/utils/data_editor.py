"""
Classes para edição de tipos específicos de dados da FURIA
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from .json_manager import JsonManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("data-editor")

class BaseEditor:
    """Classe base para editores de dados"""
    
    def __init__(self, json_manager: JsonManager, game: str, data_type: str):
        """
        Inicializa o editor de dados
        
        Args:
            json_manager: Instância do gerenciador de JSON
            game: Nome do jogo (csgo, valorant)
            data_type: Tipo de dados a ser editado
        """
        self.json_manager = json_manager
        self.game = game
        self.data_type = data_type
        self.data = None
        
    def load(self) -> bool:
        """
        Carrega os dados do arquivo JSON
        
        Returns:
            bool: True se os dados foram carregados com sucesso
        """
        self.data = self.json_manager.load(self.game, self.data_type)
        if self.data is None:
            # Se não conseguir carregar, inicializa com dados padrão
            self._init_default_data()
        return self.data is not None
    
    def save(self) -> bool:
        """
        Salva os dados no arquivo JSON
        
        Returns:
            bool: True se os dados foram salvos com sucesso
        """
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
        """
        Edita um campo específico das informações do time
        
        Args:
            field: Nome do campo a ser editado
            value: Novo valor para o campo
            
        Returns:
            bool: True se a edição foi bem-sucedida
        """
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
        """
        Retorna a lista de jogadores
        
        Returns:
            List[Dict]: Lista de jogadores
        """
        if not self.data:
            return []
        return self.data
    
    def add_player(self, player_data: Dict) -> bool:
        """
        Adiciona um novo jogador
        
        Args:
            player_data: Dicionário com dados do jogador
            
        Returns:
            bool: True se o jogador foi adicionado com sucesso
        """
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
        """
        Atualiza um jogador existente
        
        Args:
            index: Índice do jogador na lista
            player_data: Novos dados do jogador
            
        Returns:
            bool: True se o jogador foi atualizado com sucesso
        """
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
        """
        Remove um jogador
        
        Args:
            index: Índice do jogador na lista
            
        Returns:
            Optional[Dict]: Dados do jogador removido ou None se falhou
        """
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
        """
        Retorna a lista de partidas
        
        Returns:
            List[Dict]: Lista de partidas
        """
        if not self.data:
            return []
        return self.data
    
    def add_match(self, match_data: Dict) -> bool:
        """
        Adiciona uma nova partida
        
        Args:
            match_data: Dicionário com dados da partida
            
        Returns:
            bool: True se a partida foi adicionada com sucesso
        """
        self.data.append(match_data)
        logger.info(f"Partida contra {match_data.get('opponent')} adicionada com sucesso")
        return True
    
    def update_match(self, index: int, match_data: Dict) -> bool:
        """
        Atualiza uma partida existente
        
        Args:
            index: Índice da partida na lista
            match_data: Novos dados da partida
            
        Returns:
            bool: True se a partida foi atualizada com sucesso
        """
        if 0 <= index < len(self.data):
            self.data[index] = match_data
            logger.info(f"Partida contra {match_data.get('opponent')} atualizada com sucesso")
            return True
        else:
            logger.error(f"Índice de partida inválido: {index}")
            return False
    
    def remove_match(self, index: int) -> Optional[Dict]:
        """
        Remove uma partida
        
        Args:
            index: Índice da partida na lista
            
        Returns:
            Optional[Dict]: Dados da partida removida ou None se falhou
        """
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
    """Editor para próximas partidas"""
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "upcoming_matches")


class PastMatchesEditor(MatchesEditor):
    """Editor para resultados de partidas"""
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "past_matches")


class TournamentsEditor(BaseEditor):
    """Editor para torneios"""
    
    def __init__(self, json_manager: JsonManager, game: str):
        super().__init__(json_manager, game, "tournaments")
    
    def _init_default_data(self):
        """Inicializa com lista vazia de torneios"""
        self.data = []
    
    def get_tournaments(self) -> List[Dict]:
        """
        Retorna a lista de torneios
        
        Returns:
            List[Dict]: Lista de torneios
        """
        if not self.data:
            return []
        return self.data
    
    def add_tournament(self, tournament_data: Dict) -> bool:
        """
        Adiciona um novo torneio
        
        Args:
            tournament_data: Dicionário com dados do torneio
            
        Returns:
            bool: True se o torneio foi adicionado com sucesso
        """
        self.data.append(tournament_data)
        logger.info(f"Torneio {tournament_data.get('name')} adicionado com sucesso")
        return True
    
    def update_tournament(self, index: int, tournament_data: Dict) -> bool:
        """
        Atualiza um torneio existente
        
        Args:
            index: Índice do torneio na lista
            tournament_data: Novos dados do torneio
            
        Returns:
            bool: True se o torneio foi atualizado com sucesso
        """
        if 0 <= index < len(self.data):
            self.data[index] = tournament_data
            logger.info(f"Torneio {tournament_data.get('name')} atualizado com sucesso")
            return True
        else:
            logger.error(f"Índice de torneio inválido: {index}")
            return False
    
    def remove_tournament(self, index: int) -> Optional[Dict]:
        """
        Remove um torneio
        
        Args:
            index: Índice do torneio na lista
            
        Returns:
            Optional[Dict]: Dados do torneio removido ou None se falhou
        """
        if 0 <= index < len(self.data):
            removed_tournament = self.data.pop(index)
            logger.info(f"Torneio {removed_tournament.get('name')} removido com sucesso")
            return removed_tournament
        else:
            logger.error(f"Índice de torneio inválido: {index}")
            return None