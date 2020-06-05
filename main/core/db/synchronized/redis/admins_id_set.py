# -*- coding: utf8 -*-

from main.core.db.synchronized.redis.base.id_set import IdSet
import threading


class AdminsIdSet(IdSet):
    _lock = threading.Lock()
    _data = set()
    _name = 'AdminsIdSet'
    _redis_db_number = 14
    _redis_lock_db_number = 15
