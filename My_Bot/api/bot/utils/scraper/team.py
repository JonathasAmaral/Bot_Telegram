from .base import BaseScraper
from ....config import logger

class TeamScraper(BaseScraper):
    """Scraper específico para informações do time"""
    
    async def get_info(self, game):
        """Obtém informações gerais do time"""
        cache_key = f'team_info_{game}'
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
            
        info = {
            "name": "FURIA",
            "country": "Brazil",
            "region": "Americas",
            "world_ranking": "N/A",
            "ranking": "N/A"
        }
            
        try:
            url = self.base_urls.get(game.lower())
            if not url:
                return info
                
            html = await self.get_page(url)
            soup = self.parse_html(html)
            if not soup:
                return info
                
            if game.lower() == "csgo":
                # HLTV ranking element
                rank_elem = soup.select_one(".profile-team-stat .right")
                if rank_elem:
                    rank_text = rank_elem.text.strip()
                    info["world_ranking"] = rank_text.replace("#", "")
                
                # Region info from profile-team-stats
                region_elem = soup.select_one(".profile-team-stat-item .value")
                if region_elem:
                    info["region"] = region_elem.text.strip()
                    
            elif game.lower() == "valorant":
                # VLR.gg ranking is in .rank-item
                rank_elem = soup.select_one(".rank-item .rank")
                if rank_elem:
                    rank_text = rank_elem.text.strip()
                    info["world_ranking"] = rank_text.replace("#", "")
                    
                # Region from team header
                region_elem = soup.select_one(".team-header-region")
                if region_elem:
                    info["region"] = region_elem.text.strip()
            
            self._set_cache(cache_key, info)
            return info
                    
        except Exception as e:
            logger.error(f"Error getting team info for {game}: {e}")
            return info