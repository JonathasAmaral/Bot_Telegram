from telegram import Update
from telegram.ext import ContextTypes
from config import logger
from utils import create_keyboard, send_or_edit_message, json_reader
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
    
    await show_games_menu(update, context)

async def callback_furia_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # callback de seleção de jogo
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_game_options(update, context, game)

async def callback_furia_info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_team_info(update, context, game)

async def callback_furia_players(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_players(update, context, game)

async def callback_furia_upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_upcoming_matches(update, context, game)

async def callback_furia_results(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_recent_results(update, context, game)

async def callback_furia_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE):
   
    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    await show_recent_tournaments(update, context, game)

async def callback_furia_refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query.data
    game = query.split('_')[-1].upper()
    
    # Clear cache for this game's data
    json_reader.clear_cache(game.lower())
    logger.info(f"Cache limpo para o jogo {game}")
    
    # Informar ao usuário sobre o script de atualização de dados
    keyboard = create_keyboard([
        ("🔄 Recarregar dados", f"furia_game_{game.lower()}"),
        ("🔙 Voltar ao menu", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        f"🔄 <b>Dados atualizados!</b>\n\n"
        f"Os dados da FURIA {game} foram recarregados.",
        keyboard,
        parse_mode="HTML"
    )
