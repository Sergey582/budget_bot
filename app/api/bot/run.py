import telebot
from telebot import types
from telebot.types import WebAppInfo

from app.core.config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    markup = types.InlineKeyboardMarkup()

    button = types.InlineKeyboardButton(
        "Add spending",
        web_app=WebAppInfo(url="https://sergey582.github.io/budget_bot/"),
    )

    markup.add(button)
    bot.reply_to(message, 'Please tap the button below to add your spending!', reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
