import redis

class RedisUniq(object):
    """
    Module to return uniq elements given a list of elements
    This module is backed by a Redis set object
    """
    def __init__(self, host='localhost', port=6379, db=0,
                 set_name="nltkext_uniqset"):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.set_name = set_name
        self.redis.delete(self.set_name)

    def __del__(self):
        self.redis.delete(self.set_name)

    def process(self, data=None):
        for s in data:
            if not self.redis.sismember(self.set_name, s):
                self.redis.sadd(self.set_name, s)
                yield s
