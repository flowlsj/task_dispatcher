# -*- coding:utf-8 -*-

import os
from time import sleep
from threading import Thread
from optparse import OptionParser

from executor_manager import ExecutorManager
from task_manager import TaskManager

EXECUTOR_STATE_FILE = "executor_state.txt"

task_manager = None
executor_manager = None

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

        opt.add_option('--build_number',
                       dest='build_number',
                       type=str,
                       help='The build number')

        opt.add_option('--task_list_file',
                       dest='task_list_file',
                       type=str,
                       help='The file stores the task list')

        (arguments, _) = opt.parse_args()

    except Exception as ex:
        print("Exception : %s" % ex.message)

    return arguments

def executor_run_task(executor, task):
    """
    The method to be executed in worker thread
    :param executor: executor to run task
    :param task: task to be executed
    :return: None
    """
    global task_manager
    global executor_manager
    if executor.run_task(task):
        task_manager.mark_task_as_executed(task)
    else:
        task_manager.put_back_to_task_pool(task)

if __name__=="__main__":
    arguments = get_arguments()
    if arguments is None:
        print """
        Usage: python dispatcher.py --build_type=<build_type> --build_number=<build_number> --task_list=<task_list_file>
        """
    executor_manager = ExecutorManager()
    executor_manager.load_executors(build_type=arguments.build_type, build_number=arguments.build_number)

    task_manager = TaskManager()
    task_manager.load_tasks(task_file=arguments.task_list_file)

    task = task_manager.get_next_task()
    while task is not None:
        sleep(1)
        if executor_manager.has_valid_executor_for_task(task):
            executor = executor_manager.get_executor_for_task(task)
            if executor is not None:
                worker_thread = Thread(target=executor_run_task, args=(executor, task))
                worker_thread.start()
            else:
                # print "Put task [%s] back to task pool" % task.name
                task_manager.put_back_to_task_pool(task)
            task = task_manager.get_next_task()
        else:
            print "Mark task [%s] as cannot be executed" % task.name
            task_manager.mark_task_as_cannot_be_executed(task)
            task = task_manager.get_next_task()
            continue

    print "All tasks have been distributed, waitting for task running finish"
    executor_manager.wait_for_executor_finish_task()
    print "All tasks finished running"

    print "Start dumping executor status"
    log_dir = arguments.task_list_file[:arguments.task_list_file.rfind("/") + 1]
    executor_log_file = log_dir + EXECUTOR_STATE_FILE
    executor_manager.dump_executor_state(executor_log_file)
