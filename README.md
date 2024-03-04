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
Execute the following command to run a sample queue application locally, on a Docker container

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
