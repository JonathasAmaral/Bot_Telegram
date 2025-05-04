from webhook.token import BOT_TOKEN, WEBHOOK_URL
import logging
from .settings import URLS, FURIA_TEAM_IDS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("telegram-bot")

__all__ = [
    "logger",
    "URLS",
    "BOT_TOKEN",
    "WEBHOOK_URL",
    "FURIA_TEAM_IDS"
]
