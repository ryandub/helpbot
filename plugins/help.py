from lib import helps
from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == '!help':
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        # Translate channel id to channel name
        channel = data.get('channel')
        channel_name = utils.get_channel_name(channel, slack_client)

        # Translate user id to username
        user = data.get('user')
        username = utils.get_user_name(user, slack_client)

        # Store help request in Redis
        halps = helps.Helps(config['redis'])
        stored = halps.store(channel_name, username, data.get('ts'))

        if stored:
            text = "%s needs help in %s!" % (username, channel_name)
            outputs.append([admin_channel, text, message_attrs])

        text = ("Thanks %s, your help request has been received."
                " A DevOps Support Racker will be with you shortly." %
                username)
        outputs.append([channel, text, message_attrs])
