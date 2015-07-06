from lib import helps
from lib import utils


outputs = []
crontable = []
crontable.append([300, "helptimer"])


def helptimer():
    admin_channel, botname, icon_emoji = utils.setup_bot(config)
    message_attrs = {'icon_emoji': icon_emoji, 'username': botname}
    admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                    slack_client)
    halps = helps.Helps(config['redis'])
    all_halps = halps.get_all()
    text = utils.format_helps(all_halps)
    if text:
        text.insert(0, "These customers need help!")
        text = '\n'.join(text)
        outputs.append([admin_channel_id, text, message_attrs])
