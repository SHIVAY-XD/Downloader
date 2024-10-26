import json

USER_DATA_FILE = "user_details.json"

# Load user details from a JSON file
try:
    with open(USER_DATA_FILE, "r") as file:
        user_details = json.load(file)
except FileNotFoundError:
    user_details = []

def save_user_details():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_details, file, indent=4)

async def check_channel_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_member = await context.bot.get_chat_member('@itsteachteam', user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False

