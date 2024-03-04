import multiprocessing
import time
from Queue import SecodaQueue
from Task import SecodaSuccessTask, SecodaFailedTask
import json
from text_formats import *
import logging

# This is more of an integration test for the whole system
# The system has two producers and two consumers.
# Each producer produces five tasks, each task is a Python function.
# At the end, we verify that all tasks have been processed and compare the final statuses
# to the groundtruth. We also verify the FIFO order per producer.

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

NUM_PRODUCERS = 2
NUM_CONSUMERS = 2
NUM_ITEM_PER_PRODUCER = 5
FAILED_TEST_INDICES = [(0, 0), (1, 3)]


def producer(queue_name, producer_idx, num_items):
    queue_broker = SecodaQueue(queue_name=queue_name)
    for i in range(num_items):
        if (producer_idx, i) in FAILED_TEST_INDICES:
            item = SecodaFailedTask(f"task_{producer_idx}_{i}")
        else:
            item = SecodaSuccessTask(f"task_{producer_idx}_{i}")
        queue_broker.enqueue_redis(item)
        print_color(Colors.BLUE, f"Producer {producer_idx}: Produced {item.name}")
        time.sleep(1)  # Simulate time-consuming tasks


def consumer(queue_name, consumer_idx, processed_tasks):
    queue_broker = SecodaQueue(queue_name=queue_name)
    while True:
        item = queue_broker.dequeue_redis(block=True, timeout=5)
        if item:
            item_str = item.decode("utf-8")
            processed_tasks.append(json.loads(item_str)["name"])
            print_color(Colors.YELLOW, json.loads(item_str))
            if json.loads(item_str).get("task_type", "Success") == "Success":
                task = SecodaSuccessTask.from_json(item_str)
            else:
                task = SecodaFailedTask.from_json(item_str)

            task()
            queue_broker.update_task_status_redis(task)
            print_color(Colors.GREEN, f"Consumer {consumer_idx}: Consumed {item_str}")
        else:
            print_color(Colors.RED, f"Consumer {consumer_idx}: No item left.")
            break


def flush_redis(queue_name):
    queue_broker = SecodaQueue(queue_name=queue_name)
    queue_broker.redis.flushdb()


def status_logger(queue_name):
    queue_broker = SecodaQueue(queue_name=queue_name)
    while True:
        all_statuses = queue_broker.get_all_task_statuses()
        logging.info(json.dumps(all_statuses, indent=4))
        # If all tasks are processed (none are in "Queued" status), then exit
        if len(all_statuses) == NUM_PRODUCERS * NUM_ITEM_PER_PRODUCER and all(
            [val != "Queued" for key, val in all_statuses.items()]
        ):
            return
        time.sleep(1)  # Log status every 1 second


def test_concurrency():
    queue_name = "secoda_queue"
    flush_redis(queue_name)

    manager = multiprocessing.Manager()
    processed_tasks = manager.list()

    # Start the logger as a separate process
    logger_process = multiprocessing.Process(target=status_logger, args=(queue_name,))
    logger_process.start()

    # Start producer processes
    processes = []
    for i in range(NUM_PRODUCERS):
        p = multiprocessing.Process(
            target=producer, args=(queue_name, i, NUM_ITEM_PER_PRODUCER)
        )
        p.start()
        processes.append(p)

    # Start consumer processes
    for i in range(NUM_CONSUMERS):
        p = multiprocessing.Process(
            target=consumer, args=(queue_name, i, processed_tasks)
        )
        p.start()
        processes.append(p)

    # Wait for all producers and consumers to complete
    for p in processes:
        p.join()

    queue_broker = SecodaQueue(queue_name=queue_name)
    all_statuses = queue_broker.get_all_task_statuses()

    # Verify task status
    assert all_statuses == {
        "task_0_0": "Failed",
        "task_1_0": "Success",
        "task_1_1": "Success",
        "task_0_1": "Success",
        "task_1_2": "Success",
        "task_0_2": "Success",
        "task_1_3": "Failed",
        "task_0_3": "Success",
        "task_0_4": "Success",
        "task_1_4": "Success",
    }

    # Verify the FIFO order per producer
    for i in range(NUM_PRODUCERS):
        processed_sequence = [
            x.split("_")[-1] for x in processed_tasks if x.split("_")[-2] == str(i)
        ]
        print(processed_sequence)
        assert processed_sequence == [str(i) for i in range(NUM_ITEM_PER_PRODUCER)]

    print("Test completed")
