"""
Pacote API do Telegram Bot
"""
from .bot import create_bot
from config import BOT_TOKEN, WEBHOOK_URL, logger, DEBUG, URLS

__all__ = ["create_bot", "BOT_TOKEN", "WEBHOOK_URL", "logger", "DEBUG", "URLS"]
