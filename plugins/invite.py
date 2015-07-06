from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').startswith('!invite'):
        text = data.get('text').split(' ')
        channel = data.get('channel')

        # Setup plugin
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        # Only allow !invite from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return

        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        if len(text) > 1:
            invite_channel = text[1].strip('#')
        else:
            text = ("%s - to join a channel or private group type "
                    "`!invite <channel/group>`" % username)
            outputs.append([channel, text, message_attrs])
            return
        invite_channel_id = utils.get_channel_id_by_name(invite_channel,
                                                         slack_client)
        invite = utils.invite_user(user, invite_channel_id, slack_client)
        if invite['ok']:
            text = "Invited %s to %s channel." % (username, invite_channel)
        else:
            text = ("Failed to invite %s to %s"
                    " channel - %s" % (username, invite_channel,
                                       invite.get('error', 'Unknown error!')))
        logging.info(text)
        print(text)
        outputs.append([channel, text, message_attrs])
