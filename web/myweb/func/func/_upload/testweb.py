#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

from locust import HttpLocust, TaskSet, task


class MyTaskSet(TaskSet):

    @task
    def task(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"}
        r = self.client.get("/", timeout=30, headers=header)
        assert r.status_code == 200


class websitUser(HttpLocust):
    task_set = MyTaskSet
    min_wait = 3000
    max_wait = 6000
