import os
import aiohttp
import tempfile
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.user_data import check_channel_membership

# Semaphore to limit the number of concurrent downloads
max_concurrent_downloads = 5
semaphore = asyncio.Semaphore(max_concurrent_downloads)

async def download_and_send_video(video_url: str, chat_id: int, user_id: int, context):
    if not await check_channel_membership(user_id, context):
        keyboard = [
            [InlineKeyboardButton("Join Channel", url="https://t.me/Itsteachteam")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id, 
            text="<b>Before sending the link, please join our channel first.</b>\n\n<i>After joining, send the link again.</i>", 
            parse_mode='HTML', 
            reply_markup=reply_markup
        )
        return

    # Send processing message
    downloading_message = await context.bot.send_message(chat_id=chat_id, text="Processing your request... Please wait.")

    # Download video within semaphore context
    async with semaphore:
        await download_video(video_url, chat_id, context, downloading_message)

async def download_video(video_url: str, chat_id: int, context, downloading_message):
    api_url = f'https://tele-social.vercel.app/down?url={video_url}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                content = await response.json()

        platform = content.get('platform', 'Unknown')
        video_link = content['data'].get('video')
        title = content['data'].get('title', f"{platform} Video")

        if not video_link or not video_link.startswith("http"):
            await context.bot.send_message(chat_id=chat_id, text="Received an invalid video link.")
            return

        # Download the video
        async with aiohttp.ClientSession() as session:
            async with session.get(video_link) as response:
                response.raise_for_status()
                video_data = await response.read()

        # Save the video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_data)
            temp_file_path = temp_file.name

        # Send the video file to Telegram
        with open(temp_file_path, "rb") as f:
            await context.bot.send_video(chat_id=chat_id, video=f, caption=title)

        # Clean up the downloaded file
        os.remove(temp_file_path)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Failed to download video. Please try again later.")
        print(f"Error: {e}")
    finally:
        # Delete the processing message
        await context.bot.delete_message(chat_id=chat_id, message_id=downloading_message.message_id)
