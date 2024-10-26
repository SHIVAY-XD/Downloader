from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.user_data import save_user_details, user_details

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name
    user_name = update.effective_user.username

    if not any(user['id'] == user_id for user in user_details):
        user_info = {
            "id": user_id,
            "name": user_first_name,
            "username": user_name
        }
        user_details.append(user_info)
        save_user_details()

        await context.bot.send_message(chat_id='@userdatass', 
                                       text=f"New user started the bot:\nName: {user_first_name}\nUsername: {user_name}\nUser ID: {user_id}")

    welcome_message = (
        f"Hello {user_first_name} 👋!\n\n"
        "<b>I am a simple bot to download videos, reels, and photos from Instagram links.</b>\n\n"
        "<i>This bot is the fastest bot you have ever seen in Telegram.</i>\n\n"
        "<b>‣ Just send me your link🔗.</b>\n\n"
        "<b>Developer: @xdshivay</b> ❤"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("Channel", url="https://t.me/Itsteachteam"),
            InlineKeyboardButton("Group", url="https://t.me/Itsteachteamsupport")
        ], 
        [
            InlineKeyboardButton("Developer", url="https://t.me/XDSHlVAY"), 
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, parse_mode='HTML', reply_markup=reply_markup)

