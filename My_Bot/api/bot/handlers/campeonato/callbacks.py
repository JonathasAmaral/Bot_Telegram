from telegram import Update
from telegram.ext import ContextTypes
from ....config.settings import URLS
from ...utils import create_keyboard, send_or_edit_message, scraper
from .campeonato_handler import show_campeonatos_menu

async def callback_campeonatos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de campeonatos"""
    await show_campeonatos_menu(update, context)

async def callback_proximos_campeonatos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de próximos campeonatos"""
    campeonatos = await scraper.get_proximos_campeonatos()
    
    text = "🏆 <b>Próximos Campeonatos</b>\n\n"
    if not campeonatos:
        text += "Não foi possível obter informações sobre os próximos campeonatos no momento."
    else:
        for i, camp in enumerate(campeonatos, 1):
            text += f"{i}. <b>{camp['nome']}</b>\n"
            text += f"   📅 {camp['data']}\n\n"
    
    keyboard = create_keyboard([
        ("🔙 Voltar", "campeonatos")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def callback_resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de resultados"""
    resultados = await scraper.get_resultados()
    
    text = "📊 <b>Últimos Resultados</b>\n\n"
    if not resultados:
        text += "Não foi possível obter informações sobre os resultados no momento."
    else:
        for i, res in enumerate(resultados, 1):
            text += f"{i}. <b>{res['time1']} {res['placar1']} x {res['placar2']} {res['time2']}</b>\n"
            text += f"   📅 {res['data']}\n\n"
    
    keyboard = create_keyboard([
        ("🔙 Voltar", "campeonatos")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def callback_jogos_futuros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de jogos futuros"""
    jogos = await scraper.get_jogos_futuros()
    
    text = "📅 <b>Próximos Jogos</b>\n\n"
    if not jogos:
        text += "Não foi possível obter informações sobre os jogos futuros no momento."
    else:
        for i, jogo in enumerate(jogos, 1):
            text += f"{i}. <b>{jogo['time1']} vs {jogo['time2']}</b>\n"
            text += f"   📅 {jogo['data']} - ⌚ {jogo['hora']}\n"
            text += f"   🏆 {jogo['evento']}\n\n"
    
    keyboard = create_keyboard([
        ("🔙 Voltar", "campeonatos")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def callback_resumo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de resumo"""
    resumo = await scraper.get_resumo()
    
    text = "📝 <b>Resumo da FURIA</b>\n\n"
    if not resumo:
        text += "Não foi possível obter o resumo no momento."
    else:
        text += f"<b>Ranking:</b> {resumo['ranking']}\n\n"
        text += "<b>Últimos Jogos:</b>\n"
        for jogo in resumo["últimos_jogos"]:
            text += f"• {jogo['adversario']} - {jogo['resultado']}\n"
            text += f"  📅 {jogo['data']}\n"
    
    keyboard = create_keyboard([
        ("🔙 Voltar", "campeonatos")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )