from lib import helps
from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split(' ')[0] == '!ack':
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}
        channel = data.get('channel')

        # Only allow !ack from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return

        acktext = data['text'].split(' ')
        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        if len(acktext) > 1:
            ack_channel = acktext[1].strip('#')
        else:
            text = ("%s - to acknowledge help requests, type "
                    "`!ack <channel>`" % username)
            outputs.append([channel, text, message_attrs])
            return
        ack_channel_id = utils.get_channel_id_by_name(ack_channel,
                                                      slack_client)
        invite = utils.invite_user(user, ack_channel_id, slack_client)
        if invite['ok']:
            logging.info("Invited %s to %s channel." % (username, ack_channel))
        else:
            text = ("Failed to invite %s to %s"
                    " channel - %s" % (username, ack_channel,
                                       invite.get('error', 'Unknown error!')))
            logging.info(text)
            outputs.append([channel, text, message_attrs])
            return
        halps = helps.Helps(config['redis'])
        halps.ack(ack_channel)
        text = ":angel: %s has acknowledged help for %s!" % (username,
                                                             ack_channel)
        outputs.append([channel, text, message_attrs])
