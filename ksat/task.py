from collections import namedtuple
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


Task = namedtuple("Task", ["id", "path", "args", "status"])


def task_from_dict(task_dict: dict) -> Task:
    return Task(
        task_dict["id"],
        task_dict["path"],
        task_dict["args"],
        TaskStatus[task_dict["status"]])


def new_task_id() -> str:
    return uuid.uuid4().hex
