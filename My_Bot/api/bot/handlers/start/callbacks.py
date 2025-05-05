from telegram import Update
from telegram.ext import ContextTypes
from config import logger
from utils import create_keyboard, send_or_edit_message
from .start_handler import show_main_menu

async def callback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Handler para o callback de retorno ao menu principal
    await show_main_menu(update, context)

async def callback_loja(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    keyboard = create_keyboard([
        ("🛒 Visitar a Loja", "https://www.furia.gg"),
        ("🔙 Voltar ao Menu", "start")
    ])
    
    await send_or_edit_message(
        update,
        context,
        "🛒 Visite nossa loja oficial e adquira produtos exclusivos da FURIA!",
        keyboard
    )

async def callback_sobre(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = create_keyboard([
        ("🔙 Voltar ao Menu", "start")
    ])
    
    await send_or_edit_message(
        update,
        context,
        "ℹ️ <b>Sobre o Bot da FURIA</b>\n\n"
        "A FURIA é uma organização brasileira de esportes eletrônicos (eSports), "
        "reconhecida internacionalmente por suas equipes competitivas em jogos como CS:GO, Valorant e outros.\n\n"
        "Este bot foi desenvolvido para os fãs da FURIA acompanharem as novidades, "
        "campeonatos e terem acesso a conteúdos exclusivos do time.\n\n"
        "<b>Versão:</b> 3.7.9\n"
        "<b>Desenvolvido por:</b> Jonathas ",
        keyboard,
        parse_mode="HTML"
    )
