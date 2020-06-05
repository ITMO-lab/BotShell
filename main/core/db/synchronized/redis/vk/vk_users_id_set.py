# -*- coding: utf8 -*-

from main.core.db.synchronized.redis.base.id_set import IdSet
import threading


class UsersIdSet(IdSet):
    _lock = threading.Lock()
    _data = set()
    _name = 'VkUsersIdSet'
    _redis_db_number = 14
    _redis_lock_db_number = 15
