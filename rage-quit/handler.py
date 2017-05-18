from random import choice


REPLIES = ["stop it, {}",
           "whats wrong with you, {}?",
           "fuck off, {}",
           "{}, can't you understand i don't want to be here?"]


def callback(bot, update):
    message = update.message
    new_member = message.new_chat_member
    from_user = message.from_user.first_name.lower()

    if new_member:
        if new_member.id == bot.get_me().id:
            text = choice(REPLIES).format(from_user)
            message.reply_text(text)
            bot.leave_chat(message.chat_id)
