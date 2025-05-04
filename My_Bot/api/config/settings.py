import logging

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
