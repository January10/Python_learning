# windows分布式进程task_master.py
from multiprocessing.managers import BaseManager
import random, queue


class QueueManager(BaseManager):
    pass


def return_task_queue():
    return task_queue


def return_result_queue():
    return result_queue


def master():
    manager.start()

    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(1, 31):
        n = random.randint(0, 10000)
        print('Put task %d num %d...to task_queue' % (i, n))
        task.put(n)
    print('Try get results from result_queue...')
    for j in range(1, 31):
        r = result.get()
        print('Result %d: %s' % (j, r))

    manager.shutdown()


if __name__ == '__main__':
    task_queue = queue.Queue()
    result_queue = queue.Queue()
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    print('master start')
    master()
    print('master exit.')
