import os
import json
import logging
import re

logger = logging.getLogger("telegram-bot")

# Config file path - corrigindo para apontar para a pasta My_Bot/secret
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secret", "config.json")

def validate_bot_token(token):
    """Validate that the token has the proper Telegram bot token format."""
    if not token:
        return False
    
    pattern = r'^\d+:[A-Za-z0-9_-]+$'
    if not re.match(pattern, token):
        logger.error("Token inválido: não corresponde ao formato do Telegram")
        return False
    return True

def load_bot_token():
    """Load the bot token from environment variables or config file."""
    token = os.environ.get("BOT_TOKEN", "")

    if not token:
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                token = config.get("BOT_TOKEN", "")
                if token:
                    logger.info("Token carregado do arquivo de configuração")
        except Exception as e:
            logger.error(f"Erro ao carregar token: {e}")
            
    if not token:
        logger.warning("BOT_TOKEN não configurado!")
        return ""
    
    if not validate_bot_token(token):
        logger.error("BOT_TOKEN configurado com formato inválido!")
        return ""
    
    return token

def load_webhook_url():
    """Load the webhook URL from environment variables or config file."""
    webhook_url = os.environ.get("WEBHOOK_URL", "")

    if not webhook_url:
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                webhook_url = config.get("WEBHOOK_URL", "")
                if webhook_url:
                    logger.info("WEBHOOK_URL carregado do arquivo de configuração")
        except Exception as e:
            logger.debug(f"Erro ao carregar webhook URL: {e}")
    
    # Ensure the webhook URL ends with /api/webhook
    if webhook_url and not webhook_url.endswith("/api/webhook"):
        webhook_url = webhook_url.rstrip("/") + "/api/webhook"
    
    return webhook_url
