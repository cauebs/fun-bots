from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import handler


logging.basicConfig(format='[%(asctime)s] %(name)s: %(message)s')


def error_callback(bot, update, error):
    logging.error(error)


command_handler = CommandHandler('ban', handler.voteban, pass_args=True)
message_handler = MessageHandler(Filters.all, handler.add_user)

updater = Updater(TOKEN)
updater.dispatcher.add_error_handler(error_callback)
updater.dispatcher.add_handler(command_handler)
updater.dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
