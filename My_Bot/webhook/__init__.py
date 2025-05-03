# Módulo de webhook
from .config import DEFAULT_WEBHOOK_PATH, APP_SETTINGS, get_bot_info
from .token import BOT_TOKEN, WEBHOOK_URL
from .routes import router

# Expondo configurações principais do webhook
__all__ = [
    "BOT_TOKEN",
    "WEBHOOK_URL",
    "router"
]
