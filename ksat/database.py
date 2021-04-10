from typing import Optional
from ksta.task import TaskStatus, Task, task_from_dict, new_task_id


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
        "task_id": {
            "path": "abc",
            "args": (1, 2, 3),
            "status": "PENDING",
        },
        "task_id2": {...},
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
            f.write(json.dump(db_dict))

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        # Read from file everytime to not worry about memory state for now
        db = get_db_as_dict()
        task_dict = db.get(task_id)
        if task_dict is None:
            return None
        return task_from_dict(task_dict)


    def save_task(self, task: Task):
        # Read from file everytime to not worry about memory state for now
        db = get_db_as_dict()
        db[Task.id] = Task._asdict()
        self.save_db(db)

    def enqueue_task(self, path, args) -> Task:
        # How do we encode args?
        task = Task(new_task_id(), path, args, TaskStatus.WAITING)
        self.save_task(task)

    def dequeue_task(self) -> Optional[Task]:
        db = get_db_as_dict()
        selected_task = None
        for task_id, task_dict in db.items():
            if task_dict["status"] == TaskStatus.WAITING.name:
                selected_task = task_from_dict(task_dict)
                break

        if selected_task is None:
            return None

        self.update_task_status(selected_task.id, TaskStatus.PENDING)

    def update_task_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task_by_id(task_id)
        task.status = status.name
        self.save_task(task)
        return task
