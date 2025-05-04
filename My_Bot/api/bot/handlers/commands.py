from telegram.ext import CommandHandler, CallbackQueryHandler

# Comandos
from .start.start_handler import cmd_start
from .furia.furia_handler import cmd_furia
from .imagem.imagem_handler import cmd_imagem

# Callbacks - Start
from .start.callbacks import callback_start, callback_loja, callback_sobre

# Callbacks - FURIA
from .furia.callbacks import (
    callback_furia,
    callback_furia_game,
    callback_furia_info,
    callback_furia_players,
    callback_furia_upcoming,
    callback_furia_results,
    callback_furia_tournaments,
    callback_furia_refresh
)

# Callbacks - Imagem
from .imagem.callbacks import (
    callback_imagens,
    callback_imagem_time,
    callback_imagem_logo,
    callback_imagem_mobile,
    callback_imagem_desktop
)

def register_handlers(application):
    """Registra todos os handlers do bot"""
    
    # Registra handlers de comando
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("furia", cmd_furia))
    application.add_handler(CommandHandler("imagem", cmd_imagem))

    # Registra callbacks - Start
    application.add_handler(CallbackQueryHandler(callback_start, pattern="^start$"))
    application.add_handler(CallbackQueryHandler(callback_loja, pattern="^loja$"))
    application.add_handler(CallbackQueryHandler(callback_sobre, pattern="^sobre$"))

    # Registra callbacks - FURIA
    application.add_handler(CallbackQueryHandler(callback_furia, pattern="^furia$"))
    application.add_handler(CallbackQueryHandler(callback_furia_game, pattern="^furia_game_"))
    application.add_handler(CallbackQueryHandler(callback_furia_info, pattern="^furia_info_"))
    application.add_handler(CallbackQueryHandler(callback_furia_players, pattern="^furia_players_"))
    application.add_handler(CallbackQueryHandler(callback_furia_upcoming, pattern="^furia_upcoming_"))
    application.add_handler(CallbackQueryHandler(callback_furia_results, pattern="^furia_results_"))
    application.add_handler(CallbackQueryHandler(callback_furia_tournaments, pattern="^furia_tournaments_"))
    application.add_handler(CallbackQueryHandler(callback_furia_refresh, pattern="^furia_refresh_"))

    # Registra callbacks - Imagem
    application.add_handler(CallbackQueryHandler(callback_imagens, pattern="^imagens$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_time, pattern="^imagem_time$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_logo, pattern="^imagem_logo$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_mobile, pattern="^imagem_mobile$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_desktop, pattern="^imagem_desktop$"))