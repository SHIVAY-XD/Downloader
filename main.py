from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters  # Add CommandHandler and MessageHandler
from handlers.start import start
from handlers.info import info
from handlers.download import handle_message
from handlers.broadcast import broadcast

TELEGRAM_BOT_TOKEN = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
