#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Create a Redis client instance
redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """ Decorator wrapper """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator guy """
        # Increment the count for this URL in Redis
        redis_client.incr(f"count:{url}")
        # Check if the response is cached in Redis
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        # If not cached, fetch the response from the web server
        result = fn(url)
        # Cache the response in Redis with an expiration time of 10 seconds (adjust as needed)
        redis_client.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """get page self-descriptive"""
    response = requests.get(url)
    return response.text
