# Importar componentes principais do bot
from .handlers import register_handlers
from .bot import create_bot

__all__ = [
    "create_bot",
    "register_handlers"
]
