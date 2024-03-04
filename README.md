# Concurrent Task Queue

## Introduction
A concurrent task queue implemented from scratch, using only Redis and Python primitives.

## Installation

Clone the repository:
```bash
git clone <repository-url>
```

## Usage

### Running the Application
Execute the following command to run a sample queue application locally, on a Docker container.

You should see some stuff printed out on the terminal.


```bash
make run-local
```

### Testing
To run tests inside a Docker container:
```bash
make test-local
```

## Structure
- `Queue.py`: Defines the `SecodaQueue` class for queue operations.
- `Task.py`: Contains the task class definition for task processing.
- `main_driver.py`: The main script that initializes and starts the task queue system. This file also serves as an example of using the concurrent task queue.
- `test/`: Directory containing all test files


## Detailed component breakdown

### SecodaQueue class
The SecodaQueue class implements a simple queue system integrated with Redis.

**Initialization:**
```
SecodaQueue(queue_name="Secoda", host="localhost", port=6379, db=0)
```

**Parameters:**
- **queue_name**: Name of the queue, used as a key in Redis.
- **host**: Hostname of the Redis server
- **port**: Port for Redis server
- **db**: Database number to connect to on Redis

**Methods:**
- **enqueue_redis**: Enqueue a task into the Redis queue.
- **deqeue_redis**: Dequeue a task from the Redis queue. If `block` = True, block for at most `timeout` seconds until a task is available.
- **update_task_redis**: Update the status of a task in Redis
- **get_all_task_statuses**: Retrieves the status of all tasks from Redis, in `Dict[str, str]` format
- **size_redis**: Return the current size of the queue

### SecodaTask class
An abstract base class that defines the structure for tasks.

**Initialization**: 
```
SecodaSuccessTask(f"task01")
```
or 
```
SecodaFailedTask(f"task01")
```

**Call behavior**: attempts to execute the task by calling the `do_task` method. The task's status is updated based on the outcome.

**Methods**
- **do_task**: Simulate successful/failed task execution with a random delay. 
- **from_json**: static method that deserializes a JSON string into an 
`SecodaFailedTask` or `SecodaSuccessTask` instance
