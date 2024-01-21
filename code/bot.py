import os
import telebot
import requests
from time import sleep
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
PLOT_PATH = os.environ.get("PLOT_PATH")
bot = telebot.TeleBot(BOT_TOKEN)

def main():
    filenames = [
        "Total Annual Blood Donations.png",
        "Average Daily Blood Donations.png",
        "Donation Retention Percentage.png",
        "State Daily Donation Breakdown (Johor, Kedah, Kelantan, Melaka).png",
        "State Daily Donation Breakdown (Negeri Sembilan, Pahang, Perak, Pulau Pinang).png",
        "State Daily Donation Breakdown (Sabah, Sarawak, Selangor, Terengganu).png",
        "State Daily Donation Breakdown (W.P. Kuala Lumpur).png",
        "State Donation Breakdown (Johor, Kedah, Kelantan, Melaka).png",
        "State Donation Breakdown (Negeri Sembilan, Pahang, Perak, Pulau Pinang).png",
        "State Donation Breakdown (Sabah, Sarawak, Selangor, Terengganu).png",
        "State Donation Breakdown (W.P. Kuala Lumpur).png",
    ]
    message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"
    current_date = datetime.now(ZoneInfo("Asia/Kuala_Lumpur"))
    bot.send_message(
        chat_id=CHAT_ID,
        text=f"Malaysia's blood donation statistics for {current_date.date().strftime('%d-%m-%Y')}"
    )

    for name in filenames:
        bot.send_document(
            chat_id=CHAT_ID,
            document=open(f"{PLOT_PATH}/{name}", "rb"),
            caption=name.replace(".png", "")
        )
        sleep(1)
    return


if __name__ == "__main__":
    main()