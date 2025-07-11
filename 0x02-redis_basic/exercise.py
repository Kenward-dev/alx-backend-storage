#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with Redis to store
and retrieve data using unique, randomly generated keys. It also includes
mechanisms to count how many times methods are called using Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    The count is stored in Redis using the method’s qualified name.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments call count and calls method."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    A Cache class for storing data in Redis using unique keys.

    This class connects to a Redis instance, flushes the database on
    initialization, and provides methods to store and retrieve data
    with optional format conversion. It also tracks method usage.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.

        Connects to the Redis server and flushes the database to start
        with a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated UUID key.

        Args:
            data: The data to be stored. Can be of type str, bytes,
                  int, or float.

        Returns:
            A string representing the UUID key under which the data
            was stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable[[bytes], Union[str, int, float]]] = None
            ) -> Union[bytes, str, int, float, None]:
        """
        Retrieve data from Redis using a key, with optional conversion.

        Args:
            key: The key under which the data is stored.
            fn: Optional callable to convert the data (e.g., decode or cast).

        Returns:
            The retrieved data (converted if fn is provided), or None
            if the key does not exist.
        """
        
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis and decode it as a UTF-8 string.

        Args:
            key: The key under which the data is stored.

        Returns:
            The decoded string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key: The key under which the data is stored.

        Returns:
            The converted integer, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: int(d))
    