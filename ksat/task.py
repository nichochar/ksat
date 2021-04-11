from collections import namedtuple
import pickle
import uuid
import enum


class TaskStatus(enum.Enum):
    """
    enum documentation: https://docs.python.org/3/library/enum.html
    """
    WAITING = 1
    PENDING = 2
    SUCCEEDED = 3
    FAILED = 4


class Task:
    def __init__(self, path, args, status=TaskStatus.WAITING, task_id=None):
        self.id = task_id or uuid.uuid4().hex 
        self.path = path
        self.args = args
        self.status = status

    @classmethod
    def deserialize(cls, serialized_task: str):
        return pickle.loads(serialized_task)

    def serialize(self) -> str:
        return pickle.dumps(self)
