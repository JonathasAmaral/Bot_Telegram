from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path
from ....config import logger
from ...utils import create_keyboard, send_message, send_or_edit_message, send_image

# Updated path to point to the correct images directory
IMAGES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "images"

IMAGE_PATHS = {
    "time": IMAGES_DIR / "time.jpg",
    "logo": IMAGES_DIR / "logo.png",
    "wallpaper_mobile": IMAGES_DIR / "wallpaper_mobile.jpg",
    "wallpaper_desktop": IMAGES_DIR / "wallpaper_desktop.jpg"
}

def ensure_images_dir():
    # Garante que o diretório de imagens exista
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Images directory path: {IMAGES_DIR}")

async def cmd_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await show_imagens_menu(update, context)

async def show_imagens_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mostra o menu de imagens"""
    ensure_images_dir()
    
    keyboard = create_keyboard([
        ("👥 Time", "imagem_time"),
        ("🎭 Logo", "imagem_logo"),
        [
            ("📱 Wallpaper Mobile", "imagem_mobile"),
            ("💻 Wallpaper Desktop", "imagem_desktop")
        ],
        ("🔙 Voltar ao Menu", "start")
    ])

    message = "🖼️ <b>Imagens FURIA</b>\n\n" \
             "Escolha uma opção para ver imagens da FURIA:"

    await send_or_edit_message(update, context, message, keyboard, parse_mode="HTML")
