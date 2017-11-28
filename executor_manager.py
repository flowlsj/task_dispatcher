# -*- coding:utf-8 -*-

from threading import Lock
from time import sleep

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

    def get_available_executor(self):
        """
        Get an available executor that could run task
        :return: executor or None
        """
        with self.executor_lock:
            for executor in self.valid_executors:
                if executor.status == ExecutorStatus.NOT_SCHEDULED:
                    executor.status = ExecutorStatus.SCHEDULED
                    return executor
        return None

    def get_all_available_executor(self):
        """
        Get all available executors that could run task
        :return: executors or None
        """
        pass

    def release_executor(self, executor):
        """
        Release executor once there is no task for it
        :param executor: the executor to be released
        :return: None
        """
        executor.status = ExecutorStatus.RELEASED

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

    def load_executors(self, build_type=None, build_number=None):
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
                if executor_instance.is_for_build(build_type + "_" + str(build_number)):
                    self.add_valid_executor(executor_instance)
                else:
                    executor_instance.state = ExecutorState.MARK_AS_INVALID
                    self.add_invalid_executor(executor_instance)
            else:
                self.add_invalid_executor(executor_instance)

    def dump_executor_state(self, dump_file):
        """
        Dump current executor state
        :param dump_file: where to dump
        :return: None
        """
        dump_file = open(dump_file, "w+")
        with dump_file:
            for executor in self.invalid_executors + self.valid_executors:
                dump_file.write("Executor ip address: [%s], state: [%16s], driver: [%s]\n" %
                                (executor.ip_address, executor.state, executor.driver))

    def wait_for_executor_finish_task(self):
        """
        Wait for all executors finish their running task
        :return: None
        """
        has_task_running = True
        while has_task_running:
            has_task_running = False
            for executor in self.valid_executors:
                if executor.status == ExecutorStatus.RUNNING_TASK:
                    has_task_running = True
                    sleep(15)
                    break
