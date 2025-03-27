import json
import time

import redis


class RedisQueue:
    def __init__(self):
        self.redis = redis.Redis(decode_responses=True)
        self.queue_id = f"queue:{time.time()}"

    def publish(self, msg: dict):
        value = json.dumps(msg)
        self.redis.lpush(self.queue_id, value)

    def consume(self) -> dict | None:
        result = self.redis.rpop(self.queue_id)

        if result:
            return json.loads(result)

    def clear_queue(self, total: bool = False):
        if total:
            for queue in self.redis.keys("queue:*"):
                self.redis.delete(queue)
        self.redis.delete(self.queue_id)


if __name__ == "__main__":
    q = RedisQueue()
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
