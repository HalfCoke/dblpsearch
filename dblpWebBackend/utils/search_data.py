from redis import Redis

from conf import REDIS_HOST, REDIS_PORT, RECENT_WORD


class RedisOP:
    def __init__(self, set_name):
        self._redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.set_name = set_name

    def push_recent_word(self, key):
        self._redis_client.lpush(RECENT_WORD, key)

    def increment(self, key):
        self._redis_client.zincrby(self.set_name, 1, key)

    def get_recent_word(self, k):
        redis_res = self._redis_client.lrange(RECENT_WORD, 0, k)
        return [str(res).lstrip("b").strip("'") for res in redis_res]

    def get_top_k_word(self, k):
        redis_res = self._redis_client.zrevrange(self.set_name, 0, k, True, int)
        return [[str(r[0]).lstrip("b").strip("'"), r[1]] for r in redis_res]


def increment_search_data(key, redis_client):
    redis_client.increment(key)
    redis_client.push_recent_word(key)
