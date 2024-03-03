import threading
import redis 
import time 
from text_formats import *

class SecodaQueue:

    def __init__(self, queue_name='Secoda', host='localhost', port=6379, db=0):
        self.name = queue_name
        self.task_status = {}

        # Redis as message broker
        self.redis = redis.Redis(host=host, port=port, db=db)
    
    def enqueue(self, task):
        with self.lock:
            self.tasks.append(task)
    
    def deque(self):
        with self.lock:
            if not self.tasks:
                return None 
            return self.tasks.pop(0)
    
    def enqueue_redis(self, task):
        self.task_status[task] = "Queued"
        task_json = task.to_json()
        print_color(Colors.MAGENTA, task.__dict__)
        print_color(Colors.MAGENTA, task_json)
        self.redis.rpush(self.name, task_json)

    def dequeue_redis(self, block=True, timeout=0):
        time.sleep(0.5)
        if block:
            item = self.redis.blpop(self.name, timeout=timeout)
            if item:
                return item[1]
            return None 
        else:
            return self.redis.lpop(self.name)

    def update_task_redis(self, task):
        self.redis.hset(f"{self.name}:task_statuses", task.name, task.status)

    def get_all_task_statuses(self, queue_name):
        """Retrieve the status of all tasks from the broker."""
        with redis.Redis() as client:
            all_statuses = self.redis.hgetall(f"{self.name}:task_statuses")
            # Convert from bytes to string and print
            return {k.decode('utf-8'): v.decode('utf-8') for k, v in all_statuses.items()}

    def is_empty(self):
        with self.lock:
            return len(self.tasks) == 0
        
    def size(self):
        with self.lock:
            return len(self.tasks)

    def size_redis(self):
        """Return the current size of the queue."""
        return self.redis.llen(self.name)

