from telegram import Update
from telegram.ext import ContextTypes
from ....config.settings import URLS
from ....config import logger
from ...utils import create_keyboard, send_or_edit_message, scraper
from .furia_handler import (
    show_games_menu,
    show_game_options,
    show_team_info,
    show_players,
    show_upcoming_matches,
    show_recent_results,
    show_recent_tournaments
)

async def callback_furia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback do menu principal da FURIA"""
    await show_games_menu(update, context)

async def callback_furia_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de seleção de jogo"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_game_options(update, context, game)

async def callback_furia_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de informações do time"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_team_info(update, context, game)

async def callback_furia_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback da lista de jogadores"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_players(update, context, game)

async def callback_furia_upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de próximos jogos"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_upcoming_matches(update, context, game)

async def callback_furia_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de resultados recentes"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_recent_results(update, context, game)

async def callback_furia_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de torneios recentes"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_recent_tournaments(update, context, game)

async def callback_furia_refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o callback de atualização de dados"""
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    
    # Clear cache for this game's data
    for key in list(scraper.cache.keys()):
        if game.lower() in key.lower():
            del scraper.cache[key]
    
    # Show game menu again with fresh data
    await show_game_options(update, context, game)