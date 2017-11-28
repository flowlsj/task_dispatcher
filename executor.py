# -*- coding:utf-8 -*-

from threading import Lock

class ExecutorState(object):
    """
    The class to describe host state
    """
    READY = "READY"
    LOST_CONNECTION = "LOST_CONNECTION"
    CARD_NOT_FOUND = "CARD_NOT_FOUND"
    CARD_NO_RESPONSE = "CARD_NO_RESPONSE"
    MARK_AS_INVALID = "MARK_AS_INVALID"
    UNKNOWN = "UNKNOWN"

class ExecutorStatus(object):
    """
    The class to describe host status
    """
    NOT_SCHEDULED = "NOT_SCHEDULED"
    SCHEDULED = "SCHEDULED"
    RUNNING_TASK = "RUNNING_TASK"
    RELEASED = "RELEASED"

class Executor(object):
    """
    The abstract class for all executors
    """

    def __init__(self, type=0):
        self.type = type
        self.state = ExecutorState.UNKNOWN
        self.status_lock = Lock()
        self._status = ExecutorStatus.NOT_SCHEDULED
        self.task_executed = []

    @property
    def status(self):
        with self.status_lock:
            return self._status

    @status.setter
    def status(self, new_status):
        with self.status_lock:
            self._status = new_status

    def connect(self):
        pass

    def update_status(self):
        pass

    def recover(self):
        pass

    def run_task(self, task=None):
        pass

    def could_run_task(self, task):
        pass


class ExecutorGenerator(object):
    """
    The class to generate executor by type
    """
    def __init__(self):
        pass

    @classmethod
    def generate_executor(cls, type=0, **kwargs):
        """
        Produce executor by its type
        :param type: 0 - physical host, 1 - virtual machine
        :param kwargs: executor properties
        :return: instance of executor
        """
        if type == 0:
            from host import Host
            return Host(**kwargs)
