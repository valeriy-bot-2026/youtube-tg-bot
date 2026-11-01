import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from googleapiclient.discovery import build
import re

# Ваші дані налаштовано
TELEGRAM_TOKEN = "9006746049:AAGclepU7o8Isq6x9eOEZvbNc5YYtOEV4aI"
YOUTUBE_API_KEY = "AIzaSyAhoRtnx7fqPF4ThB0wEQDdGskK0pjxo3E"
PLAYLIST_ID = "PLR3hr1JiDRiQ"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функція додавання та негайного очищення відео з плейлиста
def add_and_clear_video(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        # 1. Додаємо відео в плейлист для генерації прев'ю
        insert_response = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': PLAYLIST_ID,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()
        
        # Отримуємо унікальний ID елемента всередині плейлиста
        playlist_item_id = insert_response['id']
        
        # 2. Одразу видаляємо його з плейлиста, щоб він не захаращувався
        youtube.playlistItems().delete(
            id=playlist_item_id
        ).execute()
        
        return True
    except Exception as e:
        logging.error(f"Помилка при роботі з плейлистом YouTube: {e}")
        return False

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/|v\/|youtu\.be\/|watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    video_id = extract_video_id(text)
    
    if video_id:
        # Додаємо і одразу вичищаємо плейлист
        success = add_and_clear_video(video_id)
        if success:
            await update.message.reply_text(f"✅ Прев'ю активовано! Посилання для публікації:\nhttps://youtu.be/{video_id}")
        else:
            await update.message.reply_text("⚠️ Посилання розпізнано, але сталася помилка при зверненні до YouTube API.")
    else:
        await update.message.reply_text("Будь ласка, надішліть коректне посилання на YouTube-відео.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот запущено і працює 24/7 з автоматичним очищенням плейлиста!")
    application.run_polling()

if __name__ == '__main__':
    main()