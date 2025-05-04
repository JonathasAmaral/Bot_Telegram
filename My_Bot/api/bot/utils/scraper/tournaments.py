from .base import BaseScraper
from ....config import logger

class TournamentsScraper(BaseScraper):
    """Scraper específico para informações de torneios"""
    
    async def get_recent(self, game):
        """Obtém torneios recentes"""
        cache_key = f'recent_tournaments_{game}'
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
            
        tournaments = []
        
        try:
            url = self.base_urls.get(game.lower())
            if not url:
                return tournaments
                
            html = await self.get_page(url)
            soup = self.parse_html(html)
            if not soup:
                return tournaments
                
            if game.lower() == "csgo":
                # HLTV tournaments section
                tournament_section = soup.select_one(".team-tournaments")
                if tournament_section:
                    for elem in tournament_section.select(".team-tournament")[:5]:
                        name = elem.select_one(".tournament-name")
                        date = elem.select_one(".tournament-date")
                        prize = elem.select_one(".prize-pool")
                        placement = elem.select_one(".placement")
                        location = elem.select_one(".location")
                        
                        if name:
                            tournaments.append({
                                "name": name.text.strip(),
                                "date": date.text.strip() if date else "N/A",
                                "prize_pool": prize.text.strip() if prize else "N/A",
                                "location": location.text.strip() if location else "N/A",
                                "placement": placement.text.strip() if placement else "N/A"
                            })
                            
            elif game.lower() == "valorant":
                # VLR.gg tournaments
                tournament_items = soup.select(".team-tournament-item")[:5]
                for item in tournament_items:
                    name = item.select_one(".tournament-name")
                    date = item.select_one(".tournament-date")
                    prize = item.select_one(".tournament-prize")
                    placement = item.select_one(".tournament-placement")
                    
                    if name:
                        tournaments.append({
                            "name": name.text.strip(),
                            "date": date.text.strip() if date else "N/A",
                            "prize_pool": prize.text.strip() if prize else "N/A",
                            "location": "N/A",  # VLR doesn't show location consistently
                            "placement": placement.text.strip() if placement else "N/A"
                        })
            
            self._set_cache(cache_key, tournaments)
            return tournaments
            
        except Exception as e:
            logger.error(f"Error getting recent tournaments for {game}: {e}")
            return tournaments