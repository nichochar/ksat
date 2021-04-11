from ksat.database import JsonFileDB
from ksat.tests import fixtures
import pytest
import json


DB_FILENAME = "test_db.json"


@pytest.fixture
def db_filename(tmpdir_factory):
    db_dict = {}
    fn = tmpdir_factory.mktemp("data").join(DB_FILENAME)
    with open(fn, 'w') as f:
        json.dump(db_dict, f)
    return fn


def test_db_loads(db_filename):
    DB = JsonFileDB(filename=db_filename)
    assert DB.get_db_as_dict() == {}


def test_saving_and_retrieving_task(db_filename):
    DB = JsonFileDB(filename=db_filename)
    task = fixtures.waiting_task
    DB.save_task(task)
    returned_task = DB.get_task_by_id(task.id)

    assert returned_task.id == task.id
    assert returned_task.status == task.status
    assert returned_task.path == task.path
    assert returned_task.args == task.args
