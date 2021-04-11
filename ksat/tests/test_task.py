import uuid
from ksat.task import Task, TaskStatus


def test_serialize_and_deserialize():
    task_id = uuid.uuid4().hex
    task = Task("super duper path", (1, 2), status=TaskStatus.FAILED, task_id=task_id)

    round_trip_task = Task.deserialize(task.serialize())
    assert round_trip_task.id == task.id
    assert round_trip_task.status == task.status
    assert round_trip_task.path == task.path
    assert round_trip_task.args == task.args

