import os
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def send_document(message=None, file=None, filename=None):
    if message:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )
    if file:
        bot.send_photo(
            chat_id=CHAT_ID,
            photo=file,
            caption=filename.replace(".png", "") if filename else None
        )
    return


if __name__ == "__main__":
    pass