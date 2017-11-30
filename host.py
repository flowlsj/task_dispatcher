# -*- coding:utf-8 -*-

import paramiko
from time import sleep

from executor import Executor, ExecutorState, ExecutorStatus
from task import TaskStatus, TaskType

class HostState(ExecutorState):
    """
    The class to describe host status
    """
    pass

class DriverType(object):
    NVME = "NVME"
    DNVME = "DNVME"
    UNKNOWN = "UNKNOWN"

class Host(Executor):
    """
    The class for physical host
    """
    def __init__(self, **kwargs):
        """
        Constructor of Host
        :param kwargs: the attributes for the host instance
        """
        super(Host, self).__init__()
        for mandatoryArg in ['ip_address', 'username', 'password']:
            if mandatoryArg not in kwargs:
                raise Exception("Mandatory argument %s missing" % mandatoryArg)

        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

        # For nvme test or dnvme
        self.driver = DriverType.UNKNOWN

        self.connection = None
        self.connected = False
        self.connect()
        self.update_state()

    def connect(self):
        """
        To create connection to host
        :return: True if connect successfully, False if not
        """
        if self.connection is None:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print "Connect to %s with port: %s." % (self.ip_address, self.ssh_port)
        try:
            self.connection.connect(hostname=self.ip_address,
                                    port=self.ssh_port,
                                    username=self.username,
                                    password=self.password,
                                    allow_agent=False,
                                    look_for_keys=False,
                                    timeout=10)
        except Exception as ex:
            print "Connect to host %s failed due to %s" % (self.ip_address, ex.message)
            self.connection = None
            self.state = ExecutorState.LOST_CONNECTION
            self.connected = False
        else:
            self.connected = True

    def could_run_task(self, task):
        """
        To check if current executor was able to run the task
        :param task: the task needs to be run
        :return: True if could run, False if could not
        """
        if self.driver == DriverType.NVME:
            if task.type == TaskType.PERFORMANCE:
                return True
            else:
                return False
        elif self.driver == DriverType.DNVME:
            if task.type == TaskType.FUNCTION:
                return True
            else:
                return False
        else:
            return False

    def run_task(self, task):
        """
        Run task by execute the task command line on host
        :param task: the task to be executed
        :return: True if task started successfully, False if not
        """
        self.update_state()
        task_command_line = task.cmdLine.strip()

        if self.state != ExecutorState.READY:
            return False

        retry_count = 5
        print "Try to start task [%s] on executor [%s]" % (task_command_line, self.ip_address)
        task_started = False
        while not task_started and retry_count > 0:
            try:
                self.connection.exec_command(command="nohup " + task.cmdLine + " &", timeout=30)
            except Exception as ex:
                print "Start task failed [%s] on %s due to %s, retry after 30 seconds later" %\
                      (task_command_line, self.ip_address, ex.message)
                retry_count -= 1
                sleep(30)
            else:
                task_started = True

        if task_started:
            task.status = TaskStatus.RUNNING
            self.status = ExecutorStatus.RUNNING_TASK
        else:
            task.status = TaskStatus.NOT_SCHEDULED
            self.status = ExecutorStatus.NOT_SCHEDULED
            return False

        task_finished = False
        retry_count = 10
        check_command_line = "ps -ef | grep \"" + task_command_line + "\"" + " | grep -v \"grep\""
        log_printed = False
        while not task_finished and retry_count > 0:
            # Wait until the task is finished
            if not log_printed:
                print "Running task [%s] on executor [%s]" % (task_command_line, self.ip_address)
                log_printed = True
            try:
                (_, std_out, std_err) = self.connection.exec_command(command=check_command_line, timeout=30)
                std_out = std_out.readlines()
                if len(std_out) == 0:
                    task_finished = True
            except Exception as ex:
                print "Check status of task [%s] failed on executor [%s] due to %s, retrying..." % \
                      (task_command_line, self.ip_address, ex.message)
                retry_count -= 1
                sleep(30)
        if task_finished:
            print "Finished running [%s] on executor [%s]" % (task_command_line, self.ip_address)
            self.status = ExecutorStatus.NOT_SCHEDULED
        else:
            print "Cannot get status of task [%s] on executor [%s], mark task as executed and release this executor" %\
                  (task_command_line, self.ip_address)
            self.status = ExecutorStatus.RELEASED
        task.status = TaskStatus.EXECUTED
        self.update_state()
        return True


    def update_state(self):
        """
        Update host status
        :return: None
        """
        if not self.connected:
            return

        # To check if the host could detect nvme device
        try:
            (_, driver_stdout, driver_stderr) = self.connection.exec_command("ls /dev | grep nvme")

            driver_stderr = driver_stderr.readlines()
            if len(driver_stderr) != 0:
                self.state = ExecutorState.UNKNOWN
                return
        except Exception as ex:
            print "Execute command on [%s] failed, mark it as LOST CONNECTION" % self.ip_address
            self.state = ExecutorState.LOST_CONNECTION
            return

        driver_stdout = driver_stdout.readlines()
        if len(driver_stdout) == 0:
            self.state = ExecutorState.CARD_NOT_FOUND
        else:
            # Check if there is enable/disable failure
            (_, dmesg_stdout, dmesg_stderr) = \
                self.connection.exec_command("dmesg | grep \"Disabling ctrlr failed\"")
            dmesg_stderr = dmesg_stderr.readlines()
            if len(dmesg_stderr) != 0:
                self.state = ExecutorState.UNKNOWN
                return

            dmesg_stdout = dmesg_stdout.readlines()
            if len(dmesg_stdout) != 0:
                self.state = ExecutorState.CARD_NO_RESPONSE
                return

            self.state = ExecutorState.READY
            if len(driver_stdout) == 2:
                # Two lines "nvme0" and "nvme0n1" for nvme driver
                self.driver = DriverType.NVME
            if len(driver_stdout) == 1:
                # One line "nvme0" for dnvme driver
                self.driver = DriverType.DNVME

    def is_for_build(self, build):
        """
        Check if the executor is for the required build
        :param build: the build to test
        :return: True if for this build, False if not
        """
        if not self.connected:
            return False

        (_, std_out, std_err) = self.connection.exec_command("cat /var/log/messages | grep " + build)

        std_err = std_err.readlines()
        if len(std_err) != 0:
            self.state = ExecutorState.UNKNOWN
            return False

        std_out = std_out.readlines()
        if len(std_out) != 0:
            return True
