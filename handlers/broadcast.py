from telegram import Update
from telegram.ext import ContextTypes
from utils.user_data import user_details

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id not in [6744775967]:  # Replace with your admin check
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if update.message.reply_to_message:
        message_to_forward = update.message.reply_to_message
        
        successful = 0
        failed = 0
        
        for user in user_details:
            user_id = user['id']
            try:
                await context.bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=message_to_forward.chat.id,
                    message_id=message_to_forward.message_id
                )
                successful += 1
            except Exception as e:
                print(f"Failed to forward message to {user_id}: {e}")
                failed += 1
        
        total_users = len(user_details)
        await update.message.reply_text(f"Broadcast complete:\n\nSuccessfully sent: {successful}\nFailed: {failed}\nTotal users: {total_users}")
    else:
        await update.message.reply_text("Please reply to a message to broadcast it.")

