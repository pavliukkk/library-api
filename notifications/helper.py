import os
import requests

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()
