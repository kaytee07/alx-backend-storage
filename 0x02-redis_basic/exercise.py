#!/usr/bin/env python3
"""
writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable
from funtools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count number of calls made to Cache class methods
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        call method after incrementing its call counter
        """
        method_to_count = method.__qualname__
        redis_client = getattr(self, '_redis')
        redis_client.incr(method_to_count)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    cache class
    """

    def __init__(self) -> None:
        """
        store instance of redis client and flush with flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data in redis using key generate with uuid

        Args:
            data: data to be stored using key generated with uuid

        Return:
            return the generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        get data from redis db and convert to required data type

        Args:
            key: key used to store the data
            fn: callable function that convert rtrieved data to 
            appropriate data type

        Return:
            key of the data stored in redis
        """
        data = self._redis.get(key)
        if data is None:
            return data

        if fn:
            return fn(data)

    def get_str(self, key: str) -> str:
        """
        convert redis data to string
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: int) -> int:
        """
        convert redis data to int
        """
        lambda x: int(x)
