# -*- coding:utf-8 -*-

import os
from threading import Lock

class TaskStatus(object):
    NOT_SCHEDULED = 0
    SCHEDULED = 1
    RUNNING = 2
    EXECUTED = 3
    CANNOT_BE_EXECUTED = 4

class TaskType(object):
    FUNCTION = 0
    PERFORMANCE = 1
    UNKNOWN = 2

class Task(object):
    """
    The class for task to be executed
    """

    def __init__(self, cmdLine):
        """
        Constructor of Task
        :param cmdLine:  the command line of the task, currently, task can be only executed from shell command line
        """
        self.cmdLine = cmdLine.strip()
        # TODO: need to revisit here for a better method to detect os path separator
        self.name = self.cmdLine.split(".")[0].split('/')[-1]
        if self.name.startswith("p_"):
            self.type = TaskType.PERFORMANCE
        elif self.name.startswith("t_"):
            self.type = TaskType.FUNCTION
        else:
            self.type = TaskType.UNKNOWN

        self.status_lock = Lock()
        self._status = TaskStatus.NOT_SCHEDULED

    def execute(self):
        pass

    @property
    def status(self):
        with self.status_lock:
            return self._status

    @status.setter
    def status(self, new_status):
        with self.status_lock:
            self._status = new_status
