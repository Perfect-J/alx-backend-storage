#!/usr/bin/env python3
""" Web Caching Module using Decorators """

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
        """ Wrapper for decorator """
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
    """ Get the HTML content of a URL and cache it """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test the caching functionality using the slowwly API (simulates slow response)
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.example.com"
    for _ in range(5):
        html_content = get_page(url)
        print(html_content)
