# -*- coding:utf-8 -*-

from threading import Lock

from task import Task, TaskStatus

class TaskManager(object):
    """
    The class for manage tasks
    """

    def __init__(self):
        """
        Constructor of Task Manager
        """
        self.tasks = []
        self.task_list_lock = Lock()

    def add_task(self, task):
        """
        Add task to task pool
        :param task: new task
        :return: None
        """
        self.tasks.append(task)

    def get_next_task(self):
        """
        To return the next task to be executed
        :return: task to be executed or None if all tasks had been scheduled
        """
        with self.task_list_lock:
            for task in self.tasks:
                if task.status == TaskStatus.NOT_SCHEDULED:
                    task.status = TaskStatus.SCHEDULED
                    return task
        return None

    def check_task_result(self, task):
        pass

    def load_tasks(self, task_file):
        """
        Load task from a file, each line in the file should be a command line task
        :param task_file: the file contains all tasks
        :return: None
        """
        task_file = open(task_file)
        command_line = task_file.readline()
        while command_line != "":
            task = Task(command_line)
            self.add_task(task)
            command_line = task_file.readline()
        task_file.close()
