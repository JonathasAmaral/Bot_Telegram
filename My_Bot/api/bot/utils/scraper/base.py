import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
from ....config import logger

class BaseScraper:
    """Classe base com funcionalidades comuns de scraping"""
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_ttl = 300  # Reduced TTL to 5 minutes for more frequent updates
        self.base_urls = {
            "csgo": "https://www.hltv.org/team/8297/furia",
            "valorant": "https://www.vlr.gg/team/2406/furia"
        }
        
    def _is_cache_valid(self, key):
        """Verifica se um item do cache ainda é válido"""
        if key not in self.cache:
            return False
        timestamp, _ = self.cache[key]
        return (datetime.now() - timestamp).total_seconds() < self.cache_ttl

    def _get_from_cache(self, key):
        """Obtém um item do cache se válido"""
        if self._is_cache_valid(key):
            _, value = self.cache[key]
            return value
        return None

    def _set_cache(self, key, value):
        """Armazena um item no cache"""
        self.cache[key] = (datetime.now(), value)

    async def ensure_session(self):
        """Garante que existe uma sessão HTTP ativa"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; FuriaBot/1.0; +http://furia.gg)",
                    "Accept": "text/html,application/xhtml+xml,application/xml"
                },
                timeout=aiohttp.ClientTimeout(total=10)
            )
        return self.session

    async def get_page(self, url):
        """Busca o conteúdo de uma página web com retry"""
        for attempt in range(3):  # Try up to 3 times
            try:
                session = await self.ensure_session()
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 429:  # Too Many Requests
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    logger.error(f"Error {response.status} accessing {url}")
                    return None
            except Exception as e:
                logger.error(f"Error fetching {url} (attempt {attempt + 1}): {e}")
                if attempt < 2:  # Don't sleep on last attempt
                    await asyncio.sleep(1)
        return None

    async def close(self):
        """Fecha a sessão HTTP"""
        if self.session and not self.session.closed:
            await self.session.close()

    def parse_html(self, html):
        """Parse HTML with error handling"""
        if not html:
            return None
        try:
            return BeautifulSoup(html, 'lxml')
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None