from telegram.ext import ApplicationBuilder
from telegram import BotCommand, MenuButtonCommands
from webhook.token import BOT_TOKEN, WEBHOOK_URL
from api.config import logger
from .handlers.commands import register_handlers
import os

async def create_bot():
    # Create the application instance
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register command handlers
    register_handlers(application)

    # Configurar o menu de comandos botão de menu
    commands = [
        BotCommand("start", "Iniciar o bot e mostrar o menu principal"),
        BotCommand("furia", "Ver informações sobre jogos da FURIA"),
        BotCommand("imagem", "Ver imagens e wallpapers da FURIA")
    ]
    await application.bot.set_my_commands(commands)
    
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    await application.initialize()
    logger.info("Bot inicializado com sucesso")
    
    return application
