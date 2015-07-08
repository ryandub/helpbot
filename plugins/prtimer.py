from lib import helps
from lib import utils


outputs = []
crontable = []
crontable.append([300, "prtimer"])


def prtimer():
    prs = helps.Helps(config['redis'])
    all_prs = prs.get_all()
    text = utils.format_prs(all_prs)
    if text:
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        text.insert(0, "These Pull Requests need review!")
        text.append("To acknowledge PR requests, type `!ack-pr <link_to_pr>`")
        text = '\n'.join(text)
        outputs.append([admin_channel_id, text, message_attrs])
