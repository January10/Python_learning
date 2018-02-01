# windows下分布式进程task_worker1.py

from multiprocessing.managers import BaseManager
import time


class QueueManager(BaseManager):
    pass


def worker():
    manager.connect()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    count = 0
    while 1:
        if task.empty():
            print('task is empty')
            break
        else:
            n = task.get()
            count += 1
            print('work %d task:%d * %d...' % (count, n, n))
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(1)
            result.put(r)


if __name__ == '__main__':
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    print('worker start')
    worker()
    print('worker exit.')
