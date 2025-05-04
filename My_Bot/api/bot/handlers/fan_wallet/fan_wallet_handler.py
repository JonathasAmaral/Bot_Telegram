from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ....config import logger
from ...utils import create_keyboard, send_message, send_or_edit_message
from ...utils.fan_wallet_generator import generate_fan_wallet_image, generate_fan_wallet_pdf

async def cmd_fan_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Handler para o comando /fan_wallet
    logger.info("Comando /fan_wallet recebido")
    await show_fan_wallet_menu(update, context)

async def show_fan_wallet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = create_keyboard([
        ("🎫 Carteira PNG", "fan_wallet_png"),
        ("📄 Carteira PDF", "fan_wallet_pdf"),
        ("🔙 Voltar ao Menu", "start")
    ])

    message = "💳 <b>Carteira de Fã FURIA</b>\n\n" \
              "Gere sua carteira personalizada de fã da FURIA!\n\n" \
              "Escolha o formato desejado:"

    await send_or_edit_message(update, context, message, keyboard, parse_mode="HTML")

async def create_return_button():

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="start")]
    ])
    return keyboard

async def send_fan_wallet_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gera e envia a carteira de fã
    user = update.effective_user
    
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    
    await send_message(update, context, "⏳ Gerando sua carteira de fã...", parse_mode="HTML")
    
    # Gera a carteira
    try:
        img_bytes = generate_fan_wallet_image(user_data)
        
        return_keyboard = await create_return_button()
        
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=img_bytes,
            caption="🎉 <b>Sua Carteira de Fã FURIA!</b>\n\n"
                   "Esta é sua carteira oficial de fã da FURIA.\n"
                   "Baixe e guarde com você!",
            parse_mode="HTML",
            reply_markup=return_keyboard
        )
        logger.info(f"Carteira PNG gerada para o usuário {user.id}")
    except Exception as e:
        logger.error(f"Erro ao gerar carteira PNG: {e}")
        await send_message(
            update, 
            context, 
            "❌ Erro ao gerar sua carteira. Por favor, tente novamente mais tarde.", 
            parse_mode="HTML",
            reply_markup=await create_return_button()
        )

async def send_fan_wallet_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gera e envia a carteira de fã
    user = update.effective_user
    
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    
    await send_message(update, context, "⏳ Gerando sua carteira de fã em PDF...", parse_mode="HTML")
    
    # Gera a carteira em PDF
    try:
        pdf_bytes = generate_fan_wallet_pdf(user_data)
        
        return_keyboard = await create_return_button()
        
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=pdf_bytes,
            filename=f"FURIA_Fan_Wallet_{user.id}.pdf",
            caption="🎉 <b>Sua Carteira de Fã FURIA em PDF!</b>\n\n"
                   "Esta é sua carteira oficial de fã da FURIA em formato PDF.\n"
                   "Você pode imprimir e levar com você!",
            parse_mode="HTML",
            reply_markup=return_keyboard
        )
        logger.info(f"Carteira PDF gerada para o usuário {user.id}")
    except Exception as e:
        logger.error(f"Erro ao gerar carteira PDF: {e}")
        await send_message(
            update, 
            context, 
            "❌ Erro ao gerar sua carteira em PDF. Por favor, tente novamente mais tarde.", 
            parse_mode="HTML",
            reply_markup=await create_return_button()
        )