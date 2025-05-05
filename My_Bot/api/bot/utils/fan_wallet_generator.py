from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import io
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.utils import ImageReader
import datetime
import os

# Base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Using absolute import instead of relative import
from api.assets.fan_wallet import ASSETS_DIR, FAN_WALLET_DIR

# Definição de fallback caso a importação direta falhe
if 'ASSETS_DIR' not in locals() or 'FAN_WALLET_DIR' not in locals():
    ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"
    FAN_WALLET_DIR = ASSETS_DIR / "fan_wallet"

# Font paths
FONTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "..", "assets", "fonts")
REGULAR_FONT_PATH = os.path.join(FONTS_DIR, "Roboto-Regular.ttf")
BOLD_FONT_PATH = os.path.join(FONTS_DIR, "Roboto-Bold.ttf")

# Font sizes
FONT_SIZES = {
    "title": 38,
    "subtitle": 36,
    "label": 24,
    "value": 28,
    "small": 20
}

TEMPLATE_PATH = FAN_WALLET_DIR / "template.png"
LOGO_PATH = FAN_WALLET_DIR / "logo_carterinha.png"
FURIA_BLUE = (29, 29, 30)
FURIA_BLACK = (0, 0, 0)
TEXT_COLOR = (165, 165, 165)

# Ajustar proporções para estilo cartão de visita (85.60 × 53.98 mm)
CARD_WIDTH = 900  # Aumentado para melhor qualidade
CARD_HEIGHT = int(CARD_WIDTH * 0.6)  # Mantém proporção aproximada de cartão

def ensure_fan_wallet_dir():
    FAN_WALLET_DIR.mkdir(parents=True, exist_ok=True)

def load_fonts():
    try:
<<<<<<< HEAD
        default_font = ImageFont.truetype("arial.ttf", 36)
        title_font = ImageFont.truetype("arial.ttf", 45)  # Aumentado para melhor proporção
        info_font = ImageFont.truetype("arial.ttf", 28)
        small_font = ImageFont.truetype("arial.ttf", 20)
        return title_font, default_font, info_font, small_font
    except Exception:
=======
        # Usar fontes específicas com tamanhos definidos
        title_font = ImageFont.truetype(BOLD_FONT_PATH, FONT_SIZES["title"])
        default_font = ImageFont.truetype(REGULAR_FONT_PATH, FONT_SIZES["subtitle"])
        info_font = ImageFont.truetype(REGULAR_FONT_PATH, FONT_SIZES["value"])
        small_font = ImageFont.truetype(REGULAR_FONT_PATH, FONT_SIZES["small"])
        
        return title_font, default_font, info_font, small_font
    except Exception as e:
        # Fallback seguro - mas log do erro para diagnóstico
        print(f"Erro ao carregar fontes: {e}. Caminho das fontes: {REGULAR_FONT_PATH}, {BOLD_FONT_PATH}")
>>>>>>> 6ab730e (Ajuste do Desing da Carteira e Adição de fonts)
        return ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default(), ImageFont.load_default()

def add_rounded_corners(image, radius):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
    
    alpha = Image.new('L', image.size, 255)
    w, h = image.size
    
    # Cantos arredondados
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    
    image = image.convert("RGBA")
    image.putalpha(alpha)
    
    return image

def add_card_background(image):
    # Adiciona um gradiente sutil
    gradient = Image.new('L', image.size)
    draw = ImageDraw.Draw(gradient)
    
    for y in range(image.height):
        value = int(255 * (1 - y / image.height * 0.7))
        draw.line([(0, y), (image.width, y)], fill=value)
    
    # Aplicar bordas arredondadas
    image = add_rounded_corners(image, 40)  # Aumentado para melhor estética
    
    return image

def add_logo(template):
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH)
        
        # Diminuindo o tamanho da logo 
        logo_size = int(CARD_WIDTH * 0.12) 
        logo = logo.resize((logo_size, logo_size))
        
        # Ajustando posição para manter alinhamento adequado
        margin_x = int(CARD_WIDTH * 0.03)
        margin_y = int(CARD_HEIGHT * 0.04)
        pos_x = CARD_WIDTH - logo_size - margin_x
        pos_y = margin_y
        
        template.paste(logo, (pos_x, pos_y), mask=logo if logo.mode == 'RGBA' else None)

def add_user_info(draw, user_data, info_font, small_font):
    # Margens consistentes
    margin_left = int(CARD_WIDTH * 0.06)
    
    # Espaçamento vertical consistente
    spacing = int(CARD_HEIGHT * 0.14)
    y_pos = int(CARD_HEIGHT * 0.40)  # Aumentado
    
    # Nome completo
    nome_completo = user_data.get('first_name', 'Fã')
    if user_data.get('last_name'):
        nome_completo += " " + user_data.get('last_name')
    
    draw.text((margin_left, y_pos), "NOME:", fill=FURIA_BLACK, font=small_font)
    draw.text((margin_left, y_pos + 30), nome_completo, fill=TEXT_COLOR, font=info_font)
    
    # Username
    y_pos += spacing
    draw.text((margin_left, y_pos), "USERNAME:", fill=FURIA_BLACK, font=small_font)
    draw.text((margin_left, y_pos + 30), f"@{user_data.get('username', 'fan')}", fill=TEXT_COLOR, font=info_font)
    
    # ID do Fã
    y_pos += spacing
    draw.text((margin_left, y_pos), "ID DO FÃ:", fill=FURIA_BLACK, font=small_font)
    draw.text((margin_left, y_pos + 30), f"{user_data.get('id', '000000')}", fill=TEXT_COLOR, font=info_font)
    
    # Data de emissão no canto inferior esquerdo
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
    footer_y = CARD_HEIGHT - int(CARD_HEIGHT * 0.08)
    draw.text((margin_left, footer_y), f"Emitido em: {data_atual}", fill=TEXT_COLOR, font=small_font)
    
    # Assinatura FURIA no canto inferior direito
    furia_text = "FURIA ESPORTS OFICIAL"
    text_width = small_font.getbbox(furia_text)[2]
    draw.text((CARD_WIDTH - margin_left - text_width, footer_y), furia_text, fill=FURIA_BLACK, font=small_font)

