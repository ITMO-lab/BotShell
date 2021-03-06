# -*- coding: utf8 -*-

from flask import Flask, request, json
from main.core.db.synchronized.local.vk.client import VkClient
from main.core.event_handler.vk.tasks import event_handler
from main.core.db.synchronized.redis.vk.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.vk.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.vk.directory_id_dictionary import DirectoryIdDictionary

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
        return VkClient.confirmation_token
    else:
        event_handler.apply_async(args=(event,), queue='events', priority=5)
    return 'ok'


flask_app.run(host='193.187.173.181', port=80, debug=True)
