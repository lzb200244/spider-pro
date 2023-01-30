# -*- coding: utf-8 -*-
# @Time : 2023/1/6 14:48
# @Site : https://www.codeminer.cn
"""
file-name:redis
ex:redis_pool
"""
from threading import RLock

import redis


class RedisPooL:
    POOL = redis.ConnectionPool(host='localhost', port=6379, encoding='UTF-8', max_connections=1000)

    lock = RLock()

    def __new__(cls, *args, **kwargs):
        with cls.lock:
            if not hasattr(cls, "_instance"):
                cls._instance = super(RedisPooL, cls).__new__(cls)
            return cls._instance

    @property
    def get_con(self):
        return redis.Redis(connection_pool=self.POOL)
