import telebot

from app.core.config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    bot.reply_to(message, 'Hi! Please Use the mini app')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
