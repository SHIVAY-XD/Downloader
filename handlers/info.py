from telegram import Update
from telegram.ext import ContextTypes

ADMIN_USER_IDS = [6744775967]

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_USER_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    total_users = len(user_details)  # Assuming user_details is imported from utils
    await update.message.reply_text(f"Total users in the bot: {total_users}")

