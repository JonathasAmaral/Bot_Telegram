from telegram.ext import ApplicationBuilder
from webhook.token import BOT_TOKEN, WEBHOOK_URL
from api.config import logger
from .handlers.commands import register_handlers
import os

async def create_bot():
    # Create the application instance
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register command handlers
    register_handlers(application)

    await application.initialize()
    logger.info("Bot inicializado com sucesso")
    
    return application
