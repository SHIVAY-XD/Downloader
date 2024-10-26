import os
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.user_data import check_channel_membership

async def download_and_send_video(video_url: str, chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE):
    if not await check_channel_membership(user_id, context):
        keyboard = [
            [
                InlineKeyboardButton("Join Channel", url="https://t.me/Itsteachteam"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=chat_id, text="<b>Before sending the link, please join our channel first.</b>\n\n<i>After joining, send the link again.</i>", parse_mode='HTML', reply_markup=reply_markup)
        return

    downloading_message = await context.bot.send_message(chat_id=chat_id, text="Processing your request... Please wait.")

    # API call and download logic goes here

    # Clean up and response logic

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    video_link = update.message.text
    await download_and_send_video(video_link, update.message.chat_id, update.message.from_user.id, context)

