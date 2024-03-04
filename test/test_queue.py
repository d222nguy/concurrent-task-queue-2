import pytest
from Queue import SecodaQueue  # Update import paths as needed
from Task import SecodaSuccessTask, SecodaFailedTask
import json
import redis


def test_enqueue_dequeue_redis():
    """
    Test enqueue/dequeue
        1. Enqueue a task. len(queue) should be = 1
        2. Dequeue the task. Task should be identical to the inserted one.
    """
    redis_db = redis.Redis(host="localhost", port=6379, db=0)
    redis_db.flushdb()

    queue = SecodaQueue("test_queue")

    task = SecodaSuccessTask("test_task")
    queue.enqueue_redis(task)

    # Verify that task was enqueued properly
    assert queue.size_redis() == 1

    # Dequeue and verify
    dequeued = queue.dequeue_redis()
    assert dequeued is not None

    assert json.loads(dequeued) == {"name": "test_task", "task_type": "Success"}

    assert queue.size_redis() == 0

    queue.enqueue_redis(task)
    queue.enqueue_redis(task)
    queue.dequeue_redis(task)

    assert queue.size_redis() == 1


def test_update_task_redis():
    """
    Test updating task and retrieving task statuses from broker.
    Test flow:
    1. Submit a task to queue. Status should be 'Queued'.
    2. Execute the task. Status should be 'Success'
    3. Add a failed task and execute. Status should be 'Failed'
    """
    redis_db = redis.Redis(host="localhost", port=6379, db=0)
    redis_db.flushdb()

    queue = SecodaQueue("test_queue_1")
    task = SecodaSuccessTask("test_task_1")
    queue.update_task_status_redis(task)

    statuses = queue.get_all_task_statuses()
    print(statuses)

    # Only queued, was not executed - status should be should be 'Queued'
    assert statuses == {"test_task_1": "Queued"}
    task()
    queue.update_task_status_redis(task)
    statuses = queue.get_all_task_statuses()

    # Status should be 'Success'
    assert statuses == {"test_task_1": "Success"}

    # Status should be 'Failed'
    failed_task = SecodaFailedTask("test_task_2")
    failed_task()
    queue.update_task_status_redis(failed_task)
    statuses = queue.get_all_task_statuses()
    assert statuses == {"test_task_1": "Success", "test_task_2": "Failed"}
