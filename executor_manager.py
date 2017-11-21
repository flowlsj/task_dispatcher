# -*- coding:utf-8 -*-

from threading import Lock

from config import HUT_CONFIG
from executor import ExecutorGenerator, ExecutorStatus, ExecutorState

class ExecutorManager(object):
    """
    The class for manage executors
    """

    def __init__(self):
        """
        Executor manager constructor
        """
        self.valid_executors = []
        self.invalid_executors = []
        self.executor_lock = Lock()

    def has_valid_executor_for_task(self,task):
        """
        To check if there was valid executor for task
        :param task: task needs to be executed
        :return:
        """
        with self.executor_lock:
            # Update executor status before check
            for executor in self.valid_executors:
                executor.update_status()
                if executor.state != ExecutorState.READY:
                    self.invalid_executors.append(executor)
                    self.valid_executors.remove(executor)
            for executor in self.valid_executors:
                if executor.could_run_task(task):
                    return True
            return False

    def get_executor_for_task(self, task):
        """
        Get a executor that could meet the requirements described in kwargs
        :param task: the task needs to be executed by the required executor
        :return: required executor or None
        """
        with self.executor_lock:
            index = 0
            while index < len(self.valid_executors):
                executor = self.valid_executors[index]
                if executor.status == ExecutorStatus.NOT_SCHEDULED and executor.could_run_task(task=task):
                    executor.status = ExecutorStatus.SCHEDULED
                    return executor
                index += 1
        return None


    def report_executor_status(self):
        """
        To report executor status to operation team after load executors
        So that operation team could fix faulted executors asap
        :return:
        """
        pass

    def add_valid_executor(self, executor):
        """
        Add a executor that could be used to run task
        :param executor: worked executor
        :return:  None
        """
        self.valid_executors.append(executor)

    def add_invalid_executor(self, executor):
        self.invalid_executors.append(executor)

    def load_executors(self, build_type=None):
        """
        Load all executors from config file
        :param build_type: the build type that executors work for
        :return:
        """
        executors = HUT_CONFIG.NAME_INFO_MAPPING
        for executor in executors.keys():
            if build_type is not None and build_type not in executors[executor]['for_build']:
                continue

            executor_instance = ExecutorGenerator.generate_executor(**executors[executor])
            if executor_instance.state == ExecutorState.READY:
                self.add_valid_executor(executor_instance)
            else:
                self.add_invalid_executor(executor_instance)
