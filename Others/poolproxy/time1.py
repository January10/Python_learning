# coding:utf-8
__author__ = 'wzq'
from threading import Timer
from .proxypool import PoolProxy


def func():
    f = PoolProxy()
    f.run()


def tt(n):
    a = Timer(n, func)
    a.start()
    a.join()


tt(0.0)  # 立即执行
while 1:
    tt(10800.0)  # 三小时后执行
