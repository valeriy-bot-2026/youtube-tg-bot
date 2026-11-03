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
    """Витягує чистий 11-значний ID відео з будь-якого посилання YouTube (зокрема з плейлистів та трекінгових параметрів)."""
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
    """Обробник команди /start"""
    await update.message.reply_text(
        "Вітаю! Я готовий до роботи. Надішліть мені будь-яке посилання на YouTube-відео, "
        "і я перетворю його на ідеальне посилання з прев'ю для публікацій."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробник вхідних повідомлень (посилань)"""
    text = update.message.text
    
    # Шукаємо ID відео в надісланому тексті
    video_id = extract_youtube_id(text)
    
    if video_id:
        # Формуємо канонічне посилання повного формату, яке гарантовано генерує прев'ю в Telegram
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