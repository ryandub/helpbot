import json
import redis


class Helps(object):
    def __init__(self, config):
        assert config, "config must be supplied"

        self.client = self._client(config)
        self.key = config.get('key')

    def _client(self, config):
        host = config.get('host', 'localhost')
        db = config.get('db', 0)
        port = config.get('port', 6379)
        password = config.get('password', None)

        client = redis.StrictRedis(host=host, port=port, db=db,
                                   password=password)
        return client

    def ack(self, channel_name):
        helps = self.get_all()
        acks = []
        for help in helps:
            jhelp = json.loads(help)
            if channel_name in jhelp:
                acks.append(help)
        for ack in acks:
            self.client.srem(self.key, ack)
        return True

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
