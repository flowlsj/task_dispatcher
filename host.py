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
    NVME = 0
    DNVME = 1
    UNKNOWN = 2

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
            return False
        return True

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
        :return: None
        """
        self.update_state()

        if self.state == ExecutorState.READY:
            try:
                task.status = TaskStatus.RUNNING
                self.status = ExecutorStatus.RUNNING_TASK
                print "Start to run task [%s] on executor [%s]" % (task.cmdLine, self.ip_address)
                self.connection.exec_command(command=task.cmdLine)

                #TODO: need to think about the error status

                sleep(5)
                log_printed = False
                # Wait until the task is finished
                command_line = "ps -ef | grep \"" + task.cmdLine.strip() + "\"" + " | grep -v \"grep\""
                (_, std_out, std_err) = self.connection.exec_command(command=command_line)
                std_out = std_out.readlines()
                while len(std_out) != 0:
                    if not log_printed:
                        print "Running task [%s] on executor [%s]" % (task.cmdLine, self.ip_address)
                        log_printed = True
                    sleep(3)
                    (_, std_out, std_err) = self.connection.exec_command(command=command_line)
                    std_out = std_out.readlines()
            except Exception as ex:
                print "Run task [%s] failed on executor [%s] due to %s" % (task.cmdLine, self.ip_address, ex.message)
            finally:
                print "Finished running [%s] on executor [%s]" % (task.cmdLine, self.ip_address)
                task.status = TaskStatus.EXECUTED
                self.status = ExecutorStatus.NOT_SCHEDULED
                self.update_state()


    def update_state(self):
        """
        Update host status
        :return: None
        """
        if not self.connect():
            return

        # To check if the host could detect nvme device
        (_, std_out, std_err) = self.connection.exec_command("ls /dev | grep nvme")

        std_err = std_err.readlines()
        if len(std_err) != 0:
            self.state = ExecutorState.UNKNOWN
            return

        std_out = std_out.readlines()
        if len(std_out) == 1:
            # Only one line "nvme0" for dnvme driver
            self.state = ExecutorState.READY
            self.driver = DriverType.DNVME
        elif len(std_out) == 2:
            # Two lines "nvme0" and "nvme0n1" for nvme driver
            self.state = ExecutorState.READY
            self.driver = DriverType.NVME
        else:
            self.state = ExecutorState.CARD_NOT_FOUND
