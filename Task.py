import time
import random as rnd 
import json 
from text_formats import * 
from abc import ABC, abstractmethod

class SecodaTask(ABC):
    """
        Abstract base class representing a generic Secoda task
    """
    def __init__(self, name: str):
        # Initialize task with a name and default 'Queued' status
        self.name = name 
        self.status = 'Queued'
    def __call__(self):
        # Attempt to execute the task, update the status based on outcome
        try:
            self.do_task() 
            self.status = 'Success'
        except Exception as e:
            print_color(Colors.RED, f"Error in {self.name}: {str(e)}")
            self.status = 'Failed'

    @abstractmethod
    def do_task(self):
        # Abstract method to be implemented by subclasses. Represents the task's logic.
        raise NotImplementedError("Subclasses must implement this method")

    def to_json(self):
        # Serialize task information into JSON format.
        return json.dumps({'name': self.name, 'task_type': self.task_type})
    
    
class SecodaSuccessTask(SecodaTask):
    """
        Represents a task that is expected to succeed
    """

    def __init__(self, name: str):
        # Intialize the test with type "Success"
        super().__init__(name)  
        self.task_type = 'Success'

    def do_task(self):
        # Simulate successful task execution with a random delay
        start_time = time.time()
        time.sleep(rnd.random())
        end_time = time.time()
        print_color(Colors.YELLOW, f"Task {self.name} completed after {end_time - start_time:.2f} seconds !")

    @staticmethod
    def from_json(json_str):
        # Deserialize a JSON string to create a SecodaSuccessTask instance
        data = json.loads(json_str)
        return SecodaSuccessTask(name=data['name'])
    
class SecodaFailedTask(SecodaTask):
    """
        Represent a task that is expected to fail
    """
    def __init__(self, name: str):
        # Intialize the test with type "Failed"
        super().__init__(name)  
        self.task_type = 'Failed'

    def do_task(self):
        # Simulate failed task execution with a random delay and forced error.
        start_time = time.time()
        time.sleep(rnd.random())

        # Intentionally make it failed
        x = 1/0
        end_time = time.time()
        print_color(Colors.YELLOW, f"Task {self.name} completed after {end_time - start_time:.2f} seconds !")

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return SecodaFailedTask(name=data['name'])