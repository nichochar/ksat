from ksat.task import Task, TaskStatus


waiting_task = Task("path.to.func1", (1, 2, "3"), TaskStatus.WAITING)
pending_task = Task("path.to.func2", (4, 5), TaskStatus.PENDING)
succeeded_task = Task("path.to.func3", ("str1", "str2"), TaskStatus.SUCCEEDED)
