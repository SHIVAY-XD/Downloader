import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.start import start
from handlers.info import info
from handlers.download import download_and_send_video
from handlers.broadcast import broadcast

TELEGRAM_BOT_TOKEN = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'  # Replace with your actual token

# Semaphore to limit concurrent downloads
max_concurrent_downloads = 5
semaphore = asyncio.Semaphore(max_concurrent_downloads)

async def handle_download(update, context):
    video_url = update.message.text
    user_id = update.effective_user.id
    chat_id = update.message.chat_id

    async with semaphore:
        await download_and_send_video(video_url, chat_id, user_id, context)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
