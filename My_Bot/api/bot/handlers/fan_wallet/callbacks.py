from telegram import Update
from telegram.ext import ContextTypes
from .fan_wallet_handler import show_fan_wallet_menu, send_fan_wallet_image, send_fan_wallet_pdf
from ....config import logger

async def callback_fan_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Mostra o menu de carteira de fã 
    logger.info("Callback fan_wallet recebido")
    await update.callback_query.answer()
    await show_fan_wallet_menu(update, context)

async def callback_fan_wallet_png(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    logger.info("Callback fan_wallet_png recebido")
    await update.callback_query.answer()
    await send_fan_wallet_image(update, context)

async def callback_fan_wallet_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    logger.info("Callback fan_wallet_pdf recebido")
    await update.callback_query.answer()
    await send_fan_wallet_pdf(update, context)
