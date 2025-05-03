from telegram.ext import CommandHandler, CallbackQueryHandler

# Comandos
from .start.start_handler import cmd_start
from .campeonato.campeonato_handler import cmd_campeonato
from .imagem.imagem_handler import cmd_imagem

# Callbacks - Start
from .start.callbacks import callback_start, callback_loja, callback_sobre

# Callbacks - Campeonato
from .campeonato.callbacks import (
    callback_campeonatos,
    callback_proximos_campeonatos,
    callback_resultados,
    callback_jogos_futuros,
    callback_resumo
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
    application.add_handler(CommandHandler("campeonato", cmd_campeonato))
    application.add_handler(CommandHandler("imagem", cmd_imagem))

    # Registra callbacks - Start
    application.add_handler(CallbackQueryHandler(callback_start, pattern="^start$"))
    application.add_handler(CallbackQueryHandler(callback_loja, pattern="^loja$"))
    application.add_handler(CallbackQueryHandler(callback_sobre, pattern="^sobre$"))

    # Registra callbacks - Campeonato
    application.add_handler(CallbackQueryHandler(callback_campeonatos, pattern="^campeonatos$"))
    application.add_handler(CallbackQueryHandler(callback_proximos_campeonatos, pattern="^proximos_campeonatos$"))
    application.add_handler(CallbackQueryHandler(callback_resultados, pattern="^resultados$"))
    application.add_handler(CallbackQueryHandler(callback_jogos_futuros, pattern="^jogos_futuros$"))
    application.add_handler(CallbackQueryHandler(callback_resumo, pattern="^resumo$"))

    # Registra callbacks - Imagem
    application.add_handler(CallbackQueryHandler(callback_imagens, pattern="^imagens$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_time, pattern="^imagem_time$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_logo, pattern="^imagem_logo$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_mobile, pattern="^imagem_mobile$"))
    application.add_handler(CallbackQueryHandler(callback_imagem_desktop, pattern="^imagem_desktop$"))