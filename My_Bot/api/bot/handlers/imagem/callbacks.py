from telegram import Update
from telegram.ext import ContextTypes
from ....config import logger
from ...utils import create_keyboard, send_or_edit_message
from .imagem_handler import IMAGE_PATHS, show_imagens_menu

async def callback_imagens(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await show_imagens_menu(update, context)

async def _handle_imagem(update: Update, context: ContextTypes.DEFAULT_TYPE, image_type: str, title: str, emoji: str):
    # Função auxiliar para manipular envio de imagens
    image_path = IMAGE_PATHS[image_type]
    logger.info(f"Attempting to send image from path: {image_path}")
    
    if not image_path.exists():
        error_msg = f"⚠️ {title} não está disponível no momento. Verifique se a imagem '{image_path.name}' existe no diretório correto."
        logger.error(f"Image not found: {image_path}")
        await send_or_edit_message(
            update,
            context,
            error_msg
        )
        return
    
    try:
        keyboard = create_keyboard([
            ("🔙 Voltar ao Menu", "start")  # Mudando o botão para voltar ao menu principal
        ])
        
        chat_id = update.callback_query.message.chat_id
        await update.callback_query.answer()
        
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=f"{emoji} <b>{title}</b>",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        logger.info(f"Successfully sent image: {image_path}")
    except Exception as e:
        logger.error(f"Error sending image {image_path}: {str(e)}")
        await send_or_edit_message(
            update,
            context,
            f"⚠️ Erro ao enviar {title}. Por favor, tente novamente mais tarde."
        )

# Callback handlers for each image type
async def callback_imagem_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
 
    await _handle_imagem(update, context, "time", "Time FURIA", "👥")

async def callback_imagem_logo(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    await _handle_imagem(update, context, "logo", "Logo FURIA", "🎭")

async def callback_imagem_mobile(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
    await _handle_imagem(update, context, "wallpaper_mobile", "Wallpaper Mobile FURIA", "📱")

async def callback_imagem_desktop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await _handle_imagem(update, context, "wallpaper_desktop", "Wallpaper Desktop FURIA", "💻")
