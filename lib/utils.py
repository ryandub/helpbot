import arrow
import json


def _extract_id(name, items):
    for item in items:
        if item['name'] == name:
            return item['id']
    return None


def format_helps(helps):
    text = []
    for halp in helps:
        halp = json.loads(halp)
        channel = halp.keys()[0]
        user = halp[channel]['user']
        ts = arrow.get(halp[channel]['timestamp'])
        t = ":fire: @%s needs halp in %s - %s" % (user, channel, ts.humanize())
        text.append(t)
    return text


def get_channels(slack_client):
    return json.loads(slack_client.api_call('channels.list'))


def get_channel_id_by_name(channel, slack_client):
    match = None
    groups = get_groups(slack_client)
    match = _extract_id(channel, groups.get('groups', []))
    if not match:
        channels = get_channels(slack_client)
        match = _extract_id(channel, channels.get('channels', []))
    return match


def get_channel_name(channel, slack_client):
    if channel.startswith('G'):
        apicall = 'groups.info'
        channel_type = 'group'
    else:
        apicall = 'channels.info'
        channel_type = 'channel'
    cdata = json.loads(slack_client.api_call(apicall, channel=channel))
    return cdata[channel_type]['name']


def get_groups(slack_client):
    return json.loads(slack_client.api_call('groups.list'))


def get_user_name(user, slack_client):
    udata = json.loads(slack_client.api_call('users.info', user=user))
    return udata['user']['name']


def invite_user(user, channel, slack_client):
    if channel.startswith('G'):
        apicall = 'groups.invite'
    else:
        apicall = 'channels.invite'
    resp = slack_client.api_call(apicall, user=user, channel=channel)

    return json.loads(resp)


def setup_bot(config):
    admin_channel = config.get('admin_channel')
    botname = config.get('botname')
    icon_emoji = config.get('icon_emoji')

    return admin_channel, botname, icon_emoji
