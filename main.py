import asyncio
from concurrent.futures import ThreadPoolExecutor
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.start import start  # Importing directly
from handlers.info import info  # Importing directly
from handlers.download import download_and_send_video  # Importing directly
from handlers.broadcast import broadcast  # Importing directly

TELEGRAM_BOT_TOKEN = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=4)  # Adjust as needed

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

async def handle_download(update, context):
    video_url = update.message.text
    user_id = update.effective_user.id
    chat_id = update.message.chat_id

    await download_and_send_video(video_url, chat_id, user_id, context)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))  # Using the new handler
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
