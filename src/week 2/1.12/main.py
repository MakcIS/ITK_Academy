import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self):
        self.redis = redis.Redis()

    def test(self) -> bool:
        now = time.time()
        self.redis.zremrangebyscore("rate_limiter", "-inf", now - 3)
        if self.redis.zcard("rate_limiter") < 5:
            self.redis.zadd("rate_limiter", {now: now})
            return True
        else:
            return False


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
