# windows分布式进程task_master.py
from multiprocessing.managers import BaseManager
import random, queue

task_queue = queue.Queue()
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass


def return_task_queue():
    return task_queue


def return_result_queue():
    return result_queue


def master():
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)

    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...to task_queue' % n)
        task.put(n)
    print('Try get results from result_queue...')
    for j in range(10):
        try:
            r = result.get(timeout=10)
            print('Result: %s' % r)
        except queue.Queue:
            print('Result is empty')
    manager.shutdown()
    print('master exit.')


if __name__ == '__main__':
    print('master start')
    master()
