# -*- coding: utf8 -*-

from celery import Celery
from kombu import Queue, Exchange
import time

app = Celery()
celeryconfig = {}
celeryconfig['BROKER_URL'] = 'amqp://admin:fhnkbxyjcnm@localhost/rabbit'
celeryconfig['CELERY_RESULT_BACKEND'] = 'redis'
celeryconfig['CELERY_ACKS_LATE'] = True
celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1
celeryconfig['CELERY_QUEUES'] = (
    Queue('commands', Exchange('commands'), routing_key='commands', queue_arguments={'x-max-priority': 10}),
    Queue('messages', Exchange('messages'), routing_key='messages', queue_arguments={'x-max-priority': 10}),
)
app.config_from_object(celeryconfig)


@app.task(ignore_result=True)
def add(x, y):
    return x + y


@app.task(ignore_result=True)
def pow(x, y):
    return x ** y


@app.task(ignore_result=True)
def sleep_print(x, y):
    time.sleep(float(x))
    return str(y)


from main.core.db.synchronized.redis.admins_id_set import AdminsIdSet

AdminsIdSet.users_add([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100])
@app.task(ignore_result=True)
def parallel_task(msg):
    AdminsIdSet.sync()
    result = AdminsIdSet.users_remove([msg, msg+1])
    print(AdminsIdSet.data)
    return result
