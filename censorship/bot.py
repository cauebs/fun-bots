from telegram.ext import Updater, MessageHandler, Filters
import logging
import handler


logging.basicConfig(format='[%(asctime)s] %(name)s: %(message)s')


def error_callback(bot, update, error):
    logging.error(error)


message_handler = MessageHandler(Filters.text,
                                 handler.callback)

updater = Updater(TOKEN)
updater.dispatcher.add_error_handler(error_callback)
updater.dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
