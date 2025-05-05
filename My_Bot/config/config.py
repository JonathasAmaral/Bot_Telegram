import os
import json
import logging
import re

# Base directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "secret", "config.json")

# Logger configuration
logger = logging.getLogger("telegram-bot")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuration constants
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)

# Webhook configuration
WEBHOOK_PATH = "/api/webhook"

# Import token-related functions from token.py
from .token import load_bot_token, load_webhook_url

# Load and validate tokens
BOT_TOKEN = load_bot_token()
WEBHOOK_URL = load_webhook_url()

# Additional URLs or configs can be added here
URLS = {
    "api": WEBHOOK_URL,
    "base": WEBHOOK_URL.replace(WEBHOOK_PATH, "") if WEBHOOK_URL else ""
}

if not BOT_TOKEN or not WEBHOOK_URL:
    logger.error("Configuração incompleta! Verifique BOT_TOKEN e WEBHOOK_URL no arquivo config.json ou variáveis de ambiente.")
