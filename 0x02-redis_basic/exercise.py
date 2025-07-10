#!/usr/bin/env python3

"""
Redis Basics
This module provides a simple interface to store data in Redis.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    Cache class to interact with Redis for storing data.
    """
    def __init__(self):
        """
        Initializes the Cache class and connects to Redis.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns the key.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key
    
