import dataset
from math import log, ceil


def voteban(bot, update, args):
    chat = update.message.chat
    user = update.message.from_user

    db = dataset.connect('sqlite:///ban.db')
    users = db.get_table('users', primary_id='id')

    if not args:
        update.message.reply_text("You need to tell me who you want to ban :)")
        return

    target = users.find_one(username=args[0].replace('@', ''))

    if not target:
        update.message.reply_text("I'm sorry, but I haven't met this user :(")
        return

    target_member = bot.get_chat_member(chat.id, target['id'])

    if not target_member:
        update.message.reply_text("I don't think that user is in this group :/")
        return

    if target_member.status in ("left", "kicked"):
        update.message.reply_text("That user is not in this group anymore :/")
        return

    if target_member.status in ("creator", "administrator"):
        update.message.reply_text("I would be in trouble if I banned an admin!")
        return

    votes = db.get_table('votes')

    voted = votes.find_one(
        chat_id=chat.id,
        target_id=target['id'],
        voter_id=user.id
    )

    if not voted:
        votes.insert({
            'chat_id': chat.id,
            'target_id': target['id'],
            'voter_id': user.id
        })

    member_count = bot.get_chat_members_count(chat.id)
    quorum = ceil(2 * log(member_count, 10)**2)

    tally = votes.count(target_id=target['id'], chat_id=chat.id)

    update.message.reply_text(
        "Ban {}/{} - {}".format(tally, quorum, target['first_name'])
    )

    if tally == quorum:

        bot.kick_chat_member(chat.id, target['id'])
        votes.delete(target_id=target['id'], chat_id=chat.id)


def add_user(bot, update):
    user = update.message.from_user

    db = dataset.connect('sqlite:///ban.db')
    table = db.get_table('users', primary_id='id')

    if not table.find_one(id=user.id):
        table.upsert({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, ['id'])
