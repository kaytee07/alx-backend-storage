#!/usr/bin/env python3
"""
writing strings to redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    cache class
    """

    def __init__(self):
        """
        store instance of redis client and flush with flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data in redis using key generate with uuid

        Args:
            data: data to be stored using key generated with uuid

        Return:
            return the generated key
        """
        self.key = uuid.uuid4()
        self._redis.set(key, data)
        return key
