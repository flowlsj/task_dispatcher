# -*- coding:utf-8 -*-

from time import sleep
from threading import Thread
from optparse import OptionParser

from executor_manager import ExecutorManager
from task_manager import TaskManager
from task import TaskStatus

def get_arguments():
    """
    Parse command line arguments
    :return: parsed arguments
    """
    arguments = None
    try:
        opt = OptionParser()
        opt.add_option('--build_type',
                       dest='build_type',
                       type=str,
                       help='The build type, it will determine which executors will be used to execute tasks')

        opt.add_option('--task_list_file',
                       dest='task_list_file',
                       type=str,
                       help='The file stores the task list')

        (arguments, _) = opt.parse_args()

    except Exception as ex:
        print("Exception : %s" % ex.message)

    return arguments

if __name__=="__main__":
    arguments = get_arguments()
    if arguments is None:
        print """
        Usage: python dispatcher.py --build_type=<build_type> --task_list=<task_list_file>
        """
    executor_manager = ExecutorManager()
    executor_manager.load_executors(build_type=arguments.build_type)

    task_manager = TaskManager()
    task_manager.load_tasks(task_file=arguments.task_list_file)

    task = task_manager.get_next_task()
    while task is not None:
        sleep(1)
        if executor_manager.has_valid_executor_for_task(task):
            executor = executor_manager.get_executor_for_task(task)
            if executor is not None:
                executor.run_task(task)
                task = task_manager.get_next_task()
        else:
            task.status = TaskStatus.CANNOT_BE_EXECUTED
            task = task_manager.get_next_task()
            continue
