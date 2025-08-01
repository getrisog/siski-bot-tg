import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
KEYWORDS = os.getenv("KEYWORDS", "сиськи").split(",")
GIF_URLS_FILE = os.getenv("GIF_URLS_FILE", "gif_urls.txt")
