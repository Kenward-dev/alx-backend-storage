#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with Redis to store
data using randomly generated keys. It supports multiple data types and
is designed to be used as a simple caching mechanism.
"""

import redis
import uuid
from typing import Union, Callable, Optional

class Cache:
    """
    A Cache class for storing data in Redis using unique keys.

    This class connects to a Redis instance, flushes the database on
    initialization, and provides methods to store and retrieve data
    with optional format conversion.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.

        Connects to the Redis server and flushes the database to start
        with a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
