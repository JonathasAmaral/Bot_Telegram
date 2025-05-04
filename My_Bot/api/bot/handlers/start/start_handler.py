from telegram import Update
from telegram.ext import ContextTypes
from ....config import logger
from ...utils import create_keyboard, send_or_edit_message

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start - mostra o menu principal"""
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_name=None):
    """Mostra o menu principal do bot"""
    if user_name is None:
        user_name = update.message.from_user.first_name if update.message else update.callback_query.from_user.first_name
    
    keyboard = create_keyboard([
        ("🛒 Loja", "loja"),
        ("🎮 FURIA", "furia"),
        ("🖼️ Imagens", "imagens"),
        ("ℹ️ Sobre", "sobre")
    ])
    
    await send_or_edit_message(
        update,
        context,
        f"Olá, {user_name}! 👋\n\n"
        "Bem-vindo ao Bot da FURIA! \n\n"
        "Escolha uma opção abaixo:",
        keyboard
    )
    logger.info(f"Usuário {user_name} acessou o menu principal")
