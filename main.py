from telegram.ext import ApplicationBuilder
from handlers.start_handler import start
from handlers.info_handler import info
from handlers.download_handler import handle_message
from handlers.broadcast_handler import broadcast

TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
