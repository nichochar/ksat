from typing import Optional
import json
import base64
from ksat.task import TaskStatus, Task


class DB:
    """
    The storage class for our task manager application.
    This mostly acts as a queue so the required interface follows
    the usual suspects.
    """
    def __init__(self):
        print("Loading up the DB...")
        pass

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """ Find a task by its unique identifier or None if not found """
        pass

    def save_task(self, task:Task):
        """ Save a task to the DB directly """
        pass

    def enqueue_task(self, path, args) -> Task:
        """ Create a new task from params, and add it to the queue """

    def dequeue_task(self) -> Optional[Task]:
        """ Get a task from the queue that is in WAITING status """ 

    def update_task_status(self, task_id: str, status: TaskStatus) -> Task:
        """ Update the status of a task, utility function """



class JsonFileDB(DB):
    """
    Ultra simple storage using a JSON file.

    The JSON implementation uses a JSON encoded as a string in the file.
    The schema of the JSON is as follows:
   { 
        "task_id": <b64 encoded string of pickled bytes>,
        "task_id2": <b64 encoded string of pickled bytes>,
        ...
    }
    """
    def __init__(self, filename="db.json"):
        super().__init__()
        print("Using JsonFileDB")
        self.filename = filename

    def get_db_as_dict(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def save_db(self, db_dict):
        with open(self.filename, 'w') as f:
            json.dump(db_dict, f)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        # Read from file everytime to not worry about memory state for now
        db = self.get_db_as_dict()
        serialized_task = db.get(task_id)
        if serialized_task is None:
            return None
        return Task.deserialize(base64.b64decode(serialized_task))

    def save_task(self, task: Task):
        db = self.get_db_as_dict()
        pickled_bytes = task.serialize()  # this calls pickle.dumps
        b64_encoded = base64.b64encode(pickled_bytes)
        db[task.id] = b64_encoded.decode('ascii')
        self.save_db(db)

    def enqueue_task(self, path, args) -> Task:
        task = Task(path, args)
        self.save_task(task)

    def dequeue_task(self) -> Optional[Task]:
        db = self.get_db_as_dict()
        selected_task = None
        for task_id, serialized_task in db.items():
            # Deserializint all tasks is not efficient
            task = Task.deserialize(serialized_task)
            if task.status == TaskStatus.WAITING:
                selected_task = task
                break

        if selected_task is None:
            return None

        self.update_task_status(selected_task.id, TaskStatus.PENDING)

    def update_task_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task_by_id(task_id)
        task.status = status.name
        self.save_task(task)
        return task
