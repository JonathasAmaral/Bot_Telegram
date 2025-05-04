from .base import BaseScraper
from ....config import logger

class PlayersScraper(BaseScraper):
    """Scraper específico para informações de jogadores"""
    
    async def get_players(self, game):
        """Obtém a lista de jogadores ativos"""
        cache_key = f'team_players_{game}'
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
            
        players = []
        
        try:
            url = self.base_urls.get(game.lower())
            if not url:
                return players
                
            html = await self.get_page(url)
            soup = self.parse_html(html)
            if not soup:
                return players
                
            if game.lower() == "csgo":
                # HLTV player section
                player_section = soup.select_one(".players")
                if player_section:
                    for elem in player_section.select(".player"):
                        name = elem.select_one(".text-ellipsis")
                        id_elem = elem.get("href", "")
                        role = elem.select_one(".player-role")
                        if name:
                            players.append({
                                "nickname": name.text.strip(),
                                "name": "N/A",  # Would need extra request to player page
                                "country": "BR",
                                "role": role.text.strip() if role else "Player",
                                "id": id_elem.split("/")[-1] if id_elem else None
                            })
                            
            elif game.lower() == "valorant":
                # VLR.gg player cards
                player_cards = soup.select(".team-roster-item")
                for card in player_cards:
                    name = card.select_one(".team-roster-item-name")
                    role = card.select_one(".team-roster-item-role")
                    if name:
                        players.append({
                            "nickname": name.text.strip(),
                            "name": "N/A",
                            "country": "BR",
                            "role": role.text.strip() if role else "Player"
                        })
            
            self._set_cache(cache_key, players)
            return players
            
        except Exception as e:
            logger.error(f"Error getting players for {game}: {e}")
            return players