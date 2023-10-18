#!/usr/bin/env python3
"""
writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count number of calls made to Cache class methods
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        call method after incrementing its call counter
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store history of input and output of a function of a 
    particular method
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Returns the method's output after storing its 
        inputs and output.
        """
        inputs = '{}:inputs'.format(method.__qualname__)
        outputs = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(inputs, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, output)
        return output
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

    @count_history
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
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        convert redis data to string
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: int) -> int:
        """
        convert redis data to int
        """
        return self.get(key, lambda x: int(x))
