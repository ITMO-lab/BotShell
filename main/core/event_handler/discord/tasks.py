# -*- coding: utf8 -*-

from main.core.event_handler.vk.celery_app import app
from main.core.db.synchronized.redis.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.directory_id_dictionary import DirectoryIdDictionary
from main.core.application import Application
from main.core.navigator import Navigator
import requests
from random import getrandbits
import os

api_url = "https://api.vk.com/method"
api_version = 5.103


cur_dir = '/main/core/event_handler/discord'
path = os.getcwd()
if path.count(cur_dir) == 0:
    path += '/main/core/event_handler/discord'
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
    text = str(registration['object']['message']['text']).lower()
    user_ids = [[registration['object']['message']['from_id'], ], [registration['object']['message']['from_id'], ], ]
    if text.find('12345678') != -1:
        UsersIdSet.user_add(registration['object']['message']['from_id'])
        messages = ["Проводится сканирование вашего сообщения, {0},".format(registration['object']['message']['text']),
                    "Вы пользователь, вам выданы соответствующие права", ]
        mass_send.apply_async(args=(messages, user_ids, ), kwargs=({'attachment' : ['photo7108139_456240833', ]}),
                              queue='mass_send', priority=10)
    else:
        messages = ["Для регистрации предъявите код", "Хей, пс, возьми мой код. Введи цифры от 1 до 8 в одном "
                                                      "сообщении без пробелов"]
        mass_send.apply_async(args=(messages, user_ids,), queue='mass_send', priority=10)
    return


@app.task(ignore_result=True)
def user_message_handler(user_message):
    print(f'user_message {user_message}')
    text = str(user_message['object']['message']['text']).lower()
    if text.find('клаустрофобия') != -1:
        AdminsIdSet.user_add(user_message['object']['message']['from_id'])
        user_ids = [[user_message['object']['message']['from_id'], ],
                    [user_message['object']['message']['from_id'], ], ]
        messages = ["Сейчас посмотрим, {0}...".format(user_message['object']['message']['text']),
                    "Ага, всё верно, вы АДМИН", ]
        mass_send.apply_async(args=(messages, user_ids,), queue='mass_send', priority=10)
    else:
        user_ids = [[user_message['object']['message']['from_id'], ],
                    [user_message['object']['message']['from_id'], ],
                    [user_message['object']['message']['from_id'], ], ]
        messages = ["Я не могу так просто дать тебе права админа", "Сначала отгадай загадку :D",
                    "Как называется боязнь прихода Санта-Клауса?"]
        mass_send.apply_async(args=(messages, user_ids,), queue='mass_send', priority=10)
    return


@app.task(ignore_result=True)
def admin_message_handler(admin_message):
    print(f'admin_message {admin_message}')
    admin_application = Navigator.get(DirectoryIdDictionary.get(int(admin_message['object']['message']['from_id'])))
    admin_application.run(admin_message)
    return


@app.task(ignore_result=True)
def mass_send(messages, user_ids, **kwargs):
    request_code = ""
    for i in range(min(user_ids.__len__(), 25)):
        try:
            message = messages[i]
        except KeyError:
            message = ""
        except IndexError:
            message = ""
        request_code += "API.messages.send({\"message\": \"" + message + "\", \"user_ids\": \"" + str(
            user_ids[i]).replace('[', ' ').replace(']', ' ') + "\", \"random_id\": \"" + str(
            int(getrandbits(64))) + "\""
        for key, value in kwargs.items():
            try:
                request_code += ", \"" + str(key) + "\": \"" + str(value[i]) + "\""
            except KeyError:
                pass
            except IndexError:
                pass
        request_code += "});\n"
    request_code += "return;\n"
    response = requests.post(url=f"{api_url}/execute",
                             data={
                                 "code": request_code,
                                 "access_token": token,
                                 "v": api_version,
                             }).json()
    return response


@app.task(ignore_result=True)
def command_handler(command):
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
