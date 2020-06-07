# -*- coding: utf8 -*-

from __future__ import absolute_import, unicode_literals
import main

from celery import Celery
from kombu import Queue, Exchange

app = Celery()
celeryconfig = {}
celeryconfig['BROKER_URL'] = 'amqp://admin:fhnkbxyjcnm@localhost/rabbit'
celeryconfig['CELERY_RESULT_BACKEND'] = 'redis'
celeryconfig['CELERY_ACKS_LATE'] = True
celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1
celeryconfig['CELERY_QUEUES'] = (
    Queue('registration', Exchange('registration'), routing_key='registration', queue_arguments={'x-max-priority': 10}),
    Queue('events', Exchange('events'), routing_key='events', queue_arguments={'x-max-priority': 10}),
    Queue('commands', Exchange('commands'), routing_key='commands', queue_arguments={'x-max-priority': 10}),
    Queue('user_messages', Exchange('user_messages'), routing_key='user_messages', queue_arguments={'x-max-priority': 10}),
    Queue('admin_messages', Exchange('admin_messages'), routing_key='admin_messages', queue_arguments={'x-max-priority': 10}),
    Queue('mass_send', Exchange('mass_send'), routing_key='mass_send', queue_arguments={'x-max-priority': 10}),
    Queue('celery', Exchange('celery'), routing_key='celery'),
)
app.config_from_object(celeryconfig)
app.conf.beat_schedule = {
    'directory_id_set_sync': {
        'task': 'main.core.event_handler.vk.tasks.directory_id_set_sync',
        'schedule': 5.0,
    },
    'users_id_set_sync': {
        'task': 'main.core.event_handler.vk.tasks.users_id_set_sync',
        'schedule': 5.0,
    },
    'admins_id_set_sync': {
        'task': 'main.core.event_handler.vk.tasks.admins_id_set_sync',
        'schedule': 15.0,
    },
}
