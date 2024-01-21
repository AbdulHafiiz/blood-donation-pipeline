import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def main():
    files_locations = [filename for filename in os.listdir("./data") if filename.endswith(".png")]
    message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?"
    data = {
        "message": "Here are the data plots:",
        "chat_id": CHAT_ID,
        "parse_mode": "HTML"
    }
    files = {
        "document": open(f"./data/{files_locations[0]}", "rb")
    }
    result = requests.post(message_url, data=data, files=files, stream=True)
    return result.json()


if __name__ == "__main__":
    print(main())