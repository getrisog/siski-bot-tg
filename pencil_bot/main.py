import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from pencil_bot.config import TELEGRAM_TOKEN
from pencil_bot.handlers import handle_message, help_command, start, status, test_command

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function to start the bot"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set!")
        return

    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("test", test_command))

    # Handler for all text messages (including groups)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.UpdateType.EDITED_MESSAGE, handle_message)
    )

    # Start the bot
    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
