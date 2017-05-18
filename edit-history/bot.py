from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import handler


logging.basicConfig(format='[%(asctime)s] %(name)s: %(message)s')


def error_callback(bot, update, error):
    logging.error(error)


command_handler = CommandHandler('history', handler.show_history)
message_handler = MessageHandler(Filters.text,
                                 handler.save_message,
                                 allow_edited=True)

updater = Updater(TOKEN)
updater.dispatcher.add_error_handler(error_callback)
updater.dispatcher.add_handler(message_handler)
updater.dispatcher.add_handler(command_handler)

updater.start_polling()
updater.idle()
