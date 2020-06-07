# -*- coding: utf8 -*-

from main.core.db.synchronized.redis.discord.admins_id_set import AdminsIdSet
from main.core.db.synchronized.redis.discord.users_id_set import UsersIdSet
from main.core.db.synchronized.redis.discord.directory_id_dictionary import DirectoryIdDictionary
from main.core.navigator import Navigator
Navigator.set_global_package_path('discord')
from main.core.db.synchronized.local.base.event_type_enum import EventType
import threading


def users_id_set_sync():
    UsersIdSet.sync()
    threading.Timer(5, users_id_set_sync).start()
    return


def admins_id_set_sync():
    AdminsIdSet.sync()
    threading.Timer(15, admins_id_set_sync).start()
    return


def directory_id_set_sync():
    DirectoryIdDictionary.sync()
    threading.Timer(5, directory_id_set_sync).start()
    return


async def registration_handler(registration):
    print(f'registration {registration}')
    if registration['type'] not in {EventType.MESSAGE_NEW, EventType.MESSAGE_EDIT}:
        return
    registration_application = Navigator.get(DirectoryIdDictionary.get(registration['message']['user_id']))
    await registration_application.run(registration)
    return


async def user_message_handler(user_message):
    print(f'user_message {user_message}')
    return


async def admin_message_handler(admin_message):
    print(f'admin_message {admin_message}')
    return


async def event_handler(event):
    user_id = None
    if event['type'] in {EventType.MESSAGE_NEW, EventType.MESSAGE_EDIT, EventType.MESSAGE_DELETE}:
        user_id = event['message']['user_id']
    elif event['type'] in {EventType.REACTION_ADD, EventType.REACTION_REMOVE}:
        user_id = event['reaction']['user_id']
    if user_id is not None:
        if AdminsIdSet.user_find(user_id):
            event['privilege'] = 'admin'
            await admin_message_handler(event)
        elif UsersIdSet.user_find(user_id):
            event['privilege'] = 'user'
            await user_message_handler(event)
        else:
            event['privilege'] = 'registration'
            await registration_handler(event)
    return
