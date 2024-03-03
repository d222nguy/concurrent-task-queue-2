import time
import random as rnd 
import json 
from text_formats import * 
from abc import ABC, abstractmethod

class SecodaTask(ABC):

    def __init__(self, name: str):
        self.name = name 
        self.status = 'Queued'
    def __call__(self):
        try:
            self.do_task() 
            print_color(Colors.CYAN, f'Set success to {self.name}')
            self.status = 'Success'
        except Exception as e:
            print_color(Colors.RED, f"Error in {self.name}: {str(e)}")
            self.status = 'Failed'
    @abstractmethod
    def do_task(self):
        start_time = time.time()
        time.sleep(rnd.random())
        print_color(Colors.RED, 'in task')
        end_time = time.time()
        print_color(Colors.YELLOW, f"Task {self.name} completed after {end_time - start_time:.2f} seconds !")

    def to_json(self):
        return json.dumps({'name': self.name, 'task_type': self.task_type})
    
    
class SecodaSuccessTask(SecodaTask):

    def __init__(self, name: str):
        super().__init__(name)  
        self.task_type = 'Success'

    def do_task(self):
        start_time = time.time()
        time.sleep(rnd.random())
        print_color(Colors.RED, 'in task')
        end_time = time.time()
        print_color(Colors.YELLOW, f"Task {self.name} completed after {end_time - start_time:.2f} seconds !")

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return SecodaSuccessTask(name=data['name'])
    
class SecodaFailedTask(SecodaTask):

    def __init__(self, name: str):
        super().__init__(name)  
        self.task_type = 'Failed'

    def do_task(self):
        start_time = time.time()
        time.sleep(rnd.random())
        print_color(Colors.RED, 'in failed task')
        x = 1/0
        end_time = time.time()
        print_color(Colors.YELLOW, f"Task {self.name} completed after {end_time - start_time:.2f} seconds !")

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return SecodaFailedTask(name=data['name'])