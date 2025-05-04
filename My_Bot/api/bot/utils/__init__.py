# Importar utilitários para facilitar o acesso
from .scraper import scraper  # This now imports the modular scraper instance
from .keyboard import create_keyboard, create_back_button
from .message import send_message, edit_message, send_image, send_or_edit_message

__all__ = [
    "scraper",
    "create_keyboard",
    "create_back_button",
    "send_message",
    "edit_message",
    "send_image",
    "send_or_edit_message"
]