from telegram.ext import ApplicationBuilder
from telegram import BotCommand, MenuButtonCommands
from config import BOT_TOKEN, WEBHOOK_URL, logger
from .handlers.commands import register_handlers
import os

async def create_bot():

    application = ApplicationBuilder().token(BOT_TOKEN).updater(None).build()
    
    # Register command handlers
    register_handlers(application)

    # Configurar o menu de comandos botão de menu
    commands = [
        BotCommand("start", "menu principal"),
        BotCommand("furia", "jogos da FURIA"),
        BotCommand("imagem", "imagens e wallpapers"),
        BotCommand("fan_wallet", "Carterinha de fãn")
    ]
    await application.bot.set_my_commands(commands)
    
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())
    
    # Initialize the application before returning it
    await application.initialize()
    
    logger.info("Bot inicializado com sucesso")
    
    return application
