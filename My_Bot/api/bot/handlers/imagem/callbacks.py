from telegram import Update
from telegram.ext import ContextTypes
from ....config import logger
from ...utils import create_keyboard, send_or_edit_message, send_image
from .imagem_handler import IMAGE_PATHS, show_imagens_menu

async def callback_imagens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de imagens"""
    await show_imagens_menu(update, context)

async def _handle_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE, image_type: str, title: str, emoji: str):
    """Função auxiliar para manipular envio de imagens"""
    if not IMAGE_PATHS[image_type].exists():
        await send_or_edit_message(
            update,
            context,
            f"⚠️ {title} ainda não disponível. Por favor, tente novamente mais tarde."
        )
        return
    
    keyboard = create_keyboard([
        ("🔙 Voltar às Imagens", "imagens")
    ])
    
    await send_image(
        update,
        context,
        IMAGE_PATHS[image_type],
        f"{emoji} <b>{title}</b>",
        keyboard
    )

async def callback_imagem_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de imagem do time"""
    await _handle_imagem(update, context, "time", "Time FURIA", "👥")

async def callback_imagem_logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de logo"""
    await _handle_imagem(update, context, "logo", "Logo FURIA", "🎭")

async def callback_imagem_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de wallpaper para celular"""
    await _handle_imagem(update, context, "wallpaper_mobile", "Wallpaper Mobile FURIA", "📱")

async def callback_imagem_desktop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de wallpaper para desktop"""
    await _handle_imagem(update, context, "wallpaper_desktop", "Wallpaper Desktop FURIA", "💻")