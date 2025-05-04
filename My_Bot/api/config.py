import logging
import json
import os

# Path to the config.json file
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secret", "config.json")

# Load configuration from JSON file
with open(config_path, "r") as f:
    config_data = json.load(f)

# Extract configuration values
BOT_TOKEN = config_data.get("BOT_TOKEN")
WEBHOOK_URL = config_data.get("WEBHOOK_URL")
DEBUG = config_data.get("DEBUG", False)

# Configurar o logger para o bot
logger = logging.getLogger("telegram-bot")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)