def create_qr_code(user_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=2,
    )
    qr.add_data(f"FURIA_FAN:{user_id}")
    qr.make(fit=True)
    return qr.make_image(fill_color="white", back_color="transparent")

def add_qr_code(template, user_id, small_font):
    qr_img = create_qr_code(user_id)
    
    # Reduzindo o tamanho do QR code
    qr_size = int(CARD_HEIGHT * 0.25)  # Reduzido de 0.32 para 0.25 (25% da altura)
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Reposicionando o QR code para mais abaixo, próximo ao texto "FURIA ESPORTS OFICIAL"
    margin_x = int(CARD_WIDTH * 0.05)
    footer_y = CARD_HEIGHT - int(CARD_HEIGHT * 0.08)  # Posição Y do texto de footer
    
    # Posicionando o QR code acima do texto de footer com espaçamento adequado
    qr_x = CARD_WIDTH - qr_size - margin_x
    qr_y = footer_y - qr_size - 30  # 30px de espaço entre o QR e o texto
    
    template.paste(qr_img, (qr_x, qr_y))
    
    # Texto de verificação acima do QR code
    draw = ImageDraw.Draw(template)
    text = "VERIFICAÇÃO"
    text_width = small_font.getbbox(text)[2]
    text_x = qr_x + (qr_size - text_width) // 2  # Centralizado sobre o QR
    text_y = qr_y - 25  # Espaço acima do QR
    
    draw.text((text_x, text_y), text, fill=FURIA_BLUE, font=small_font)

def generate_fan_wallet_image(user_data):
    ensure_fan_wallet_dir()
    
    # Carrega o template ou cria uma imagem com dimensões atualizadas
    if TEMPLATE_PATH.exists():
        template = Image.open(TEMPLATE_PATH).resize((CARD_WIDTH, CARD_HEIGHT))
    else:
        template = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT))
    
    template = add_card_background(template)
    
    # Template para elementos de texto
    draw_template = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_template)
    
    title_font, default_font, info_font, small_font = load_fonts()
    
    # Título sem efeito de sombra
    margin_left = int(CARD_WIDTH * 0.06)
    title_y = int(CARD_HEIGHT * 0.05)
    
    # Primeiro título - CARTEIRA DE FÃ
<<<<<<< HEAD
    draw.text((margin_left+2, title_y+2), "CARTEIRA DE FÃ", fill=(30, 30, 30), font=title_font)
=======
>>>>>>> 6ab730e (Ajuste do Desing da Carteira e Adição de fonts)
    draw.text((margin_left, title_y), "CARTEIRA DE FÃ", fill=FURIA_BLACK, font=title_font)
    
    # Segundo título - FURIA ESPORTS 
    title_y += title_font.getbbox("CARTEIRA DE FÃ")[3] + 10  # Espaço entre os títulos
<<<<<<< HEAD
    draw.text((margin_left+2, title_y+2), "FURIA ESPORTS", fill=(30, 30, 30), font=title_font)
=======
>>>>>>> 6ab730e (Ajuste do Desing da Carteira e Adição de fonts)
    draw.text((margin_left, title_y), "FURIA ESPORTS", fill=TEXT_COLOR, font=title_font)
    
    # Informações do usuário
    add_user_info(draw, user_data, info_font, small_font)
    
    # Adiciona o layer de texto sobre o template
    template.paste(draw_template, (0,0), draw_template)
    
    add_qr_code(template, user_data.get('id', '000000'), small_font)
    add_logo(template)
    
    # Converte para RGB e salva
    template = template.convert('RGB')
    
    img_byte_array = io.BytesIO()
    template.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)
    
    return img_byte_array

def generate_fan_wallet_pdf(user_data):
    img_bytes = generate_fan_wallet_image(user_data)
    
    pdf_bytes = io.BytesIO()
    # Ajusta tamanho do PDF para proporção de cartão
    custom_size = (A6[0], A6[0] * CARD_HEIGHT / CARD_WIDTH)
    c = canvas.Canvas(pdf_bytes, pagesize=custom_size)
    
    img = ImageReader(io.BytesIO(img_bytes.getvalue()))
    
    width, height = custom_size
    c.drawImage(img, 0, 0, width=width, height=height, preserveAspectRatio=True)
    
    c.save()
    pdf_bytes.seek(0)
    
    return pdf_bytes
