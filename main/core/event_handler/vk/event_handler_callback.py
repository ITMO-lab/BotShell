# -*- coding: utf8 -*-

from flask import Flask, request, json
from main.core.event_handler.vk.tasks import event_handler
from main.core.db.synchronized.redis.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.directory_id_dictionary import DirectoryIdDictionary
import os

cur_dir = '/main/core/event_handler/vk'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += '/main/core/event_handler/vk'
with open(path + '/confirmation_token') as file:
    confirmation_token = file.readline()

flask_app = Flask(__name__)
AdminsIdSet.sync()
UsersIdSet.sync()
DirectoryIdDictionary.sync()

@flask_app.route('/', methods=['POST'])
def processing():
    event = json.loads(request.data)
    if 'type' not in event.keys():
        return 'not vk'
    if event['type'] == 'confirmation':
        return confirmation_token
    else:
        event_handler.apply_async(args=(event,), queue='events', priority=5)
    return 'ok'


flask_app.run(host='193.187.173.181', port=80, debug=True)
