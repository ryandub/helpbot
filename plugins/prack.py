from lib import helps
from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split(' ')[0] == '!ack-pr':
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}
        channel = data.get('channel')

        # Only allow !ack-pr from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return

        acktext = data['text'].split(' ')
        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        if len(acktext) > 1:
            ack_pr = acktext[1]
        else:
            text = ("%s - to acknowledge PR requests, type "
                    "`!ack-pr <link_to_pr>`" % username)
            outputs.append([channel, text, message_attrs])
            return

        prs = helps.Helps(config['redis'])
        prs.ack(ack_pr)
        text = ":angel: %s has acknowledged PR review for %s!" % (username,
                                                                  ack_pr)
        outputs.append([channel, text, message_attrs])
