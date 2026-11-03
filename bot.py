import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашого бота
TOKEN = "9006746049:AAGclepU7o8Isq6x9eOEZvbNc5YYtOEV4aI"

def extract_youtube_id(url: str) -> str:
    """Витягує чистий 11-значний ID відео з будь-якого посилання YouTube."""
    patterns = [
        r'(?:v=|\/|vi\/|youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник команди /start (спрацьовує тільки при першому запуску бота)"""
    welcome_text = (
        "Вітаю! 🤖 Цей бот призначений для генерації посилань на YouTube із гарантованим прев'ю-малюнком.\n\n"
        "Надішліть мені посилання на відео з YouTube, і у відповідь отримаєте чисте посилання, "
        "яке завжди відкриває відео з гарним прев'ю.\n\n"
        "Просто надішліть посилання у чат! 👇"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник вхідних повідомлень (посилань) - працює тихо та миттєво без привітань"""
    text = update.message.text
    
    # Шукаємо ID відео в надісланому тексті
    video_id = extract_youtube_id(text)
    
    if video_id:
        # Формуємо канонічне посилання повного формату для гарантованого прев'ю
        clean_url = f"https://www.youtube.com/watch?v={video_id}"
        await update.message.reply_text(clean_url)
    else:
        await update.message.reply_text(
            "Будь ласка, надішліть коректне посилання на відео з YouTube."
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот запущено і готово до роботи...")
    app.run_polling()