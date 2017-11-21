# -*- coding:utf-8 -*-

from threading import Lock
import time

from task import Task, TaskStatus

class TaskManager(object):
    """
    The class for manage tasks
    """

    def __init__(self):
        """
        Constructor of Task Manager
        """
        self.task_list_to_be_executed = []
        self.task_list_to_be_executed_lock = Lock()

        self.task_list_executed = []
        self.task_list_executed_lock = Lock()

        self.task_list_cannot_be_executed = []
        self.task_list_cannot_be_executed_lock = Lock()

    def _add_task(self, task):
        """
        Add task to task pool
        :param task: new task
        :return: None
        """
        task.status = TaskStatus.NOT_SCHEDULED
        self.task_list_to_be_executed.append(task)

    def get_next_task(self):
        """
        To return the next task to be executed
        :return: task to be executed or None if all tasks had been scheduled
        """
        retry_count = 2
        # Add retry to make sure only return None after all tasks had been executed
        # We might get none and first time, but get a task second time if no executor
        # could execute the task
        while retry_count > 0:
            with self.task_list_to_be_executed_lock:
                if len(self.task_list_to_be_executed) != 0:
                    task = self.task_list_to_be_executed.pop(0)
                    task.status = TaskStatus.SCHEDULED
                    return task
            retry_count -= 1
            time.sleep(3)
        return None

    def put_back_to_task_pool(self, task):
        """
        To put a scheduled task back to task pool
        :param task:
        :return: None
        """
        with self.task_list_to_be_executed_lock:
            self._add_task(task)
            
    def mark_task_as_cannot_be_executed(self, task):
        """
        To mark a task as cannot be executed due to no executor is valid
        :param task: the task to be marked as unable to be executed
        :return: None
        """
        with self.task_list_cannot_be_executed_lock:
            task.status = TaskStatus.CANNOT_BE_EXECUTED
            self.task_list_cannot_be_executed.append(task)

    def mark_task_as_executed(self, task):
        """
        To mark a task as executed
        :param task: the task has been executed
        :return: None
        """
        with self.task_list_executed_lock:
            self.task_list_executed.append(task)

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
            self._add_task(task)
            command_line = task_file.readline()
        task_file.close()
