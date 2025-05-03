import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re
from functools import lru_cache
from ...config import URLS, logger

# Cache para evitar requisições repetidas (TTL: 1 hora)
CACHE_TTL = 3600  # segundos

class WebScraper:
    """Classe para coletar dados de sites externos de forma eficiente"""
    
    def __init__(self):
        """Inicializa o scraper"""
        self.session = None
        self.last_fetch = {}

    async def ensure_session(self):
        """Garante que existe uma sessão HTTP ativa"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; FuriaBot/1.0)",
                    "Accept": "text/html,application/xhtml+xml"
                },
                timeout=aiohttp.ClientTimeout(total=10)
            )
        return self.session

    async def close(self):
        """Fecha a sessão HTTP"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get_page(self, url):
        """Busca o conteúdo de uma página web"""
        try:
            session = await self.ensure_session()
            async with session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Erro ao acessar {url}: {response.status}")
                    return None
                return await response.text()
        except Exception as e:
            logger.error(f"Erro ao buscar {url}: {e}")
            return None

    @lru_cache(maxsize=32)
    async def get_proximos_campeonatos(self):
        """Obtém os próximos campeonatos da equipe"""
        html = await self.get_page(URLS["campeonatos"])
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        campeonatos = []
        
        try:
            # Localizar seção de campeonatos
            elementos = soup.select('.event-card')
            
            for elemento in elementos[:5]:  # Limitar a 5 resultados
                nome = elemento.select_one('.event-card__title')
                data = elemento.select_one('.event-card__date')
                
                if nome and data:
                    campeonatos.append({
                        "nome": nome.text.strip(),
                        "data": data.text.strip()
                    })
            
            return campeonatos
        except Exception as e:
            logger.error(f"Erro ao processar campeonatos: {e}")
            return []

    @lru_cache(maxsize=32)
    async def get_resultados(self):
        """Obtém os resultados dos últimos jogos"""
        html = await self.get_page(URLS["resultados"])
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        resultados = []
        
        try:
            # Localizar seção de resultados
            elementos = soup.select('.match-card')
            
            for elemento in elementos[:5]:  # Limitar a 5 resultados
                times = elemento.select('.match-card__team-name')
                placar = elemento.select('.match-card__score')
                data = elemento.select_one('.match-card__date')
                
                if len(times) >= 2 and len(placar) >= 2 and data:
                    resultados.append({
                        "time1": times[0].text.strip(),
                        "time2": times[1].text.strip(),
                        "placar1": placar[0].text.strip(),
                        "placar2": placar[1].text.strip(),
                        "data": data.text.strip()
                    })
            
            return resultados
        except Exception as e:
            logger.error(f"Erro ao processar resultados: {e}")
            return []

    @lru_cache(maxsize=32)
    async def get_jogos_futuros(self):
        """Obtém os próximos jogos agendados"""
        html = await self.get_page(URLS["proximos_jogos"])
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        jogos = []
        
        try:
            # Localizar seção de jogos futuros
            elementos = soup.select('.match-card')
            
            for elemento in elementos[:5]:  # Limitar a 5 resultados
                times = elemento.select('.match-card__team-name')
                data = elemento.select_one('.match-card__date')
                hora = elemento.select_one('.match-card__time')
                evento = elemento.select_one('.match-card__event')
                
                if len(times) >= 2 and data:
                    jogos.append({
                        "time1": times[0].text.strip(),
                        "time2": times[1].text.strip(),
                        "data": data.text.strip(),
                        "hora": hora.text.strip() if hora else "A definir",
                        "evento": evento.text.strip() if evento else "Evento não especificado"
                    })
            
            return jogos
        except Exception as e:
            logger.error(f"Erro ao processar jogos futuros: {e}")
            return []

    @lru_cache(maxsize=32)
    async def get_resumo(self):
        """Obtém um resumo geral da equipe"""
        html = await self.get_page(URLS["equipe"])
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        resumo = {
            "nome": "FURIA",
            "ranking": "N/A",
            "últimos_jogos": [],
            "próximos_jogos": []
        }
        
        try:
            # Extrair informações gerais
            ranking = soup.select_one('.team-header__ranking')
            if ranking:
                resumo["ranking"] = ranking.text.strip()
            
            # Últimos jogos
            jogos = soup.select('.match-list__item')[:3]
            for jogo in jogos:
                adversario = jogo.select_one('.match-list__opponent')
                resultado = jogo.select_one('.match-list__result')
                data = jogo.select_one('.match-list__date')
                
                if adversario and resultado and data:
                    resumo["últimos_jogos"].append({
                        "adversario": adversario.text.strip(),
                        "resultado": resultado.text.strip(),
                        "data": data.text.strip()
                    })
            
            return resumo
        except Exception as e:
            logger.error(f"Erro ao processar resumo: {e}")
            return resumo

# Instância global
scraper = WebScraper() 