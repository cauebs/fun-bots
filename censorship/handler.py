import logging
from telegram import TelegramError
from blacklist import WORDS


WARNING = "I'm sorry, {}, but you used a word not allowed in this chat." + \
          "The administrators have been notified."
ADMIN_MESSAGE = "{} has sent a message with a forbidden word. Just saying."


def callback(bot, update):
    message = update.message

    for word in WORDS:
        if word in message.text.lower():
            censor(bot, update)


def censor(bot, update):
    message = update.message
    chat_id = message.chat_id
    username = message.from_user.first_name

    bot.delete_message(chat_id, message.message_id)
    bot.send_message(chat_id, WARNING.format(username))

    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        try:
            bot.send_message(admin.user.id,
                             ADMIN_MESSAGE.format(username))
        except TelegramError:
            logging.debug(f"Admin is a bot. User id: {admin.user.id}")
