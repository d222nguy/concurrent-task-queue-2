import threading
import redis
import time
from text_formats import *


class SecodaQueue:
    """Class representing a queue system integrated with Redis for task management."""

    def __init__(self, queue_name="Secoda", host="localhost", port=6379, db=0):
        # Initialize queue with specific name and connection to Redis.

        self.name = queue_name  # Nam of the queue, used as key in Redis
        self.task_status = {}  # Local cache of task statuses

        # Redis as message broker
        self.redis = redis.Redis(host=host, port=port, db=db)

    def enqueue_redis(self, task):
        # Enqueue a task into Redis queue.
        task_json = task.to_json()
        self.redis.rpush(self.name, task_json)

    def dequeue_redis(self, block=True, timeout=0):
        # Dequeue a task from Redis queue.
        time.sleep(0.5)
        if block:
            # Blocking pop from the left end of the Redis list.
            item = self.redis.blpop(self.name, timeout=timeout)
            if item:
                return item[1]  # Task data
            return None
        else:
            # Non-blocking pop from the left end of the Redis list.
            return self.redis.lpop(self.name)

    def update_task_status_redis(self, task):
        # Update a task's status in Redis.
        self.redis.hset(f"{self.name}:task_statuses", task.name, task.status)

    def get_all_task_statuses(self):
        # Retrieve the status of all tasks from the broker.
        with redis.Redis() as client:
            all_statuses = self.redis.hgetall(f"{self.name}:task_statuses")
            # Convert from bytes to string and print
            return {
                k.decode("utf-8"): v.decode("utf-8") for k, v in all_statuses.items()
            }

    def size_redis(self):
        # Return the current size of the queue
        return self.redis.llen(self.name)
