from .base import BaseScraper
from .team import TeamScraper
from .matches import MatchesScraper
from .tournaments import TournamentsScraper
from .players import PlayersScraper

class WebScraper:
    """Classe principal para gerenciar todos os scrapers"""
    
    def __init__(self):
        self._team = TeamScraper()
        self._matches = MatchesScraper()
        self._tournaments = TournamentsScraper()
        self._players = PlayersScraper()
        
    async def get_furia_games(self):
        """Retorna lista de jogos suportados"""
        return ["CS:GO", "VALORANT"]
        
    async def get_team_info(self, game):
        """Obtém informações do time"""
        return await self._team.get_info(game)
        
    async def get_team_players(self, game):
        """Obtém lista de jogadores"""
        return await self._players.get_players(game)
        
    async def get_upcoming_matches(self, game):
        """Obtém próximos jogos"""
        return await self._matches.get_upcoming(game)
        
    async def get_recent_results(self, game):
        """Obtém resultados recentes"""
        return await self._matches.get_results(game)
        
    async def get_recent_tournaments(self, game):
        """Obtém torneios recentes"""
        return await self._tournaments.get_recent(game)

# Instância global
scraper = WebScraper()