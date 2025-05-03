from telegram import Update
from telegram.ext import ContextTypes
from ....config.settings import logger, URLS
from ...utils import create_keyboard, send_or_edit_message

async def cmd_campeonato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /campeonato - mostra opções de campeonatos"""
    await show_campeonatos_menu(update, context)

async def show_campeonatos_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o menu de campeonatos"""
    keyboard = create_keyboard([
        ("🏆 Próximos Campeonatos", "proximos_campeonatos"),
        ("📊 Resultados", "resultados"),
        ("📅 Jogos Futuros", "jogos_futuros"),
        ("📝 Resumo", "resumo"),
        ("🌐 Ver no Site", URLS["campeonatos"]),
        ("🔙 Voltar ao Menu", "start")
    ])
    
    await send_or_edit_message(
        update,
        context,
        "🎮 <b>Campeonatos FURIA</b>\n\n"
        "Escolha uma opção para ver informações sobre os campeonatos e partidas:",
        keyboard,
        parse_mode="HTML"
    )