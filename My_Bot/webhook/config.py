import logging
from .token import BOT_TOKEN, WEBHOOK_URL

CONFIG_FILE_PATH = "secret/config.json"
DEFAULT_WEBHOOK_PATH = "/api/webhook"

logger = logging.getLogger("telegram-bot")


# Configurações da aplicação
APP_SETTINGS = {
    "name": "Telegram Bot",
    "version": "1.7.4",
    "description": "Bot Telegram com webhook",
    "debug": False
}

def get_bot_info():
    return {
        "bot_token_configured": bool(BOT_TOKEN),
        "webhook_url_configured": bool(WEBHOOK_URL),
        "webhook_url": WEBHOOK_URL or "Not configured",
        "app_version": APP_SETTINGS["version"]
    }
