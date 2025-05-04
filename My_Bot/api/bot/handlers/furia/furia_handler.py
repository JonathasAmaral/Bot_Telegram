from telegram import Update
from telegram.ext import ContextTypes
from ....config import logger
from ...utils import create_keyboard, send_or_edit_message, scraper

async def cmd_furia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /furia - mostra o menu de jogos da FURIA"""
    await show_games_menu(update, context)

async def show_games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o menu de jogos disponíveis da FURIA"""
    games = await scraper.get_furia_games()
    
    if not games:
        await send_or_edit_message(
            update,
            context,
            "❌ Não foi possível obter informações sobre os jogos da FURIA no momento.",
            create_keyboard([("🔙 Voltar ao Menu", "start")])
        )
        return

    # Create buttons for each available game
    buttons = [(f"🎮 {game}", f"furia_game_{game.lower()}") for game in games]
    buttons.append(("🔙 Voltar ao Menu", "start"))
    
    keyboard = create_keyboard(buttons)
    
    await send_or_edit_message(
        update,
        context,
        "🏆 <b>FURIA Esports</b>\n\n"
        "Escolha um jogo para ver informações da FURIA:",
        keyboard,
        parse_mode="HTML"
    )

async def show_game_options(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra o menu de opções para um jogo específico"""
    keyboard = create_keyboard([
        ("📋 Informações gerais", f"furia_info_{game}"),
        ("👥 Lista de jogadores", f"furia_players_{game}"),
        ("📆 Próximos jogos", f"furia_upcoming_{game}"),
        ("📈 Últimos resultados", f"furia_results_{game}"),
        ("🏆 Torneios recentes", f"furia_tournaments_{game}"),
        ("🔄 Atualizar dados", f"furia_refresh_{game}"),
        ("🔙 Voltar aos jogos", "furia")
    ])
    
    await send_or_edit_message(
        update,
        context,
        f"🎮 <b>FURIA {game}</b>\n\n"
        "Escolha uma opção:",
        keyboard,
        parse_mode="HTML"
    )

async def show_team_info(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra informações gerais do time para um jogo específico"""
    info = await scraper.get_team_info(game)
    
    if not info:
        text = f"❌ Não foi possível obter informações da FURIA {game}."
    else:
        text = (
            f"📋 <b>FURIA {game}</b>\n\n"
            f"🌎 País: {info['country']}\n"
            f"🏆 Ranking Mundial: {info['world_ranking']}\n"
            f"🌍 Região: {info['region']}\n"
            f"📊 Ranking Regional: {info['ranking']}\n"
        )
    
    keyboard = create_keyboard([
        ("🔙 Voltar", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def show_players(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra a lista de jogadores para um jogo específico"""
    players = await scraper.get_team_players(game)
    
    if not players:
        text = f"❌ Não foi possível obter a lista de jogadores da FURIA {game}."
    else:
        text = f"👥 <b>Jogadores FURIA {game}</b>\n\n"
        for player in players:
            text += (
                f"🎮 <b>{player['nickname']}</b>\n"
                f"👤 Nome: {player['name']}\n"
                f"🌎 País: {player['country']}\n"
                f"📋 Função: {player['role']}\n\n"
            )
    
    keyboard = create_keyboard([
        ("🔙 Voltar", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def show_upcoming_matches(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra os próximos jogos para um jogo específico"""
    matches = await scraper.get_upcoming_matches(game)
    
    if not matches:
        text = f"❌ Não há próximos jogos agendados para FURIA {game}."
    else:
        text = f"📆 <b>Próximos Jogos FURIA {game}</b>\n\n"
        for match in matches:
            text += (
                f"🆚 <b>vs {match['opponent']}</b>\n"
                f"🏆 Evento: {match['event']}\n"
                f"📅 Data: {match['date']}\n"
                f"⌚ Horário: {match['time']}\n"
                f"📋 Formato: {match['format']}\n\n"
            )
    
    keyboard = create_keyboard([
        ("🔙 Voltar", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def show_recent_results(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra os resultados recentes para um jogo específico"""
    results = await scraper.get_recent_results(game)
    
    if not results:
        text = f"❌ Não foi possível obter resultados recentes da FURIA {game}."
    else:
        text = f"📈 <b>Últimos Resultados FURIA {game}</b>\n\n"
        for result in results:
            text += (
                f"🆚 <b>vs {result['opponent']}</b>\n"
                f"🏆 Evento: {result['event']}\n"
                f"📅 Data: {result['date']}\n"
                f"📊 Placar: {result['score']}\n"
                f"🗺️ Mapa: {result['map']}\n\n"
            )
    
    keyboard = create_keyboard([
        ("🔙 Voltar", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )

async def show_recent_tournaments(update: Update, context: ContextTypes.DEFAULT_TYPE, game: str):
    """Mostra os torneios recentes para um jogo específico"""
    tournaments = await scraper.get_recent_tournaments(game)
    
    if not tournaments:
        text = f"❌ Não foi possível obter torneios recentes da FURIA {game}."
    else:
        text = f"🏆 <b>Torneios Recentes FURIA {game}</b>\n\n"
        for tournament in tournaments:
            text += (
                f"🎮 <b>{tournament['name']}</b>\n"
                f"📅 Data: {tournament['date']}\n"
                f"💰 Premiação: {tournament['prize_pool']}\n"
                f"📍 Local: {tournament['location']}\n"
                f"🏅 Colocação: {tournament['placement']}\n\n"
            )
    
    keyboard = create_keyboard([
        ("🔙 Voltar", f"furia_game_{game.lower()}")
    ])
    
    await send_or_edit_message(
        update,
        context,
        text,
        keyboard,
        parse_mode="HTML"
    )