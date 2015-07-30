import json
import redis


class Helps(object):
    def __init__(self, config):
        assert config, "config must be supplied"

        self.client = self._client(config)
        self.key = config.get('key')
        self.help_ack_score = self.key + "_ack_score_help"
        self.pr_ack_score = self.key + "_ack_score_pr"

    def _client(self, config):
        host = config.get('host', 'localhost')
        db = config.get('db', 0)
        port = config.get('port', 6379)
        password = config.get('password', None)

        client = redis.StrictRedis(host=host, port=port, db=db,
                                   password=password)
        return client

    def ack_help(self, channel_name, username):
        return self.ack(channel_name, username, self.help_ack_score)

    def ack_pr(self, channel_name, username):
        return self.ack(channel_name, username, self.pr_ack_score)

    def ack(self, channel_name, username, ack_flavor):
        helps = self.get_all()
        acks = []
        at_least_one_ack = False

        for help in helps:
            jhelp = json.loads(help)
            if channel_name in jhelp:
                acks.append(help)
                at_least_one_ack = True

        for ack in acks:
            self.client.srem(self.key, ack)

        if at_least_one_ack:
            self.client.zincrby(ack_flavor, username, amount=1)
            return self.client.zscore(ack_flavor, username)

        # implies zero found to start with. this info may be useful to caller.
        return 0

    def get_all(self):
        return self.client.smembers(self.key)

    def store(self, channel_name, username, timestamp):
        helps = self.get_all()
        for help in helps:
            jhelp = json.loads(help)
            if channel_name in jhelp:
                return False
        help_request = ('{"%s": {"user": "%s", "timestamp": "%s"}}' %
                        (channel_name, username, timestamp))
        self.client.sadd(self.key, help_request)
        return True
