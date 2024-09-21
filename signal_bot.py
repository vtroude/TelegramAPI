import requests

from telegram       import Update
from telegram.ext   import Application, MessageHandler, CallbackContext

from function       import get_signal

# Your bot token from @BotFather
bot_token = '7640093061:AAFaD-ybDlRnytPYHGjazRcqwcvbIqtizMA'

# Your Flask API endpoint to save messages
api_endpoint = 'http://100.64.100.6:5000/post_signal'

# Function to handle and print new messages
async def message_handler(update: Update, context: CallbackContext):
    #if update.channel_post:  # Checks if the update is from a channel
    message = update.channel_post or update.message
    if (("TestChannel" in message.chat.title or "AstroPack" in message.chat.title)
        and ("TestChannel" in message.chat.username or "AstroPack" in message.chat.username)):

        try:
            signal  = get_signal(message.text, message.date.isoformat())
            response = requests.post(api_endpoint, json=signal)
            response.raise_for_status()
            print(f"Message sent to API: {response.json()}")
            print(signal)
            print("-" * 40)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to API: {e}")

def main():
    # Create the Application with your bot's token
    application = Application.builder().token(bot_token).build()

    # Add handler to process messages from the channel
    application.add_handler(MessageHandler(None, message_handler)) # filters.Chat(username=channel_username) & filters.TEXT

    # Start the Bot
    print(f"Bot started! Listening for new messages in AstroPack...")
    application.run_polling()

if __name__ == '__main__':
    main()