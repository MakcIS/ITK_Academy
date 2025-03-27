import time
from datetime import timedelta

import redis

redis = redis.Redis(host="localhost", port=6379, decode_responses=True)


def single(max_processing_time: timedelta = timedelta(seconds=1)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"lock:{func.__name__}"
            value = str(time.time())

            while True:
                if redis.set(key, value, nx=True, ex=max_processing_time):
                    result = func(*args, **kwargs)
                    if redis.get(key) == value:
                        redis.delete(key)
                    return result

        return wrapper

    return decorator


@single(max_processing_time=timedelta(seconds=2))
def process_transaction():
    time.sleep(5)


process_transaction()
