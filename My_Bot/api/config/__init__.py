from webhook.token import BOT_TOKEN, WEBHOOK_URL
import logging
from .settings import URLS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("telegram-bot")

__all__ = ["logger", "URLS", "BOT_TOKEN", "WEBHOOK_URL"]
