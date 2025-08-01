import logging

from telegram import Update
from telegram.ext import ContextTypes

from pencil_bot.config import GIF_URLS_FILE
from pencil_bot.gif_bot import GifBot

logger = logging.getLogger(__name__)

# Create bot instance
bot = GifBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    welcome_message = """
🤖 Привет! Я сиськобот пенсил.

🔑 Ключевые слова: {}
""".format(", ".join(bot.keywords))

    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    help_text = """
📖 Справка по использованию бота:

🔑 Ключевые слова: {}
🎬 Доступных GIF-ссылок: {}

💡 Просто напиши сообщение с любым из ключевых слов, и я отправлю случайную GIF-анимацию!
""".format(", ".join(bot.keywords), len(bot.gif_urls))

    await update.message.reply_text(help_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for all text messages"""
    if not update.message.text:
        return

    # Check for keywords
    found_keywords, found_siski = bot.check_keywords(update.message.text)

    if found_keywords:
        logger.info(f"Found keywords: {found_keywords}")

        # Get random GIF URL
        gif_url = bot.get_random_gif_url()
        if gif_url:
            try:
                # Download GIF
                gif_file = await bot.download_gif(gif_url)
                if gif_file:
                    # Form caption
                    caption = ""

                    # If "сиськи" word found, add funny response
                    if found_siski:
                        caption += "😏 Правильно! Сиськи - это всегда хорошо!"
                    else:
                        # If other keywords found, add funny response
                        caption += f"🤪 Не {', '.join(found_keywords)}, а сиськи!"

                    # Send GIF
                    with open(gif_file, "rb") as gif:
                        await update.message.reply_animation(animation=gif, caption=caption)
                    logger.info(f"Sent GIF: {gif_url}")

                    # Delete temporary file
                    import os

                    os.unlink(gif_file)
                else:
                    await update.message.reply_text("❌ Error downloading GIF")
            except Exception as e:
                logger.error(f"Error sending GIF: {e}")
                await update.message.reply_text("❌ Error sending GIF")
        else:
            await update.message.reply_text("❌ No available GIF URLs")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /status command to check bot status"""
    status_text = f"""
📊 Bot status:

🔑 Keywords: {len(bot.keywords)}
🎬 Available GIF URLs: {len(bot.gif_urls)}
📂 GIF URLs file: {GIF_URLS_FILE}
"""
    await update.message.reply_text(status_text)


async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /test command to test bot functionality"""
    test_message = f"""
🧪 Bot test:

✅ Bot is working
🎬 Available GIF URLs: {len(bot.gif_urls)}
🔑 Keywords: {", ".join(bot.keywords)}
🔤 Normalized keywords: {", ".join(bot.normalized_keywords)}
💬 Chat type: {update.effective_chat.type}
👤 User: {update.effective_user.id if update.effective_user else "Unknown"}

💡 Bot now understands different word forms!
   For example: "коты" -> "кот", "собаки" -> "собака"
"""
    await update.message.reply_text(test_message)
