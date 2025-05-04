import logging
import os

logger = logging.getLogger("telegram-bot")

WEBHOOK_PATH = "/api/webhook"

# Configurações do bot
DEBUG = False

# URLs para serviços externos
URLS = {
    "loja": "https://www.furia.gg",
    "csgo": "https://www.hltv.org/team/8297/furia",
    "valorant": "https://www.vlr.gg/team/2406/furia"
}

# Team IDs for FURIA
FURIA_TEAM_IDS = {
    "csgo": "3237",  # FURIA CS:GO team ID
    "valorant": "3512"  # FURIA Valorant team ID  
}

# Cache settings
CACHE_TTL = 300  # 5 minutes cache
