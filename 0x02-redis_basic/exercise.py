#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with Redis to store
data using randomly generated keys. It supports multiple data types and
is designed to be used as a simple caching mechanism.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    A Cache class for storing data in Redis using unique keys.

    This class connects to a Redis instance, flushes the database on
    initialization, and provides a method to store data using a
    randomly generated UUID key.
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
