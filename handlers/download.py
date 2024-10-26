import os
import aiohttp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.user_data import check_channel_membership

async def download_and_send_video(video_url: str, chat_id: int, user_id: int, context):
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

    # Use run_in_executor for blocking download function
    await run_in_executor(download_video, video_url, chat_id, context)

async def run_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)

def download_video(video_url, chat_id, context):
    api_url = f'https://tele-social.vercel.app/down?url={video_url}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                response.raise_for_status()
                content = await response.json()

        platform = content.get('platform')
        video_link = None
        title = None
        image_url = None

        if platform in ["YouTube", "Instagram", "Facebook"]:
            video_link = content['data'].get('video')
            title = content['data'].get('title', f"{platform} Video")
            image_url = content['data'].get('image')

        if not video_link or not video_link.startswith("http"):
            await context.bot.send_message(chat_id=chat_id, text="Received an invalid video link.")
            return

        # Download the video
        async with aiohttp.ClientSession() as session:
            async with session.get(video_link) as response:
                response.raise_for_status()
                video_data = await response.read()

        # Save the video to a temporary file
        temp_file_path = "downloaded_video.mp4"
        with open(temp_file_path, "wb") as f:
            f.write(video_data)

        # Send the video file to Telegram
        with open(temp_file_path, "rb") as f:
            await context.bot.send_video(chat_id=chat_id, video=f, caption=f"{title}", reply_markup=reply_markup)

        # Optionally delete the file after sending
        os.remove(temp_file_path)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Failed to download video. Please try again later.")
        print(f"Error: {e}")

