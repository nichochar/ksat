from ksat.task import new_task_id, Task, task_from_dict, TaskStatus


def test_new_task_id():
    assert len(new_task_id()) == 32


def to_and_from_dict():
    task_id = new_task_id()
    expected_task = Task(task_id, "super duper path", (1, 2), TaskStatus.FAILED)

    task_dict = {
        "id":task_id,
        "path": "super duper path",
        "args": (1, 2),
        "status": "FAILED",
    }

    assert task_from_dict(task_dict) == expected_task

