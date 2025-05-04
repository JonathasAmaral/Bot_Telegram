from telegram import Update
from telegram.ext import ContextTypes

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, parse_mode=None):
    """Send a new message"""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        return await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    else:
        return await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

async def edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, parse_mode=None):
    """Edit existing message"""
    await update.callback_query.answer()
    return await update.callback_query.message.edit_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )

async def send_or_edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None, parse_mode=None):
    """Envia uma nova mensagem ou edita a mensagem existente baseado no contexto"""
        #  e a mensagem atual é uma imagem, envia uma nova mensagem ao invés de tentar editar
    try:
        return await edit_message(update, context, text, reply_markup, parse_mode)
    except Exception as e:
        # Se falhar ao editar, envia uma nova mensagem
        return await send_message(update, context, text, reply_markup, parse_mode)
  
async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE, image_path, caption=None, reply_markup=None):
    """Send an image with optional caption and keyboard"""
    if update.callback_query:
        await update.callback_query.answer()
        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = update.message.chat_id

    with open(image_path, 'rb') as photo:
        return await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
