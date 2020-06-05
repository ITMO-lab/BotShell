# -*- coding: utf8 -*-

import requests
import json
from main.core.event_handler.vk.tasks import event_handler
from main.core.db.synchronized.redis.vk.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.vk.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.vk.directory_id_dictionary import DirectoryIdDictionary
import os

cur_dir = '/main/core/event_handler/vk'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += '/main/core/event_handler/vk'
with open(path + '/token.secret') as file:
    token = file.readline()
group_id = 195403459

long_poll_server = json.loads(requests.get('https://api.vk.com/method/groups.getLongPollServer?access_token={0}&group_id={1}&v=5.103'.format(token, group_id)).text)['response']
time_stamp = long_poll_server['ts']

AdminsIdSet.sync()
UsersIdSet.sync()
DirectoryIdDictionary.sync()

while True:
    long_poll = json.loads(requests.get('{server}?act=a_check&key={key}&ts={ts}&wait=25'.format(server=long_poll_server['server'], key=long_poll_server['key'], ts=time_stamp)).text)
    event_array = long_poll['updates']
    for event in event_array:
        event_handler.apply_async(args=(event,), queue='events', priority=5)
    time_stamp = int(long_poll['ts'])
