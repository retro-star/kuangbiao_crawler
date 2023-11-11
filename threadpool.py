#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :threadpool.py
# @Time      :2023/10/24 22:48
# @Author    :retro_star
import time
from threading import Thread
from queue import Queue, Empty


class ThreadPool:
    def __init__(self, max_size):
        self.max_size = max_size
        self.thread_list = []
        self.task_list = Queue()
        self.task_num = None

    def run(self):
        self.task_num = self.task_list.unfinished_tasks
        for i in range(self.max_size):
            handle = Thread(target=self.work)
            self.thread_list.append(handle)
            handle.start()

    def put(self, func, *args, **kwargs):
        self.task_list.put((func, args, kwargs))

    def work(self):
        while True:
            try:
                task, args, kwargs = self.task_list.get(block=False)
            except Empty:
                break
            task(*args, **kwargs)
            self.task_list.task_done()

    def join(self):
        while self.task_list.unfinished_tasks:
            remine = self.task_list.unfinished_tasks
            done = self.task_num - remine
            print(f'\r{done}/{self.task_num}', end='')
            time.sleep(3)
        print()
        self.task_list.join()
