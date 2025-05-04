from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def create_keyboard(buttons):
    #Cria um teclado inline a partir de uma lista de botões
    # buttons: lista de tuplas (texto, callback_data ou url)
    keyboard = []
    for row in buttons:
        if isinstance(row, tuple):
            row = [row]
        row_buttons = []
        for text, data in row:
            if isinstance(data, str) and data.startswith('http'):
                button = InlineKeyboardButton(text=text, url=data)
            else:
                button = InlineKeyboardButton(text=text, callback_data=data)
            row_buttons.append(button)
        keyboard.append(row_buttons)
    return InlineKeyboardMarkup(keyboard)

def create_back_button(callback_data="start"):
    # Cria um teclado com apenas o botão de voltar
    return create_keyboard([("🔙 Voltar ao Menu", callback_data)])
