from lib import helps
from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == ('!pr'):
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        # Translate channel id to channel name
        channel = data.get('channel')

        # Only allow !pr from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return

        # Translate user id to username
        user = data.get('user')
        username = utils.get_user_name(user, slack_client)

        text = data.get('text').split()
        if len(text) > 1:
            link = text[1]
        else:
            text = ("%s - to request PR help, type "
                    "`!pr <link-to-pr>`" % username)
            outputs.append([channel, text, message_attrs])
            return

        # Store pr request in Redis
        prs = helps.Helps(config['redis'])
        stored = prs.store(link, username, data.get('ts'))

        if stored:
            text = "%s needs this PR reviewed: %s" % (username, link)
            outputs.append([admin_channel, text, message_attrs])
