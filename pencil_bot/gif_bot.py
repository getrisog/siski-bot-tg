import logging
import random
import tempfile
from pathlib import Path

import aiohttp
import pymorphy3

from pencil_bot.config import GIF_URLS_FILE, KEYWORDS

logger = logging.getLogger(__name__)

# Initialize morphological analyzer
morph = pymorphy3.MorphAnalyzer()


class GifBot:
    def __init__(self):
        self.keywords = [kw.strip().lower() for kw in KEYWORDS]
        self.gif_urls = self._load_gif_urls()

        # Normalize keywords
        self.normalized_keywords = self._normalize_keywords()
        logger.info(f"Normalized keywords: {self.normalized_keywords}")
        logger.info(f"Available GIF URLs: {len(self.gif_urls)}")

    def _normalize_keywords(self):
        """Normalizes keywords to their base form"""
        normalized = []
        for keyword in self.keywords:
            # Get normal form of the word
            parsed = morph.parse(keyword)[0]
            normal_form = parsed.normal_form
            normalized.append(normal_form)
            logger.info(f"Keyword '{keyword}' -> normal form '{normal_form}'")
        return normalized

    def _load_gif_urls(self):
        """Loads GIF URLs from file"""
        urls = []
        gif_file = Path(GIF_URLS_FILE)

        if not gif_file.exists():
            logger.warning(f"File {GIF_URLS_FILE} not found!")
            return urls

        try:
            with open(gif_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        urls.append(line)
                        logger.debug(f"Loaded GIF URL: {line}")

            logger.info(f"Loaded {len(urls)} GIF URLs from file {GIF_URLS_FILE}")
        except Exception as e:
            logger.error(f"Error loading GIF URLs from {GIF_URLS_FILE}: {e}")

        return urls

    def get_random_gif_url(self):
        """Returns a random GIF URL"""
        if not self.gif_urls:
            return None
        return random.choice(self.gif_urls)

    async def download_gif(self, url):
        """Downloads GIF from URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Create temporary file
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
                        content = await response.read()
                        temp_file.write(content)
                        temp_file.close()
                        logger.info(f"Downloaded GIF: {url}")
                        return temp_file.name
                    else:
                        logger.error(f"Error downloading GIF: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Error downloading GIF {url}: {e}")
            return None

    def check_keywords(self, text):
        """Checks for keywords in text with normalization"""
        text_lower = text.lower()
        found_keywords = []
        found_siski = False

        # Split text into words
        words = text_lower.split()

        for word in words:
            # Clean word from punctuation
            clean_word = "".join(c for c in word if c.isalnum())
            if not clean_word:
                continue

            # Check special word "сиськи"
            if clean_word == "сиськи" or clean_word == "сиська":
                found_siski = True
                found_keywords.append("сиськи")
                logger.info("Found special word: 'сиськи'")
                continue

            # Normalize word
            try:
                parsed = morph.parse(clean_word)[0]
                normal_form = parsed.normal_form
                logger.debug(f"Word '{clean_word}' -> normal form '{normal_form}'")

                # Check if normal form is in keywords
                if normal_form in self.normalized_keywords:
                    # Find original keyword for display
                    original_keyword = self.keywords[self.normalized_keywords.index(normal_form)]
                    found_keywords.append(original_keyword)
                    logger.info(f"Found keyword: '{original_keyword}' (normal form: '{normal_form}')")
            except Exception as e:
                logger.debug(f"Error normalizing word '{clean_word}': {e}")
                # If normalization failed, check as is
                if clean_word in self.keywords:
                    found_keywords.append(clean_word)
                    logger.info(f"Found keyword without normalization: '{clean_word}'")

        return list(set(found_keywords)), found_siski  # Remove duplicates and return siski flag
