
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing!")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            "🟢 GREEN",
            callback_data="green",
            style="success"
        ),
        InlineKeyboardButton(
            "🔴 RED",
            callback_data="red",
            style="danger"
        ),
        InlineKeyboardButton(
            "🔵 BLUE",
            callback_data="blue",
            style="primary"
        ),
        InlineKeyboardButton(
            "💜 PURPLE",
            callback_data="purple"
        )
    )

    bot.send_message(
        message.chat.id,
        "✨ WELCOME BHAI! ✨\n\n"
        "👇 Apna button select kar:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    responses = {
        "green": "🟢 Green button clicked!",
        "red": "🔴 Red button clicked!",
        "blue": "🔵 Blue button clicked!",
        "purple": "💜 Purple button clicked!"
    }

    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        responses.get(call.data, "Button clicked!")
    )


print("Bot is running...")
bot.infinity_polling()
