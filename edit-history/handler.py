import dataset


def save_message(bot, update):
    message = update.message or update.edited_message
    date = message.edit_date or message.date

    db = dataset.connect('sqlite:///history.db')
    table = db.get_table('messages')

    table.insert({
        'update_id': update.update_id,
        'chat_id': message.chat_id,
        'message_id': message.message_id,
        'date': date,
        'text': message.text
    })


def show_history(bot, update):
    chat_id = update.message.chat_id
    message_id = update.message.reply_to_message.message_id

    db = dataset.connect('sqlite:///history.db')
    table = db.get_table('messages')

    history = list(table.find(message_id=message_id, chat_id=chat_id))
    history.sort(key=lambda x: x['update_id'])

    if len(history) > 1:
        text = '\n'.join(m['date'].strftime('[%H:%M:%S] ') + m['text'] for m in history)
        update.message.reply_text(text)
    else:
        update.message.reply_text('There are no recorded edits for this message.')
