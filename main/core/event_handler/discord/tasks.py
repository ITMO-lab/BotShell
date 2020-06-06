# -*- coding: utf8 -*-

from main.core.event_handler.discord.celery_app import app
from main.core.db.synchronized.redis.discord.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.discord.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.discord.directory_id_dictionary import DirectoryIdDictionary
from main.core.navigator import Navigator
import requests
from random import getrandbits
import os


cur_dir = '/main/core/event_handler/discord'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += cur_dir
with open(path + '/token.secret') as file:
    token = file.readline()


@app.task(ignore_result=True)
def users_id_set_sync():
    UsersIdSet.sync()
    return


@app.task(ignore_result=True)
def admins_id_set_sync():
    AdminsIdSet.sync()
    return


@app.task(ignore_result=True)
def registration_handler(registration):
    print(f'registration {registration}')
    return


@app.task(ignore_result=True)
def user_message_handler(user_message):
    print(f'user_message {user_message}')
    return


@app.task(ignore_result=True)
def admin_message_handler(admin_message):
    print(f'admin_message {admin_message}')
    return


@app.task(ignore_result=True)
def command_handler(command):
    print(f'command {command}')
    return


@app.task(ignore_result=True)
def event_handler(event):
    print(f'event {event}')
    if event['type'] == 'message_new':
        if AdminsIdSet.user_find(event['object']['message']['from_id']):
            admin_message_handler.apply_async(args=(event,), queue='admin_messages', priority=8)
        elif UsersIdSet.user_find(event['object']['message']['from_id']):
            user_message_handler.apply_async(args=(event,), queue='user_messages', priority=5)
        else:
            registration_handler.apply_async(args=(event,), queue='registration', priority=2)
    return
