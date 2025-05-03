import logging

logger = logging.getLogger("telegram-bot")

WEBHOOK_PATH = "/api/webhook"

# Configurações do bot
DEBUG = False

# URLs para serviços externos
URLS = {
    "equipe": "https://draft5.gg/equipe/330-FURIA",
    "campeonatos": "https://draft5.gg/equipe/330-FURIA/campeonatos",
    "resultados": "https://draft5.gg/equipe/330-FURIA/resultados",
    "proximos_jogos": "https://draft5.gg/equipe/330-FURIA/proximas-partidas",
    "loja": "https://www.furia.gg"
}
