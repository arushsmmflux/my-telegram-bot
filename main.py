
import os
import telebot

TOKEN = os.getenv("8871548094:AAGmIcQtd6MEc_qj2NoCkDj8MvIRD5uilvI")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello bhai! ❤️ Bot successfully working hai!"
    )

print("Bot is running...")
bot.infinity_polling()
