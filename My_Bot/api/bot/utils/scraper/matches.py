from .base import BaseScraper
from ....config import logger
from datetime import datetime

class MatchesScraper(BaseScraper):
    """Scraper específico para informações de partidas"""
    
    async def get_upcoming(self, game):
        """Obtém próximos jogos agendados"""
        cache_key = f'upcoming_matches_{game}'
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
            
        matches = []
        
        try:
            url = self.base_urls.get(game.lower())
            if not url:
                return matches
                
            html = await self.get_page(url)
            soup = self.parse_html(html)
            if not soup:
                return matches
                
            if game.lower() == "csgo":
                # HLTV upcoming matches section
                match_section = soup.select_one(".upcoming-matches")
                if match_section:
                    for elem in match_section.select(".match-item"):
                        opponent = elem.select_one(".team-cell")
                        event = elem.select_one(".event-cell")
                        date = elem.select_one(".date-cell")
                        format_text = elem.select_one(".format-cell")
                        
                        if opponent and date:
                            matches.append({
                                "opponent": opponent.text.strip(),
                                "event": event.text.strip() if event else "TBD",
                                "date": date.text.strip(),
                                "time": "TBD",
                                "format": format_text.text.strip() if format_text else "BO3"
                            })
                            
            elif game.lower() == "valorant":
                # VLR.gg upcoming matches
                match_items = soup.select(".wf-card.match-item:not(.mod-completed)")
                for item in match_items:
                    opponent = item.select_one(".match-item-vs-team-name")
                    event = item.select_one(".match-item-event")
                    date = item.select_one(".match-item-time")
                    format_text = item.select_one(".match-item-format")
                    
                    if opponent and date:
                        matches.append({
                            "opponent": opponent.text.strip(),
                            "event": event.text.strip() if event else "TBD",
                            "date": date.text.strip(),
                            "time": "TBD",
                            "format": format_text.text.strip() if format_text else "BO3"
                        })
            
            self._set_cache(cache_key, matches)
            return matches
            
        except Exception as e:
            logger.error(f"Error getting upcoming matches for {game}: {e}")
            return matches
            
    async def get_results(self, game):
        """Obtém resultados recentes"""
        cache_key = f'recent_results_{game}'
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            return cached
            
        results = []
        
        try:
            url = self.base_urls.get(game.lower())
            if not url:
                return results
                
            html = await self.get_page(url)
            soup = self.parse_html(html)
            if not soup:
                return results
                
            if game.lower() == "csgo":
                # HLTV results section
                result_section = soup.select_one(".results-holder")
                if result_section:
                    for elem in result_section.select(".result-con")[:5]:
                        opponent = elem.select_one(".team-name")
                        event = elem.select_one(".event-name")
                        date = elem.select_one(".date")
                        score = elem.select_one(".score-cell")
                        map_name = elem.select_one(".map-name")
                        
                        if opponent and score:
                            results.append({
                                "opponent": opponent.text.strip(),
                                "event": event.text.strip() if event else "N/A",
                                "date": date.text.strip() if date else "N/A",
                                "score": score.text.strip(),
                                "map": map_name.text.strip() if map_name else "N/A"
                            })
                            
            elif game.lower() == "valorant":
                # VLR.gg completed matches
                match_items = soup.select(".wf-card.match-item.mod-completed")[:5]
                for item in match_items:
                    opponent = item.select_one(".match-item-vs-team-name")
                    event = item.select_one(".match-item-event")
                    date = item.select_one(".match-item-time")
                    score = item.select_one(".match-item-score")
                    maps = item.select(".match-item-map-name")
                    
                    if opponent and score:
                        results.append({
                            "opponent": opponent.text.strip(),
                            "event": event.text.strip() if event else "N/A",
                            "date": date.text.strip() if date else "N/A",
                            "score": score.text.strip(),
                            "map": ", ".join(m.text.strip() for m in maps) if maps else "N/A"
                        })
            
            self._set_cache(cache_key, results)
            return results
            
        except Exception as e:
            logger.error(f"Error getting recent results for {game}: {e}")
            return results