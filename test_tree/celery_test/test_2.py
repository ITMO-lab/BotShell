# -*- coding: utf8 -*-

from test_tree.celery_test.test_1 import add, pow, sleep_print, parallel_task
from test_tree.celery_test.extender import TEST as App
from time import sleep

tasks = []


for i in range(10):
    tasks.append(parallel_task.apply_async(args=(i,), queue='commands', priority=i))
for i in range(10):
    tasks.append(parallel_task.apply_async(args=(9-i,), queue='commands', priority=9-i))


# sleep(20)