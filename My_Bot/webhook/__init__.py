# Webhook package initialization

# Import from the new centralized configuration
from config import BOT_TOKEN, WEBHOOK_URL, logger


# Expondo configurações principais do webhook
__all__ = ["BOT_TOKEN", "WEBHOOK_URL"]
